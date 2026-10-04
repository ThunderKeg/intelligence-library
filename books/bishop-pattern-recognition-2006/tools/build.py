"""Compile PRML source Markdown into the reader's static JSON format."""

import argparse
import hashlib
import html
import json
import re
import subprocess
import unicodedata
from pathlib import Path

import fitz
import markdown
from bs4 import BeautifulSoup, Comment, Tag, NavigableString


ROOT = Path(__file__).resolve().parents[3]
BOOK_ID = "bishop-pattern-recognition-2006"
BOOK = ROOT / "books" / BOOK_ID
PDF = ROOT / "Bishop-Pattern-Recognition-and-Machine-Learning-2006.pdf"
PAGE_MARKER = re.compile(r"pdf-page:\s*(\d+)")
NUMBERED_HEADING = re.compile(r"^((?:\d+|[A-E])(?:\.\d+)*)\.?\s+(.+)$")
CHAPTER_HEADING = re.compile(r"^第\s*(\d+)\s*章\s*(.+)$")
DISPLAY_MATH = re.compile(r"(?<!\\)\$\$(.+?)(?<!\\)\$\$", re.DOTALL)
INLINE_MATH = re.compile(r"(?<!\\)\$(?!\$)(.+?)(?<!\\)\$", re.DOTALL)
MATH_TOKEN = re.compile(r"BISHOPMATH(?:DISPLAY|INLINE)\d{6}")
TAG = re.compile(r"\\tag\{([^{}]+)\}")


def protect_math(raw: str) -> tuple[str, dict[str, tuple[str, bool]]]:
    expressions: dict[str, tuple[str, bool]] = {}

    def replace_display(match: re.Match) -> str:
        token = f"BISHOPMATHDISPLAY{len(expressions):06d}"
        expressions[token] = (match.group(1).strip(), True)
        return token

    def replace_inline(match: re.Match) -> str:
        token = f"BISHOPMATHINLINE{len(expressions):06d}"
        expressions[token] = (match.group(1).strip(), False)
        return token

    return INLINE_MATH.sub(replace_inline, DISPLAY_MATH.sub(replace_display, raw)), expressions


def restore_math_text(value: str, expressions: dict[str, tuple[str, bool]]) -> str:
    return MATH_TOKEN.sub(lambda match: ("$$" if expressions[match.group()][1] else "$")
                          + expressions[match.group()][0]
                          + ("$$" if expressions[match.group()][1] else "$"), value)


def inline_segments(value: str, expressions: dict[str, tuple[str, bool]]) -> list[str | dict]:
    segments = []
    last = 0
    for match in MATH_TOKEN.finditer(value):
        if match.start() > last:
            segments.append(value[last:match.start()])
        tex, display = expressions[match.group()]
        if display:
            raise ValueError("Display math embedded in paragraph")
        segments.append({"tex": tex, "text": tex})
        last = match.end()
    if last < len(value):
        segments.append(value[last:])
    return segments


def list_items(node: Tag, expressions: dict[str, tuple[str, bool]]) -> list[dict]:
    result = []
    for item in node.find_all("li", recursive=False):
        nested = item.find(["ul", "ol"], recursive=False)
        value = "".join(str(part) if isinstance(part, str) else part.get_text() for part in item.contents if part is not nested).strip()
        entry = {"text": restore_math_text(value, expressions), "segments": inline_segments(value, expressions)}
        if nested:
            entry["children"] = list_items(nested, expressions)
            entry["ordered"] = nested.name == "ol"
            if nested.name == "ol" and nested.get("start"):
                entry["start"] = int(nested["start"])
        result.append(entry)
    return result


