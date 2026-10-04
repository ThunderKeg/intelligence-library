"""Compile this book's Markdown to the existing schemaVersion 3 reader format.

This is a structural compiler, not a translation/completeness/semantic reviewer.
Use --check for read-only validation, --partial for work in progress. Only the
chapter author/integrator should invoke a writing build for their assigned files.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from collections import Counter
from pathlib import Path

import markdown
from bs4 import BeautifulSoup, Comment, NavigableString, Tag
from PIL import Image

from common import BOOK, BOOK_ID, CHAPTERS, CHAPTER_BY_ID, ROOT, TMP, Chapter

PAGE_MARKER = re.compile(r"<!--\s*pdf-page:\s*(\d+)\s*-->")
PAGE_IN_COMMENT = re.compile(r"^\s*pdf-page:\s*(\d+)\s*$")
DISPLAY_MATH = re.compile(r"(?<!\\)\$\$(.+?)(?<!\\)\$\$", re.DOTALL)
INLINE_MATH = re.compile(r"(?<!\\)\$(?!\$)(.+?)(?<!\\)\$", re.DOTALL)
MATH_TOKEN = re.compile(r"CONVEXMATH(?:DISPLAY|INLINE)\d{6}")
TAG = re.compile(r"\\tag\s*\{([^{}]+)\}")
NUMBER = re.compile(r"^(?:[1-9]\d*|[ABC])\.\d+[a-z]?$")
SECTION_NUMBER = re.compile(r"^((?:\d+|[ABC])(?:\.\d+)+)(?:[.、：:]?\s+)(.+)$")
FENCE = re.compile(r"(?ms)^ {0,3}(`{3,}|~{3,})[^\n]*\n.*?^ {0,3}\1[ \t]*(?:\n|$)")
INLINE_CODE = re.compile(r"(`+)(?!`)(.+?)(?<!`)\1(?!`)", re.DOTALL)
ASSET_PREFIX = f"books/{BOOK_ID}/assets/"


def inventory_pages() -> dict[int, dict]:
    source = BOOK / "source-inventory.json"
    if not source.is_file():
        raise ValueError("Run tools/inventory.py before building: source-inventory.json is absent")
    inventory = json.loads(source.read_text(encoding="utf-8"))
    return {page["pdfPage"]: page for page in inventory["pages"]}


def protect_math(raw: str) -> tuple[str, dict[str, dict]]:
    # Code examples can contain literal dollars/backslashes. Hide code before
    # scanning math, then restore it for the Markdown compiler.
    codes: dict[str, str] = {}

    def hide_code(match: re.Match[str]) -> str:
        token = f"CONVEXCODE{len(codes):06d}"
        codes[token] = match.group()
        return token + ("\n" if match.group().endswith("\n") else "")

    protected = INLINE_CODE.sub(hide_code, FENCE.sub(hide_code, raw))
    expressions: dict[str, dict] = {}

    def replace(match: re.Match[str], display: bool) -> str:
        original = match.group(1).strip()
        numbers = TAG.findall(original)
        if len(numbers) > 1 or (numbers and not display):
            raise ValueError("Use at most one original equation \\tag{number} per display formula")
        if numbers and not NUMBER.fullmatch(numbers[0]):
            raise ValueError(f"Invalid original equation number: {numbers[0]}")
        tex = TAG.sub("", original).strip()
        if not tex:
            raise ValueError("Empty TeX expression")
        token = f"CONVEXMATH{'DISPLAY' if display else 'INLINE'}{len(expressions):06d}"
        expressions[token] = {"tex": tex, "sourceTex": original, "display": display,
                              "number": numbers[0] if numbers else None}
        return token

    protected = DISPLAY_MATH.sub(lambda match: replace(match, True), protected)
    protected = INLINE_MATH.sub(lambda match: replace(match, False), protected)
    for token, code in codes.items():
        protected = protected.replace(token, code)
    return protected, expressions


def compile_math(expressions: dict[str, dict]) -> dict[str, str]:
    if not expressions:
        return {}
    payload = [{"tex": value["tex"], "display": value["display"]} for value in expressions.values()]
    result = subprocess.run(["node", str(ROOT / "scripts" / "tex_to_mathml.js")],
                            input=json.dumps(payload, ensure_ascii=False), text=True,
                            encoding="utf-8", capture_output=True, check=False)
    if result.returncode:
        raise ValueError(f"TeX to MathML conversion failed: {result.stderr.strip()}")
    values = json.loads(result.stdout)
    if len(values) != len(expressions):
        raise ValueError("MathML expression count differs from source TeX count")
    return dict(zip(expressions, values))


def normalize_native_math(node: Tag) -> None:
    """Keep mathematical alphabets and stacked operators visible in rich MathML.

    The shared reader's rich blocks bypass renderMathml(), so this book needs
    the same explicit alphabet glyphs. Record the original token information
    to make every presentation-only change reversible during independent QA.
    """
    script_capitals = "𝒜ℬ𝒞𝒟ℰℱ𝒢ℋℐ𝒥𝒦ℒℳ𝒩𝒪𝒫𝒬ℛ𝒮𝒯𝒰𝒱𝒲𝒳𝒴𝒵"

    # KaTeX nests a bold operator's letter tokens inside an mi/mrow, which
    # native MathML cannot interpret as a single identifier. Flatten only
    # that exact alphabetic shape, preserving the following function-
    # application operator and the original TeX/MathML for inspection.
    for token in list(node.find_all("mi", attrs={"mathvariant": "normal"})):
        if len(token.contents) != 1 or not isinstance(token.contents[0], Tag):
            continue
        row = token.contents[0]
        if row.name != "mrow" or row.attrs or not row.contents:
            continue
        letters = row.contents
        if not all(isinstance(letter, Tag) and letter.name == "mi"
                   and letter.attrs == {"mathvariant": "bold"}
                   and len(letter.contents) == 1
                   and isinstance(letter.contents[0], NavigableString)
                   and re.fullmatch(r"[A-Za-z]", str(letter.contents[0]))
                   for letter in letters):
            continue
        original = str(token)
        name = "".join(letter.get_text() for letter in letters)
        token.clear()
        token.string = name
        token["mathvariant"] = "bold"
        token["data-source-operator-mathml"] = original
        application = token.find_next_sibling()
        argument = application.find_next_sibling() if application is not None else None
        # Native MathML gives U+2061 zero space, unlike TeX's thin space
        # between an operator and an ordinary/inner argument. Opening
        # delimiters, explicit spaces, and isolated names remain untouched.
        if (application is not None and application.name == "mo"
                and application.get_text() == "\u2061" and not application.attrs
                and argument is not None
                and argument.name in {"mi", "mn", "msub", "msup", "msubsup",
                                      "mrow", "mover", "munder", "munderover",
                                      "mfrac", "msqrt", "mroot"}):
            application["data-source-operator-spacing"] = str(application)
            application["rspace"] = "0.1667em"
        elif (application is not None and application.name == "mo"
              and application.get_text() == "\u2061" and not application.attrs
              and argument is None and token.parent.name == "mrow"
              and token.parent.contents == [token, application]
              and token.parent.parent.name in {"msub", "msup", "msubsup"}
              and token.parent.parent.contents[0] is token.parent):
            # In epi_K f the application token is inside the script base.
            # Put spacing after the complete scripted name, never before K.
            operator = token.parent.parent
            argument = operator.find_next_sibling()
            if argument is not None and argument.name in {"mi", "mn", "msub", "msup", "msubsup",
                                                          "mrow", "mover", "munder", "munderover",
                                                          "mfrac", "msqrt", "mroot"}:
                spacer = BeautifulSoup('<mspace width="0.1667em" data-source-operator-script-spacing="true"></mspace>',
                                       "html.parser").mspace
                operator.insert_after(spacer)

    def glyph(variant: str, char: str) -> str:
        if variant == "script" and "A" <= char <= "Z":
            return script_capitals[ord(char) - ord("A")]
        if variant == "bold":
            for first, last, start in [("A", "Z", 0x1D400), ("a", "z", 0x1D41A), ("0", "9", 0x1D7CE)]:
                if first <= char <= last:
                    return chr(start + ord(char) - ord(first))
        return char

    for token in node.find_all(["mi", "mn"], attrs={"mathvariant": ["script", "bold"]}):
        if token.find(True):
            continue
        original = token.get_text()
        variant = token["mathvariant"]
        rendered = "".join(glyph(variant, char) for char in original)
        if rendered != original:
            token["data-source-glyph"] = original
            token["data-source-mathvariant"] = variant
            token["mathvariant"] = "normal"
            token.string = rendered

    def sole_element(parent: Tag, child: Tag) -> bool:
        meaningful = [item for item in parent.contents if isinstance(item, Tag) or str(item).strip()]
        return len(meaningful) == 1 and meaningful[0] is child

    # KaTeX can wrap an overset binary operator in mo tokens. An mo cannot
    # contain a mover; Chromium flattens its children into adjacent glyphs.
    # Unwrap only these single-child token chains, preserving the binary
    # spacing on the base operator. Ordinary mo tokens are left untouched.
    for mover in list(node.find_all("mover")):
        outer = mover
        spacing = {}
        while outer.parent.name == "mo" and sole_element(outer.parent, outer):
            outer = outer.parent
            spacing.update({key: outer[key] for key in ("lspace", "rspace") if outer.has_attr(key)})
        if outer is mover:
            continue
        original = str(outer)
        base = mover.find(True, recursive=False)
        while base is not None and base.name == "mo":
            inner = base.find("mo", recursive=False)
            if inner is None or not sole_element(base, inner):
                break
            for key, val in base.attrs.items():
                inner.attrs.setdefault(key, val)
            base.replace_with(inner.extract())
            base = inner
        if base is not None and base.name == "mo":
            base.attrs.update(spacing)
        mover["data-source-mathml"] = original
        outer.replace_with(mover.extract())


def math_node(soup: BeautifulSoup, value: dict, markup: str) -> Tag:
    node = BeautifulSoup(markup, "html.parser").math
    if node is None:
        raise ValueError(f"MathML root missing for {value['tex'][:80]}")
    normalize_native_math(node)
    node["display"] = "block" if value["display"] else "inline"
    node["data-tex"] = value["sourceTex"]
    if value["display"]:
        node["style"] = "min-width:max-content"
    # Native MathML can compress CJK mtext in an mtable down to one glyph on
    # narrow screens, discarding the remaining characters instead of wrapping.
    # Keep textual labels intact and let the containing formula scroll.
    for text_node in node.find_all("mtext"):
        text_node["style"] = "white-space:nowrap"
    # Chromium's native MathML does not apply mtable columnalign to the cells.
    # Without explicit CSS an aligned derivation centers each right-hand side,
    # so its equality/inequality signs drift between lines.
    for table in node.find_all("mtable"):
        for row in table.find_all(["mtr", "mlabeledtr"], recursive=False):
            columns = row.get("columnalign", table.get("columnalign", "center")).split()
            column = 0
            for cell in row.find_all("mtd", recursive=False):
                align = cell.get("columnalign", columns[min(column, len(columns) - 1)])
                if align in {"left", "right", "center"}:
                    # The prefixed value also aligns the MathML layout box;
                    # standard right alone can leave mstyle content at its left.
                    cell["style"] = (cell.get("style", "").rstrip(";")
                                     + f";text-align:{align};text-align:-webkit-{align}")
                    cell["style"] = cell["style"].lstrip(";")
                column += int(cell.get("columnspan", "1"))
    for fence in node.find_all("mo", attrs={"fence": "true"}):
        if not fence.has_attr("stretchy"):
            fence["stretchy"] = "true"
    # Standard MathML source annotation preserves copyable TeX, without adding
    # process information to the reading text.
    semantics = soup.new_tag("semantics")
    row = soup.new_tag("mrow")
    for child in list(node.contents):
        row.append(child.extract())
    semantics.append(row)
    annotation = soup.new_tag("annotation", attrs={"encoding": "application/x-tex"})
    annotation.string = value["sourceTex"]
    semantics.append(annotation)
    node.append(semantics)
    return node


def insert_math(soup: BeautifulSoup, expressions: dict[str, dict], mathml: dict[str, str]) -> None:
    for node in list(soup.find_all(string=True)):
        if isinstance(node, Comment) or node.find_parent(["code", "pre"]):
            continue
        matches = list(MATH_TOKEN.finditer(str(node)))
        if not matches:
            continue
        text = str(node)
        if any(expressions[match.group()]["display"] for match in matches):
            if len(matches) != 1 or text.strip() != matches[0].group():
                raise ValueError(f"Display math must occupy its own block: {text[:120]}")
            token = matches[0].group()
            value = expressions[token]
            wrapper = soup.new_tag("div", attrs={"class": "book-formula"})
            scroller = soup.new_tag("div", attrs={"class": "formula-scroll"})
            scroller.append(math_node(soup, value, mathml[token]))
            wrapper.append(scroller)
            if value["number"]:
                wrapper["id"] = "eq-" + value["number"].replace(".", "-")
                label = soup.new_tag("span", attrs={"class": "formula-number"})
                label.string = "(" + value["number"] + ")"
                wrapper.append(label)
            if node.parent.name == "p" and node.parent.get_text(strip=True) == token:
                node.parent.replace_with(wrapper)
            else:
                node.replace_with(wrapper)
            continue
        last = 0
        for match in matches:
            if match.start() > last:
                node.insert_before(NavigableString(text[last:match.start()]))
            token = match.group()
            node.insert_before(math_node(soup, expressions[token], mathml[token]))
            last = match.end()
        if last < len(text):
            node.insert_before(NavigableString(text[last:]))
        node.extract()


def visible_text(node: Tag) -> str:
    # annotation is machine-readable TeX, not duplicate visible reading text.
    clone = BeautifulSoup(str(node), "html.parser")
    for annotation in clone.find_all("annotation"):
        annotation.decompose()
    return clone.get_text(" ", strip=True)


def image_dimensions(path: Path) -> tuple[int, int]:
    if path.suffix.lower() == ".svg":
        svg = BeautifulSoup(path.read_text(encoding="utf-8"), "xml")
        if svg.find(["script", "foreignObject", "image", "iframe"]):
            raise ValueError(f"Unsupported active/external SVG element: {path}")
        root = svg.find("svg")
        if root is None or not root.get("viewBox"):
            raise ValueError(f"SVG needs an explicit viewBox: {path}")
        bounds = [float(number) for number in re.split(r"[\s,]+", root["viewBox"].strip())]
        if len(bounds) != 4 or bounds[2] <= 0 or bounds[3] <= 0:
            raise ValueError(f"Invalid SVG viewBox: {path}")
        return round(bounds[2]), round(bounds[3])
    with Image.open(path) as source:
        if source.format not in {"PNG", "JPEG", "WEBP"}:
            raise ValueError(f"Unsupported image format: {path}")
        return source.size


def validate_crop(tag: Tag, path: Path, pages: dict[int, dict]) -> dict:
    provenance_file = path.with_suffix(".source.json")
    provenance = json.loads(provenance_file.read_text(encoding="utf-8")) if provenance_file.exists() else {}
    page_value = tag.get("data-source-page", provenance.get("pdfPage"))
    bounds_value = tag.get("data-source-rect", provenance.get("cropPoints"))
    if page_value is None or bounds_value is None:
        raise ValueError(f"Image requires source page and crop rectangle: {path.name}")
    page_number = int(page_value)
    if page_number not in pages:
        raise ValueError(f"Image source PDF page out of range: {page_number}")
    bounds = ([float(value) for value in re.split(r"[\s,]+", bounds_value.strip())]
              if isinstance(bounds_value, str) else [float(value) for value in bounds_value])
    width, height = pages[page_number]["sizePoints"]
    if len(bounds) != 4 or not (0 <= bounds[0] < bounds[2] <= width + .1 and 0 <= bounds[1] < bounds[3] <= height + .1):
        raise ValueError(f"Invalid source crop rectangle: {path.name}: {bounds}")
    crop_width, crop_height = bounds[2] - bounds[0], bounds[3] - bounds[1]
    if crop_width * crop_height >= .80 * width * height or (crop_width >= .90 * width and crop_height >= .85 * height):
        raise ValueError(f"Whole-page or nearly whole-page PDF images are prohibited: {path.name}")
    if provenance.get("imageSha256") and provenance["imageSha256"] != hashlib.sha256(path.read_bytes()).hexdigest():
        raise ValueError(f"Image no longer matches crop provenance: {path.name}")
    return {"src": path.relative_to(ROOT).as_posix(), "pdfPage": page_number, "cropPoints": bounds}


def validate_and_style(soup: BeautifulSoup, pages: dict[int, dict], chapter_id: str = "") -> tuple[list[str], list[dict]]:
    images, provenance = [], []
    if soup.find(["script", "style", "iframe", "object", "embed", "link", "form", "input", "button"]):
        raise ValueError("Unsupported active HTML in translation")
    classes = {"ol": "book-list", "ul": "book-list", "pre": "book-code",
               "figure": "book-figure", "figcaption": "figure-caption", "table": "book-table"}
    for tag in soup.find_all(True):
        if any(key.lower().startswith("on") for key in tag.attrs):
            raise ValueError(f"HTML event attribute on <{tag.name}>")
        if tag.name in classes:
            tag["class"] = list(dict.fromkeys([*tag.get("class", []), classes[tag.name]]))
        if tag.name == "h4":
            tag["style"] = "margin:1.7em 0 .65em;font:600 19px/1.5 var(--serif);color:var(--ink)"
        if tag.name == "table" and not (tag.parent.name == "div" and "table-scroll" in tag.parent.get("class", [])):
            tag.wrap(soup.new_tag("div", attrs={"class": "table-scroll"}))
        if tag.name == "table" and chapter_id == "contents":
            tag["class"] = list(dict.fromkeys([*tag.get("class", []), "convex-original-contents"]))
            tag["style"] = "min-width:0;width:100%;table-layout:fixed"
            for row in tag.find_all("tr"):
                cells = row.find_all(["th", "td"], recursive=False)
                if cells:
                    cells[0]["style"] = "white-space:normal;overflow-wrap:anywhere;word-break:normal"
                    cells[-1]["style"] = "width:6em;white-space:nowrap;text-align:right"
        if tag.name == "a" and re.match(r"\s*(?:javascript|data|vbscript):", tag.get("href", ""), re.I):
            raise ValueError("Unsafe link in translation")
        if tag.name != "img":
            continue
        src = tag.get("src", "")
        path = (ROOT / src).resolve()
        assets = (BOOK / "assets").resolve()
        if not src.startswith(ASSET_PREFIX) or not path.is_relative_to(assets) or not path.is_file():
            raise ValueError(f"Missing or invalid book-local image: {src}")
        if not tag.get("alt", "").strip():
            raise ValueError(f"Missing image alt text: {src}")
        if tag.find_parent("figure") is None:
            raise ValueError(f"Image must be inside a figure with a caption: {src}")
        provenance.append(validate_crop(tag, path, pages))
        width, height = image_dimensions(path)
        if width <= 0 or height <= 0:
            raise ValueError(f"Invalid image dimensions: {src}")
        tag["width"], tag["height"] = width, height
        tag["style"] = f"width:{width}px;max-width:100%;height:auto;aspect-ratio:{width}/{height}"
        tag["loading"], tag["decoding"] = "lazy", "async"
        if tag.find_parent("a") is None:
            link = soup.new_tag("a", href=src, attrs={"class": "figure-image-link", "target": "_blank", "rel": "noopener"})
            tag.wrap(link)
        images.append(src)
    for figure in soup.find_all("figure"):
        if not figure.find("img"):
            raise ValueError("Each figure needs an image")
        if not figure.find("figcaption") and figure.get("data-uncaptioned") != "true":
            raise ValueError("Each figure needs an image and original translated caption")
        if not figure.select_one(".figure-translation") and figure.get("data-no-english-text") != "true":
            raise ValueError("Each figure needs figure-translation, or an explicit data-no-english-text=true declaration for review")
    return sorted(set(images)), provenance


def source_coverage(raw: str, chapter: Chapter, pages: dict[int, dict], partial: bool) -> dict:
    markers = [int(value) for value in PAGE_MARKER.findall(raw)]
    if not markers or markers[0] != chapter.first:
        raise ValueError(f"First page marker must be PDF page {chapter.first}")
    if markers != sorted(markers) or len(markers) != len(set(markers)):
        raise ValueError("PDF page markers must be increasing and unique")
    if min(markers) < chapter.first or max(markers) > chapter.last:
        raise ValueError(f"Page marker lies outside assigned PDF pages {chapter.first}-{chapter.last}")
    missing = sorted(set(range(chapter.first, chapter.last + 1)) - set(markers))
    if missing and not partial:
        raise ValueError(f"Missing original PDF page markers: {missing}; --partial is for unfinished drafts only")
    empty_nonblank = []
    split = PAGE_MARKER.split(raw)
    for index in range(1, len(split), 2):
        number, fragment = int(split[index]), split[index + 1]
        cleaned = re.sub(r"<!--.*?-->", "", fragment, flags=re.S).strip()
        if not cleaned and not pages[number]["blankCandidate"]:
            empty_nonblank.append(number)
    if empty_nonblank and not partial:
        raise ValueError(f"No translated content after nonblank PDF page markers: {empty_nonblank}")
    return {"presentPdfPages": markers, "missingPdfPages": missing,
            "emptyNonblankPdfPages": empty_nonblank, "scope": "marker presence only; not content completeness"}


def arrange_floating_figures(soup: BeautifulSoup, first_page: int) -> dict[int, int]:
    # Record physical provenance before moving a printed floating figure out of
    # a sentence. The author source and its page markers remain in PDF order.
    # Only explicitly marked figures can move. Same-container moves, return to
    # the preceding example, and exit from a printed frame each have separate
    # guards below. Multiple figures retain their order.
    node_pages: dict[int, int] = {}
    current_page = first_page
    original_nodes = list(soup.contents)
    positions = {id(node): position for position, node in enumerate(soup.descendants)}
    for node in original_nodes:
        if isinstance(node, Comment) and (match := PAGE_IN_COMMENT.fullmatch(str(node))):
            current_page = int(match.group(1))
        elif isinstance(node, Tag):
            node_pages[id(node)] = current_page
            for descendant in node.descendants:
                if isinstance(descendant, Comment) and (match := PAGE_IN_COMMENT.fullmatch(str(descendant))):
                    current_page = int(match.group(1))
                elif isinstance(descendant, Tag) and descendant.name == "figure":
                    node_pages[id(descendant)] = current_page
    def supported_container(node: Tag) -> bool:
        return node is soup or (node.name == "div" and bool(
            {"example", "remark", "exercise", "algorithm"}.intersection(node.get("class", []))))

    original_figures = list(soup.find_all("figure"))
    movement_attributes = ("data-reader-after", "data-reader-owner",
                           "data-reader-after-container", "data-reader-after-previous",
                           "data-reader-return-to-example")
    for figure in original_figures:
        if sum(key in figure.attrs for key in movement_attributes) > 1:
            raise ValueError("A floating figure must have only one movement instruction")
    for node in soup.select("[data-reader-citation]"):
        if node.name != "figure" or "data-reader-after-previous" not in node.attrs:
            raise ValueError("A separate citation belongs only to a returning chapter figure")
    returning_figures = list(soup.select("figure[data-reader-after-previous]"))
    previous_target_position = -1
    for figure in returning_figures:
        destination = figure["data-reader-after-previous"]
        matches = soup.find_all(id=destination)
        number = figure.get("data-figure", "")
        if (figure.parent is not soup or len(matches) != 1
                or matches[0].parent is not soup or matches[0].name != "p"
                or "data-reader-continue" in matches[0].attrs
                or positions[id(matches[0])] >= positions[id(figure)]
                or not NUMBER.fullmatch(number)
                or len(soup.find_all("figure", attrs={"data-figure": number})) != 1):
            raise ValueError(f"Returning float needs a unique earlier chapter paragraph: {destination}")
        target = matches[0]
        citation = target
        if "data-reader-citation" in figure.attrs:
            cited = soup.find_all(id=figure["data-reader-citation"])
            if (len(cited) != 1 or cited[0].parent is not soup or cited[0].name != "p"
                    or "data-reader-continue" in cited[0].attrs
                    or positions[id(cited[0])] > positions[id(target)]):
                raise ValueError(f"Separate figure citation needs a unique chapter paragraph before its destination: {destination}")
            citation = cited[0]
            # The citation may introduce a displayed model. Keep the model and
            # its explanation together, but never borrow a reference from a
            # different section, framed example, list, or illustration.
            group = [node for node in original_nodes if isinstance(node, Tag)
                     and positions[id(citation)] <= positions[id(node)] <= positions[id(target)]]
            if any(not (node.name == "p" or
                        (node.name == "div" and "book-formula" in node.get("class", [])))
                   or node.find(["figure", "img", "h1", "h2", "h3", "h4", "ul", "ol"])
                   or any(bool({"example", "remark", "exercise", "algorithm"}.intersection(
                       child.get("class", []))) for child in [node, *node.find_all("div")])
                   for node in group):
                raise ValueError(f"Separate citation and destination must stay in one paragraph-and-formula group: {destination}")
        if not re.search(rf"图\s*{re.escape(number)}(?![\d.])", citation.get_text(" ")):
            raise ValueError(f"Returning float needs an exact figure citation in its specified paragraph: {destination}")
        if positions[id(matches[0])] < previous_target_position:
            raise ValueError("Returning figures must retain their original relative order")
        previous_target_position = positions[id(matches[0])]

    returning_example_figures = list(soup.select("figure[data-reader-return-to-example]"))
    for figure in returning_example_figures:
        destination = figure["data-reader-return-to-example"]
        matches = soup.find_all(id=destination)
        number = figure.get("data-figure", "")
        if (figure.parent is not soup or len(matches) != 1
                or matches[0].parent is not soup or matches[0].name != "div"
                or "example" not in matches[0].get("class", [])
                or positions[id(matches[0])] >= positions[id(figure)]
                or not NUMBER.fullmatch(number)
                or len(soup.find_all("figure", attrs={"data-figure": number})) != 1):
            raise ValueError(f"Example return needs a unique earlier chapter example and chapter-level figure: {destination}")
        owner = matches[0]
        # The source example must cite the precise figure in its own prose.
        # A later illustration cannot borrow a reference from another figure.
        if not any(re.search(rf"图\s*{re.escape(number)}(?![\d.])", p.get_text(" "))
                   for p in owner.find_all("p", recursive=False)):
            raise ValueError(f"Example return needs an exact figure citation in the example prose: {destination}")
        between = [node for node in original_nodes if isinstance(node, Tag)
                   and positions[id(owner)] < positions[id(node)] < positions[id(figure)]]
        if any(node.name in {"h1", "h2", "h3"} or
               (node.name == "div" and bool({"example", "remark", "exercise", "algorithm"}
                                             .intersection(node.get("class", [])))) for node in between):
            raise ValueError(f"Example return cannot cross another frame or a numbered section: {destination}")

    tails: dict[str, Tag] = {}
    changed_containers: dict[int, Tag] = {}
    # A later printed float can belong to an earlier subsection. Return only
    # explicitly identified chapter figures to paragraphs that actually cite
    # them; keep source positions and physical-page metadata recorded above.
    for figure in returning_figures:
        destination = figure["data-reader-after-previous"]
        target = soup.find(id=destination)
        changed_containers[id(soup)] = soup
        del figure["data-reader-after-previous"]
        figure.attrs.pop("data-reader-citation", None)
        anchor = tails.get(destination, target)
        anchor.insert_after(figure.extract())
        tails[destination] = figure
    # Figure 11.2 is printed in the following chapter-level discussion, while
    # its source example 11.1 explicitly identifies it. This is separate from
    # the older rule that moves a figure out of the immediately following example.
    for figure in returning_example_figures:
        owner = soup.find(id=figure["data-reader-return-to-example"])
        changed_containers[id(soup)] = soup
        changed_containers[id(owner)] = owner
        del figure["data-reader-return-to-example"]
        owner.append(figure.extract())
    # A chapter illustration may float through a framed remark on the next PDF
    # page. Only an explicit request may move it just outside that same frame;
    # the preceding text must cite it, so unrelated figures cannot escape.
    for figure in list(soup.select("figure[data-reader-after-container]")):
        destination = figure["data-reader-after-container"]
        matches = soup.find_all(id=destination)
        container = figure.parent
        number = figure.get("data-figure", "")
        preceding = container.find_previous_sibling(True)
        if (any(key in figure.attrs for key in ("data-reader-after", "data-reader-owner"))
                or len(matches) != 1 or matches[0] is not container
                or container.name != "div" or not supported_container(container)
                or not supported_container(container.parent)
                or not NUMBER.fullmatch(number) or preceding is None
                or preceding.name != "p"
                or not re.search(rf"图\s*{re.escape(number)}(?![\d.])", preceding.get_text(" "))):
            raise ValueError(f"Outside float needs its own framed container and a preceding text citation: {destination}")
        changed_containers[id(container)] = container
        changed_containers[id(container.parent)] = container.parent
        del figure["data-reader-after-container"]
        anchor = tails.get(destination, container)
        anchor.insert_after(figure.extract())
        tails[destination] = figure
    # A printed float may land inside the continuation of the following example
    # even though its caption and the preceding example identify its owner.
    # Support that explicit correction only for the immediately preceding peer
    # example, and require that example to actually refer to this figure.
    for figure in list(soup.select("figure[data-reader-owner]")):
        destination = figure["data-reader-owner"]
        matches = soup.find_all(id=destination)
        parent = figure.parent
        number = figure.get("data-figure", "")
        if ("data-reader-after" in figure.attrs or not NUMBER.fullmatch(number)
                or parent.name != "div" or "example" not in parent.get("class", [])
                or len(matches) != 1 or matches[0].name != "div"
                or "example" not in matches[0].get("class", [])
                or matches[0].parent is not parent.parent
                or parent.find_previous_sibling(True) is not matches[0]
                or not re.search(rf"图\s*{re.escape(number)}(?![\d.])", matches[0].get_text(" "))):
            raise ValueError(f"Figure owner must be the preceding peer example that cites this figure: {destination}")
        owner = matches[0]
        changed_containers[id(parent)] = parent
        changed_containers[id(owner)] = owner
        del figure["data-reader-owner"]
        owner.append(figure.extract())
    for figure in list(soup.select("figure[data-reader-after]")):
        destination = figure["data-reader-after"]
        matches = soup.find_all(id=destination)
        if (not supported_container(figure.parent) or len(matches) != 1
                or matches[0].parent is not figure.parent or matches[0].name == "figure"
                or positions[id(matches[0])] <= positions[id(figure)]):
            raise ValueError(f"Floating figure needs a unique later text sibling in the same container: {destination}")
        anchor = tails.get(destination, matches[0])
        changed_containers[id(figure.parent)] = figure.parent
        del figure["data-reader-after"]
        anchor.insert_after(figure.extract())
        tails[destination] = figure
    # A printed float can interrupt one paragraph or one unordered list. Join
    # only an explicitly identified continuation after floats have moved away.
    # Whitespace and physical-page comments may intervene; other content may not.
    for continuation in list(soup.select("[data-reader-continue]")):
        destination = continuation["data-reader-continue"]
        matches = soup.find_all(id=destination)
        if (len(matches) != 1 or continuation.name not in {"p", "ul"}
                or not supported_container(continuation.parent)
                or matches[0].name != continuation.name
                or matches[0].parent is not continuation.parent
                or continuation.find_previous_sibling(True) is not matches[0]):
            raise ValueError(f"Continuation needs the immediately preceding matching paragraph/list: {destination}")
        target = matches[0]
        changed_containers[id(continuation.parent)] = continuation.parent
        changed_containers[id(target)] = target
        cursor = target.next_sibling
        while cursor is not continuation:
            if not isinstance(cursor, Comment) and str(cursor).strip():
                raise ValueError(f"Continuation would skip intervening content: {destination}")
            cursor = cursor.next_sibling
        # Keep a former fragment ID as an inline anchor at its original textual
        # boundary. For a list this belongs inside its first li, never under ul.
        if continuation.get("id"):
            marker = soup.new_tag("span", id=continuation["id"])
            if continuation.name == "p":
                target.append(marker)
            else:
                first_item = continuation.find("li", recursive=False)
                if first_item is None:
                    raise ValueError("List continuation has no list items")
                first_item.insert(0, marker)
        for child in list(continuation.contents):
            target.append(child.extract())
        continuation.decompose()
    # Moving a float or joining a list can leave adjacent whitespace-only text
    # nodes. HTML parsers coalesce those when the reference linker reparses a
    # block. Normalize only these newly adjacent nodes, so the emitted block is
    # stable across that round trip without touching prose or math/code text.
    for container in changed_containers.values():
        for child in list(container.contents):
            if child.parent is not container or type(child) is not NavigableString or child.strip():
                continue
            adjacent = []
            cursor = child.next_sibling
            while type(cursor) is NavigableString and not cursor.strip():
                adjacent.append(cursor)
                cursor = cursor.next_sibling
            if adjacent:
                whitespace = str(child) + "".join(str(node) for node in adjacent)
                child.replace_with("\n" if "\n" in whitespace else " ")
                for node in adjacent:
                    node.extract()
    if (returning_figures or returning_example_figures) and [id(node) for node in soup.find_all("figure")] != [id(node) for node in original_figures]:
        raise ValueError("Returning floats must preserve the order of all figures, including unmoved ones")
    return node_pages


def compile_chapter(chapter: Chapter, *, source_dir: Path | None = None, partial: bool = False) -> tuple[dict, dict]:
    source = (source_dir or BOOK / "translation") / chapter.source_name
    raw = source.read_text(encoding="utf-8")
    # Deliberately narrow: legitimate source text such as the CIP's "p. cm." or
    # its Chinese translation must not be mistaken for an author placeholder.
    if re.search(r"(?im)^\s*(?:TODO|TBD|待补译|此处略|\[待翻译\])\s*[:：]?.*$", raw):
        raise ValueError(f"Unfinished author placeholder in {source.name}")
    pages = inventory_pages()
    coverage = source_coverage(raw, chapter, pages, partial)
    protected, expressions = protect_math(raw)
    rendered = markdown.markdown(protected, extensions=["fenced_code", "tables", "footnotes", "sane_lists", "md_in_html"], output_format="html5")
    soup = BeautifulSoup(rendered, "html.parser")
    insert_math(soup, expressions, compile_math(expressions))
    images, provenance = validate_and_style(soup, pages, chapter.id)
    if soup.find(string=MATH_TOKEN):
        raise ValueError(f"Unresolved math token in {source.name}")
    headings = soup.find_all("h1")
    if len(headings) != 1:
        raise ValueError(f"Exactly one h1 is required in {source.name}")
    guides = soup.select("aside.chapter-guide")
    if chapter.guide_required and len(guides) != 1:
        raise ValueError(f"Exactly one clearly separated chapter-guide is required in {source.name}")
    if any(guide.find(["math", "img", "table"]) for guide in guides):
        raise ValueError("Keep the short chapter-guide plain text; formulas and figures belong in translated content")

    node_pages = arrange_floating_figures(soup, chapter.first)
    counters: dict[int, int] = {}
    blocks, toc = [], []
    for node in list(soup.contents):
        if isinstance(node, Comment):
            continue
        if isinstance(node, NavigableString):
            if node.strip():
                raise ValueError(f"Unwrapped text in {source.name}: {str(node)[:80]}")
            continue
        if not isinstance(node, Tag):
            continue
        current_page = node_pages[id(node)]
        counters[current_page] = counters.get(current_page, 0) + 1
        block_id = f"p{current_page - chapter.first + 1:03d}-b{counters[current_page]:03d}"
        common = {"id": block_id, "page": current_page - chapter.first + 1, "pdfPage": current_page}
        text = visible_text(node)
        if re.fullmatch(r"h[1-4]", node.name):
            level = int(node.name[1])
            # Keep heading HTML for h4 as the existing text renderer clamps h4
            # to h3; preserving the tag also preserves inline math and anchors.
            block = {**common, "kind": "heading", "level": level, "text": text, "html": str(node)}
            number = chapter.id.lstrip("0") if level == 1 else ""
            title = text
            if match := SECTION_NUMBER.match(text):
                number, title = match.groups()
            toc.append({"number": number, "title": title, "level": level, "block": block_id})
        elif node.name == "aside" and "chapter-guide" in node.get("class", []):
            block = {**common, "kind": "intro", "text": text}
        else:
            block = {**common, "kind": "rich", "html": str(node), "text": text}
        blocks.append(block)
    if not blocks or not toc or toc[0]["level"] != 1:
        raise ValueError(f"Missing chapter content or top-level heading in {source.name}")
    # Apply controlled book CSS synchronously. An asynchronously loaded <link>
    # can arrive after the reader has restored progress, shifting the saved
    # paragraph when the math font and example borders subsequently take effect.
    # Author HTML still cannot contain style or link elements.
    stylesheet = f"books/{BOOK_ID}/assets/reader.css"
    if not (ROOT / stylesheet).is_file():
        raise FileNotFoundError(stylesheet)
    reader_css = (ROOT / stylesheet).read_text(encoding="utf-8")
    reader_css = reader_css.replace('url("fonts/', f'url("books/{BOOK_ID}/assets/fonts/')
    if "</style" in reader_css.lower():
        raise ValueError("Invalid embedded book stylesheet")
    blocks[0]["html"] = f'<style data-book-styles="{BOOK_ID}">{reader_css}</style>' + blocks[0]["html"]
    numbers = [value["number"] for value in expressions.values() if value["number"]]
    duplicates = [number for number, count in Counter(numbers).items() if count > 1]
    if duplicates:
        raise ValueError(f"Duplicate displayed equation numbers: {duplicates}")
    expected_numbers = {item["number"] for page in pages.values() if chapter.first <= page["pdfPage"] <= chapter.last
                        for item in page["equationCandidates"]}
    caption_numbers = {kind: sorted({item["number"] for page in pages.values()
                                    if chapter.first <= page["pdfPage"] <= chapter.last
                                    for item in page["captionCandidates"] if item["kind"] == kind})
                       for kind in ["figure", "table", "algorithm", "example"]}
    figure_numbers = sorted({figure.get("data-figure") or match.group(1)
                             for figure in soup.find_all("figure")
                             if figure.get("data-figure") or (match := re.search(r"图\s*((?:\d+|[ABC])\.\d+)", visible_text(figure.find("figcaption"))))})
    report = {"chapterId": chapter.id, "source": str(source), "scope": "structural checks only",
              "semanticReview": "NOT PERFORMED", "sourceCoverage": coverage,
              "blocks": len(blocks), "headings": len(toc), "images": len(images),
              "inlineMath": sum(not value["display"] for value in expressions.values()),
              "displayMath": sum(value["display"] for value in expressions.values()),
              "equationNumbers": numbers,
              "equationCandidatesNotTagged": sorted(expected_numbers - set(numbers)),
              "taggedNumbersNotInCandidates": sorted(set(numbers) - expected_numbers),
              "sourceCaptionCandidates": caption_numbers, "translatedFigureNumbers": figure_numbers,
              "figureCandidatesNotPresent": sorted(set(caption_numbers["figure"]) - set(figure_numbers)),
              "imageProvenance": provenance}
    document = {"schemaVersion": 3, "bookId": BOOK_ID, "chapterId": chapter.id,
                "title": visible_text(headings[0]), "sourcePdfPages": [chapter.first, chapter.last],
                "toc": toc, "images": images, "blocks": blocks}
    return document, report


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("chapters", nargs="*", help="IDs such as 01 A frontmatter preface; default: existing sources in book order")
    parser.add_argument("--check", action="store_true", help="Compile and validate without writing reader JSON")
    parser.add_argument("--partial", action="store_true", help="Allow missing pages in drafts; never a completion claim")
    parser.add_argument("--source-dir", type=Path, default=BOOK / "translation")
    parser.add_argument("--output-dir", type=Path, default=BOOK)
    parser.add_argument("--report", type=Path, help="Optional structural JSON report, preferably under tmp/convex")
    args = parser.parse_args()
    unknown = [value for value in args.chapters if value not in CHAPTER_BY_ID]
    if unknown:
        parser.error(f"Unknown chapter IDs: {unknown}")
    selected = ([CHAPTER_BY_ID[value] for value in args.chapters] if args.chapters else
                [chapter for chapter in CHAPTERS if (args.source_dir / chapter.source_name).is_file()])
    if not selected:
        parser.error("No translation sources found")
    reports = []
    failed = False
    for chapter in selected:
        try:
            document, report = compile_chapter(chapter, source_dir=args.source_dir, partial=args.partial)
            if not args.check:
                args.output_dir.mkdir(parents=True, exist_ok=True)
                path = args.output_dir / f"chapter-{chapter.id}.json"
                path.write_text(json.dumps(document, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")
            reports.append(report)
            print(json.dumps({"chapter": chapter.id, "blocks": report["blocks"], "images": report["images"],
                              "displayMath": report["displayMath"], "missingPageMarkers": report["sourceCoverage"]["missingPdfPages"],
                              "equationCandidatesNotTagged": report["equationCandidatesNotTagged"],
                              "figureCandidatesNotPresent": report["figureCandidatesNotPresent"],
                              "semanticReview": "NOT PERFORMED"}, ensure_ascii=False), flush=True)
        except (ValueError, FileNotFoundError, subprocess.SubprocessError) as error:
            failed = True
            reports.append({"chapterId": chapter.id, "error": str(error), "semanticReview": "NOT PERFORMED"})
            print(f"ERROR {chapter.id}: {error}", flush=True)
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps({"scope": "structural only", "chapters": reports}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    raise SystemExit(1 if failed else 0)


if __name__ == "__main__":
    main()