def original_contents_items(node: Tag) -> list[dict]:
    items = []
    for item in node.find_all("li", recursive=False):
        value = item.get_text(" ", strip=True)
        title, separator, page = value.rpartition(" — ")
        if not separator or not title or not page:
            raise ValueError(f"Invalid original contents item: {value}")
        match = re.match(r"^((?:\d+|[A-E])(?:\.\d+)*)\s", title)
        depth = match.group(1).count(".") if match else (0 if item.find("strong") else 1)
        entry = {"text": value, "title": title, "pageLabel": page,
                 "depth": depth, "strong": bool(item.find("strong"))}
        link = item.find("a", href=True)
        if link:
            href = link["href"]
            if not re.fullmatch(rf"\?book={BOOK_ID}&chapter=[\w-]+(?:#read-[\w-]+)?", href):
                raise ValueError(f"Invalid original contents target: {href}")
            entry["href"] = href
        items.append(entry)
    return items


def table_text(node: Tag) -> str:
    rows = []
    for row in node.find_all("tr"):
        cells = [cell.get_text(" ", strip=True).replace("|", "∣") for cell in row.find_all(["th", "td"], recursive=False)]
        rows.append("| " + " | ".join(cells) + " |")
        if len(rows) == 1:
            rows.append("| " + " | ".join("---" for _ in cells) + " |")
    return "\n".join(rows)


def table_rows(node: Tag, expressions: dict[str, tuple[str, bool]]) -> list[list[dict]]:
    rows = []
    for row_index, row in enumerate(node.find_all("tr")):
        cells = []
        for cell in row.find_all(["th", "td"], recursive=False):
            value = cell.get_text(" ", strip=True)
            entry = {"text": restore_math_text(value, expressions), "segments": inline_segments(value, expressions)}
            if row_index == 0 or cell.name == "th":
                entry["header"] = True
            for attribute in ("colspan", "rowspan"):
                if cell.get(attribute):
                    entry[attribute] = int(cell[attribute])
            cells.append(entry)
        rows.append(cells)
    return rows


def rich_segments(node: Tag, expressions: dict) -> list:
    """Preserve source emphasis, inline code and external links around mathematics."""
    result = []
    for child in node.children:
        if isinstance(child, Comment):
            continue
        if isinstance(child, NavigableString):
            result.extend(inline_segments(str(child), expressions))
        elif child.name == "br":
            result.append(" ")
        elif child.name in {"em", "strong"}:
            result.append({child.name: True, "text": restore_math_text(child.get_text(), expressions),
                           "segments": rich_segments(child, expressions)})
        elif child.name == "code":
            result.append({"code": True, "text": child.get_text()})
        elif child.name == "a" and re.match(r"^https?://", child.get("href", "")):
            result.append({"href": child["href"], "text": child.get_text()})
        else:
            result.extend(rich_segments(child, expressions))
    return result


def visible_math_alphabet(markup: str) -> str:
    """Preserve legacy MathML alphabets in browsers that implement MathML Core."""
    styles = {v:v.replace('-', ' ').upper() for v in ('bold','italic','bold-italic','script',
        'bold-script','fraktur','bold-fraktur','double-struck','monospace')}
    styles.update({'double-struck':'DOUBLE-STRUCK','sans-serif':'SANS-SERIF','bold-sans-serif':'SANS-SERIF BOLD',
                   'sans-serif-italic':'SANS-SERIF ITALIC','sans-serif-bold-italic':'SANS-SERIF BOLD ITALIC'})
    exceptional = {('italic','h'):'ℎ', **{('fraktur',k):v for k,v in zip('CHIRZ','ℭℌℑℜℨ')}}

    def replace(match):
        tag, variant, value = match.groups()
        if variant not in styles:
            return match[0]
        converted = []
        for char in html.unescape(value):
            if ('A' <= char <= 'Z') or ('a' <= char <= 'z'):
                name = ('CAPITAL ' if char.isupper() else 'SMALL ') + char.upper()
            elif '0' <= char <= '9':
                name = unicodedata.name(char)
            else:
                name = unicodedata.name(char, '')
                if name.startswith('MATHEMATICAL '):
                    converted.append(char)
                    continue
                if name.startswith('GREEK '):
                    name = name.removeprefix('GREEK ').replace('LETTER ', '').replace('LUNATE ', '')
                elif name not in {'NABLA', 'PARTIAL DIFFERENTIAL'}:
                    converted.append(char)
                    continue
            glyph = exceptional.get((variant,char))
            for candidate in (f'MATHEMATICAL {styles[variant]} {name}',f'{styles[variant]} {name}'):
                if glyph:
                    break
                try:
                    glyph = unicodedata.lookup(candidate)
                except KeyError:
                    pass
            converted.append(glyph or char)
        return f'<{tag} mathvariant="{variant}">{html.escape("".join(converted),quote=False)}</{tag}>'

    return re.sub(r'<(mi|mn|mo) mathvariant="([a-z-]+)">([^<]+)</\1>',replace,markup)


def compile_math(blocks: list[dict]) -> None:
    expressions = []
    targets = []

    def visit(value):
        if isinstance(value, dict):
            if isinstance(value.get("tex"), str):
                expressions.append({"tex":value["tex"], "display":value.get("kind") == "formula"})
                targets.append(value)
            for child in value.values():
                visit(child)
        elif isinstance(value, list):
            for child in value:
                visit(child)

    visit(blocks)
    if not expressions:
        return
    conversion = subprocess.run(
        ["node", str(ROOT / "scripts/tex_to_mathml.js")],
        input=json.dumps(expressions, ensure_ascii=False),
        text=True,
        encoding="utf-8",
        capture_output=True,
        check=False,
    )
    if conversion.returncode:
        raise ValueError(f"KaTeX conversion failed: {conversion.stderr.strip()}")
    mathml = json.loads(conversion.stdout)
    if len(mathml) != len(targets):
        raise ValueError("KaTeX conversion lost an expression")
    for target, markup in zip(targets, mathml):
        # KaTeX encodes negative thin spaces as positive mtext spaces in MathML.
        # Join only the source's overlaid perpendicular pair into its dedicated
        # Unicode relation; retain the original TeX for copying and source audits.
        independent = '<mo>⊥</mo>' + '<mtext>\u2009\u2063</mtext>' * 3 + '<mo>⊥</mo>'
        dependent = '<mo>⊥̸</mo>' + '<mtext>\u2009\u2063</mtext>' * 3 + '<mo>⊥</mo>'
        if r'\perp\!\!\!\perp' in target['tex']:
            relation = '<mo lspace="0.278em" rspace="0.278em">{}</mo>'
            markup = markup.replace(dependent, relation.format('⫫̸')).replace(independent, relation.format('⫫'))
        markup = markup.replace('<mo stretchy="true">⏟</mo>',
                                '<mo stretchy="true" minsize="100%">⏟</mo>')
        # KaTeX uses U+2223 for scalable \left|...\right| fences, but MathML
        # Core treats that glyph as a non-stretching relation by default.
        # Explicit fence nodes may stretch; ordinary conditional \mid may not.
        markup = markup.replace('<mo fence="true">∣</mo>',
                                '<mo fence="true" stretchy="true">∣</mo>')
        markup = re.sub(r'<mstyle mathvariant="bold"><mi mathvariant="sans-serif">([A-Za-z])</mi></mstyle>',
                        r'<mi mathvariant="bold-sans-serif">\1</mi>', markup)
        if re.fullmatch(r"\\boldsymbol\{\\mathsf\{[A-Za-z]\}\}", target["tex"]):
            markup = markup.replace('mathvariant="sans-serif"', 'mathvariant="bold-sans-serif"')
        for letter in set(re.findall(r"\\boldsymbol\{\\mathsf\{([A-Za-z])\}\}", target["tex"])):
            # KaTeX emits explicit sans-serif which overrides the enclosing bold style.
            # Restrict the correction to the letter explicitly marked bold in source TeX.
            markup = markup.replace(f'<mi mathvariant="sans-serif">{letter}</mi>',
                                    f'<mi mathvariant="bold-sans-serif">{letter}</mi>')
        target["mathml"] = visible_math_alphabet(markup)


def render_chapter(number: int | str, source: Path, page_range: tuple[int, int]) -> dict:
    raw = source.read_text(encoding="utf-8")
    if re.search(r"\b(?:TODO|TBD)\b|待补|此处略", raw, re.IGNORECASE):
        raise ValueError(f"Unfinished placeholder in {source}")
    protected, expressions = protect_math(raw)
    rendered = markdown.markdown(protected, extensions=["fenced_code", "tables", "footnotes", "sane_lists"], output_format="html5")
    soup = BeautifulSoup(rendered, "html.parser")
    for reference in soup.select("span.margin-reference"):
        # A PDF margin reference must remain separate from the surrounding sentence.
        reference.insert(0, NavigableString("（"))
        reference.append(NavigableString("）"))
    first_marker = next((int(match.group(1)) for node in soup.contents if isinstance(node, Comment) if (match := PAGE_MARKER.search(str(node)))), None)
    if first_marker != page_range[0]:
        raise ValueError(f"First PDF page marker must be {page_range[0]} in {source}")

    current_page = first_marker
    seen_pages = set()
    counters: dict[int, int] = {}
    blocks = []
    toc = []
    images = []
    h1_count = 0
    join_next_paragraph = False
    join_space = False
    join_across_kind = None
    join_list_item = False
    join_next_procedure = False
    procedure_ids = set()
    biography_ids = set()
    for node in soup.contents:
        if isinstance(node, Comment):
            match = PAGE_MARKER.search(str(node))
            if match:
                page = int(match.group(1))
                if not current_page <= page <= page_range[1]:
                    raise ValueError(f"Out-of-order PDF page marker {page} in {source}")
                current_page = page
                seen_pages.add(page)
            elif str(node).strip() == "join-previous-paragraph":
                join_next_paragraph = True
                join_space = False
                join_across_kind = None
                join_list_item = False
            elif str(node).strip() == "join-previous-paragraph-with-space":
                join_next_paragraph = True
                join_space = True
                join_across_kind = None
                join_list_item = False
            elif str(node).strip() in {"join-previous-paragraph-across-figures", "join-previous-paragraph-across-tables", "join-previous-paragraph-across-biography"}:
                join_next_paragraph = True
                join_space = False
                join_across_kind = {"figures":"figure", "tables":"table", "biography":"biography"}[str(node).strip().rsplit("-across-", 1)[1]]
                join_list_item = False
            elif str(node).strip() in {"join-previous-list-item", "join-previous-list-item-across-figures"}:
                join_next_paragraph = True
                join_space = False
                join_across_kind = "figure" if str(node).strip().endswith("-across-figures") else None
                join_list_item = True
            elif str(node).strip() == "join-previous-procedure":
                if join_next_paragraph or join_next_procedure:
                    raise ValueError(f"Conflicting procedure continuation in {source}")
                join_next_procedure = True
            continue
        if not isinstance(node, Tag):
            if str(node).strip():
                raise ValueError(f"Unexpected unwrapped text in {source}: {str(node)[:80]}")
            continue
        if node.name in ("script", "style", "iframe") or node.find(["script", "style", "iframe"]):
            raise ValueError(f"Unsupported HTML element in {source}")
        for element in [node, *node.find_all(True)]:
            if any(attribute.lower().startswith("on") for attribute in element.attrs):
                raise ValueError(f"Event handler in {source}")
            if element.get("href", "").strip().lower().startswith("javascript:"):
                raise ValueError(f"Unsafe link in {source}")
        counters[current_page] = counters.get(current_page, 0) + 1
        chapter_page = current_page - page_range[0] + 1
        block_id = f"p{chapter_page:02d}-b{counters[current_page]:03d}"
        common = {"id": block_id, "page": chapter_page, "pdfPage": current_page}
        if node.name in ("h1", "h2", "h3"):
            heading = node.get_text(" ", strip=True)
            if MATH_TOKEN.search(heading):
                raise ValueError(f"Math in a heading needs plain-text notation in {source}: {heading}")
            level = int(node.name[1])
            block = {**common, "kind": "heading", "level": level, "text": heading}
            if level == 1:
                h1_count += 1
                if number == 0 and heading == "前言":
                    toc.append({"number": "序", "title": "前言", "block": block_id, "level": level})
                elif isinstance(number, int):
                    match = CHAPTER_HEADING.match(heading)
                    if not match or int(match.group(1)) != number:
                        raise ValueError(f"Invalid chapter heading in {source}")
                    toc.append({"number": str(number), "title": match.group(2), "block": block_id, "level": level})
                elif number in {"A", "B", "C", "D", "E"}:
                    prefix = f"附录 {number}"
                    if not heading.startswith(prefix):
                        raise ValueError(f"Invalid appendix heading in {source}")
                    toc.append({"number": prefix, "title": heading.removeprefix(prefix).strip(), "block": block_id, "level": level})
                else:
                    expected = {
                        "frontmatter": "封面与出版信息",
                        "preface": "前言",
                        "notation": "数学记号",
                        "references": "参考文献",
                        "contents": "原书目录",
                        "bibliography": "参考文献",
                        "index": "索引",
                    }.get(number)
                    if heading != expected:
                        raise ValueError(f"Invalid book-matter heading in {source}: {heading}")
                    toc.append({"number": "", "title": heading, "block": block_id, "level": level})
            else:
                match = NUMBERED_HEADING.match(heading)
                toc.append({"number": match.group(1) if match else "", "title": match.group(2) if match else heading, "block": block_id, "level": level})
        elif node.name == "aside" and "chapter-guide" in node.get("class", []):
            value = node.get_text(" ", strip=True)
            block = {**common, "kind": "intro", "text": restore_math_text(value, expressions), "segments": inline_segments(value, expressions)}
        elif node.name == "aside" and "procedure" in node.get("class", []):
            children = []
            for child in node.find_all(recursive=False):
                child_common = {**common, "id": f"{block_id}-step{len(children)+1}"}
                value = child.get_text(" ", strip=True)
                if child.name == "h3":
                    children.append({**child_common, "kind": "heading", "level": 3,
                                     "text": restore_math_text(value, expressions),
                                     "segments": rich_segments(child, expressions)})
                elif child.name in ("ol", "ul"):
                    item = {**child_common, "kind": "list", "ordered": child.name == "ol",
                            "items": list_items(child, expressions)}
                    if child.name == "ol" and child.get("start"):
                        item["start"] = int(child["start"])
                    children.append(item)
                elif child.name == "p" and value in expressions and expressions[value][1]:
                    expression = expressions[value][0]
                    number_match = TAG.search(expression)
                    expression = TAG.sub("", expression).strip()
                    item = {**child_common, "kind": "formula", "tex": expression, "text": expression}
                    if number_match:
                        item["number"] = f"({number_match.group(1)})"
                    children.append(item)
                elif child.name == "p":
                    children.append({**child_common, "kind": "paragraph",
                                     "text": restore_math_text(value, expressions),
                                     "segments": rich_segments(child, expressions)})
                else:
                    raise ValueError(f"Unsupported procedure element: {child.name}")
            if not children:
                raise ValueError(f"Empty procedure in {source}")
            block = {**common, "kind": "box", "blocks": children}
            procedure_ids.add(block_id)
        elif node.name == "aside" and "biography" in node.get("class", []):
            children = []
            for child in node.find_all(recursive=False):
                child_common = {**common, "id": f"{block_id}-bio{len(children)+1}"}
                if child.name == "img":
                    full_src = child.get("src", "")
                    prefix = f"books/{BOOK_ID}/"
                    if not full_src.startswith(prefix+"assets/") or not (ROOT/full_src).is_file():
                        raise ValueError(f"Missing biography image: {full_src}")
                    pixmap = fitz.Pixmap(str(ROOT/full_src))
                    children.append({**child_common, "kind":"figure", "src":full_src.removeprefix(prefix),
                                     "alt":child.get("alt", ""), "caption":"", "captionSegments":[],
                                     "width":pixmap.width, "height":pixmap.height})
                    images.append(full_src)
                elif child.name == "p":
                    children.append({**child_common, "kind":"paragraph", "text":restore_math_text(child.get_text(" ",strip=True),expressions),
                                     "segments":rich_segments(child, expressions)})
                else:
                    raise ValueError(f"Unsupported biography element: {child.name}")
            block = {**common, "kind":"box", "blocks":children}
            biography_ids.add(block_id)
        elif node.name == "figure":
            image = node.find("img")
            if image is None:
                raise ValueError(f"Figure without image in {source}")
            full_src = image.get("src", "")
            prefix = f"books/{BOOK_ID}/"
            image_dir = (f"chapter-{number:02d}" if isinstance(number, int)
                         else f"appendix-{number.lower()}" if number in {"A", "B", "C", "D", "E"}
                         else number)
            if not full_src.startswith(prefix + f"assets/{image_dir}/") or not (ROOT / full_src).is_file():
                raise ValueError(f"Missing or misplaced figure {full_src} in {source}")
            alt = image.get("alt", "").strip()
            caption = node.find("figcaption")
            unnumbered_art = bool(set(node.get("class", [])) & {"chapter-opener", "chapter-art"})
            if not alt or (not unnumbered_art and (caption is None or not caption.get_text(strip=True))):
                raise ValueError(f"Figure missing alt or caption: {full_src}")
            translation = node.find(class_="figure-translation")
            caption_text = caption.get_text(" ", strip=True) if caption else ""
            block = {**common, "kind": "figure", "src": full_src.removeprefix(prefix), "alt": alt,
                     "caption": restore_math_text(caption_text, expressions),
                     "captionSegments": (rich_segments(caption, expressions) if caption and caption.find("a")
                                         else inline_segments(caption_text, expressions))}
            pixmap = fitz.Pixmap(str(ROOT / full_src))
            block["width"], block["height"] = pixmap.width, pixmap.height
            if not unnumbered_art and pixmap.width >= 600:
                block["wide"] = True
            if translation:
                notes = [part.strip() for part in re.split(r"[；;]", translation.get_text(" ", strip=True)) if part.strip()]
                block["annotations"] = [restore_math_text(note, expressions) for note in notes]
                block["annotationSegments"] = [inline_segments(note, expressions) for note in notes]
            images.append(full_src)
        elif node.name == "table":
            block = {**common, "kind": "table", "text": restore_math_text(table_text(node), expressions),
                     "rows": table_rows(node, expressions)}
            if blocks and blocks[-1]["kind"] == "paragraph" and re.match(rf"^表\s*{number}\.\d+[:：]", blocks[-1]["text"]):
                title = blocks.pop()
                block["caption"] = title["text"]
                block["captionSegments"] = title["segments"]
        elif node.name == "pre":
            code = node.find("code")
            language = next((name.removeprefix("language-") for name in code.get("class", []) if name.startswith("language-")), "") if code else ""
            block = {**common, "kind": "code", "text": code.get_text() if code else node.get_text(), "language": language}
        elif node.name in ("ul", "ol"):
            original_contents = number == "contents"
            block = {**common, "kind": "list", "ordered": node.name == "ol",
                     "items": original_contents_items(node) if original_contents else list_items(node, expressions)}
            if original_contents:
                block["originalContents"] = True
            if node.name == "ol" and node.get("start"):
                block["start"] = int(node["start"])
        elif node.name == "blockquote":
            if MATH_TOKEN.search(str(node)):
                raise ValueError(f"Math in a rich quote needs explicit handling in {source}")
            node["class"] = [*node.get("class", []), "book-quote"]
            block = {**common, "kind": "rich", "html": str(node)}
        elif node.name == "p" and set(node.get("class", [])) & {"index-entry", "index-subentry", "reference-entry"}:
            if MATH_TOKEN.search(str(node)):
                raise ValueError(f"Math in a rich index/reference entry needs explicit handling in {source}")
            block = {**common, "kind": "rich", "html": str(node)}
        elif node.name == "p" and node.get_text(strip=True) in expressions and expressions[node.get_text(strip=True)][1]:
            expression = expressions[node.get_text(strip=True)][0]
            number_match = TAG.search(expression)
            number_label = f"({number_match.group(1)})" if number_match else ""
            expression = TAG.sub("", expression).strip()
            block = {**common, "kind": "formula", "tex": expression, "text": expression}
            if number_label:
                block["number"] = number_label
        else:
            content = node.get_text("", strip=False).strip()
            block = {**common, "kind": "paragraph", "text": restore_math_text(content, expressions),
                     "segments": rich_segments(node, expressions)}
        if join_next_procedure:
            if (join_next_paragraph or block_id not in procedure_ids or not blocks
                    or blocks[-1]["id"] not in procedure_ids):
                raise ValueError(f"Procedure continuation must join adjacent procedure boxes in {source}")
            blocks[-1]["blocks"].extend(block["blocks"])
            blocks[-1].setdefault("continuedPdfPages", []).append(current_page)
            join_next_procedure = False
        elif join_next_paragraph and block["kind"] == "rich":
            # Bibliographic entries can continue onto the next PDF page. Keep
            # their inline emphasis and links while joining the hanging paragraph.
            if (join_across_kind or join_list_item or not blocks
                    or blocks[-1]["kind"] != "rich"):
                raise ValueError(f"Reference continuation has no adjacent entry in {source}")
            previous = blocks[-1]
            earlier = BeautifulSoup(previous["html"], "html.parser").find("p")
            later = BeautifulSoup(block["html"], "html.parser").find("p")
            if (earlier is None or later is None
                    or set(earlier.get("class", [])) != {"reference-entry"}
                    or set(later.get("class", [])) != {"reference-entry"}):
                raise ValueError(f"Only reference entries support rich paragraph continuation in {source}")
            if join_space:
                earlier.append(" ")
            for child in list(later.contents):
                earlier.append(child.extract())
            previous["html"] = str(earlier)
            previous.setdefault("continuedPdfPages", []).append(current_page)
            join_next_paragraph = False
            join_space = False
            join_across_kind = None
            join_list_item = False
        elif join_next_paragraph:
            previous_index = len(blocks) - 1
            if join_across_kind:
                while previous_index >= 0 and (
                    blocks[previous_index]["id"] in biography_ids if join_across_kind == "biography"
                    else blocks[previous_index]["kind"] == join_across_kind
                ):
                    previous_index -= 1
            expected_kind = "list" if join_list_item else "paragraph"
            if block["kind"] != "paragraph" or previous_index < 0 or blocks[previous_index]["kind"] != expected_kind:
                raise ValueError(f"Paragraph continuation has no {expected_kind} to join in {source}")
            previous = blocks[previous_index]
            if join_list_item:
                if not previous.get("items") or not isinstance(previous["items"][-1], dict):
                    raise ValueError(f"List continuation has no last item in {source}")
                previous = previous["items"][-1]
            if join_space:
                previous["text"] += " "
                previous["segments"].append(" ")
            previous["text"] += block["text"]
            previous["segments"].extend(block["segments"])
            previous.setdefault("continuedPdfPages", []).append(current_page)
            join_next_paragraph = False
            join_space = False
            join_across_kind = None
            join_list_item = False
        else:
            blocks.append(block)

    if join_next_paragraph:
        raise ValueError(f"Paragraph continuation has no following paragraph in {source}")
    if join_next_procedure:
        raise ValueError(f"Procedure continuation has no following procedure in {source}")
    missing = sorted(set(range(page_range[0], page_range[1] + 1)) - seen_pages)
    if missing:
        raise ValueError(f"Missing PDF page markers in {source}: {missing}")
    if h1_count != 1 or len(toc) < (2 if isinstance(number, int) else 1) or not blocks:
        raise ValueError(f"Missing chapter heading, sections, or content in {source}")
    compile_math(blocks)
    return {
        "schemaVersion": 2,
        "bookId": BOOK_ID,
        "title": next(block["text"] for block in blocks if block["kind"] == "heading" and block["level"] == 1),
        "sourcePdfPages": list(page_range),
        "toc": toc,
        "images": sorted(set(images)),
        "blocks": blocks,
    }


def unit_number(key: str) -> int | str:
    if key.startswith("chapter-"):
        return int(key.split("-")[1])
    if key.startswith("appendix-"):
        return key.split("-")[1].upper()
    return key


def review_fingerprint(chapter: dict, source: Path) -> dict:
    """Bind editorial acceptance to the reviewed source, rendering and assets."""
    content = {key:value for key,value in chapter.items()
               if key not in {'editorialStatus','sourcePdfSha256','reviewRecord'}}
    images = hashlib.sha256()
    for path in sorted(chapter['images']):
        images.update(path.encode('utf-8'))
        images.update(hashlib.sha256((ROOT/path).read_bytes()).digest())
    return {
        'sourceNormalizedSha256':hashlib.sha256(source.read_text(encoding='utf-8').encode('utf-8')).hexdigest(),
        'renderedContentSha256':hashlib.sha256(json.dumps(content,ensure_ascii=False,sort_keys=True,
                                                        separators=(',',':')).encode('utf-8')).hexdigest(),
        'imagesSha256':images.hexdigest(),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("units", nargs="*", help="Unit IDs, e.g. frontmatter or chapter-01")
    parser.add_argument("--preview", action="store_true", help="Update isolated local preview")
    args = parser.parse_args()
    inventory = json.loads((BOOK / "source-inventory.json").read_text(encoding="utf-8"))
    units = {unit["id"]: unit for unit in inventory["units"]}
    for key in args.units:
        if key not in units:
            raise SystemExit(f"Unknown unit: {key}")
        unit = units[key]
        source = BOOK / "translation" / f"{key}.md"
        parts = sorted((BOOK / "translation" / "parts").glob(f"{key}-*.md"))
        if parts:
            # Only the integrator writes assembled sources; authors own separate parts.
            source.parent.mkdir(parents=True, exist_ok=True)
            source.write_text("\n\n".join(p.read_text(encoding="utf-8").strip() for p in parts)+"\n", encoding="utf-8")
        if not source.is_file():
            raise SystemExit(f"Missing source: {source}")
        chapter = render_chapter(unit_number(key), source, (unit["start"], unit["end"]))
        if key == 'index':
            from index_links import link_index
            link_index(chapter)
        chapter["editorialStatus"] = "draft-unreviewed"
        review = unit.get('review',{})
        if review.get('status') == 'accepted' and all(review.get(k) == v for k,v in review_fingerprint(chapter,source).items()):
            if not (BOOK/review['record']).is_file():
                raise ValueError(f'Missing independent review record for {key}')
            chapter['editorialStatus'] = 'reviewed'
            chapter['reviewRecord'] = review['record']
        chapter["sourcePdfSha256"] = inventory["sha256"]
        target = BOOK / f"{key}.json"
        target.write_text(json.dumps(chapter, ensure_ascii=False, separators=(",", ":"))+"\n", encoding="utf-8")
        print(f"{key}: {len(chapter['blocks'])} blocks; {len(chapter['images'])} images; PDF {unit['start']}–{unit['end']}")
    if args.preview:
        chapters = []
        for key, unit in units.items():
            if (BOOK / f"{key}.json").is_file():
                number = unit_number(key)
                title = re.sub(r"^第\s*\d+\s*章\s*", "", unit["title"])
                chapters.append({"id": key, "number": str(number) if isinstance(number, int) else "",
                                 "title": title, "content": f"books/{BOOK_ID}/{key}.json"})
        metadata = [{"id":BOOK_ID, "title":"模式识别与机器学习", "originalTitle":"Pattern Recognition and Machine Learning",
                     "author":"Christopher M. Bishop", "year":"2006", "description":"中文译稿 · 编撰中", "chapters":chapters}]
        if (BOOK / "reference-index.json").exists():
            metadata[0]["referenceIndex"] = f"books/{BOOK_ID}/reference-index.json"
        (BOOK / "preview-books.js").write_text("const books = "+json.dumps(metadata, ensure_ascii=False, indent=2)+";\n", encoding="utf-8")
        print(f"Preview manifest: {len(chapters)} available units; run tools/serve.py for local review")


if __name__ == "__main__":
    main()
