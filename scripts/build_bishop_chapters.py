"""Compile checked Bishop chapter Markdown into the reader's static JSON format."""

import argparse
import json
import re
import subprocess
from pathlib import Path

import fitz
import markdown
from bs4 import BeautifulSoup, Comment, Tag


ROOT = Path(__file__).resolve().parents[1]
BOOK_ID = "bishop-deep-learning-2024"
BOOK = ROOT / "books" / BOOK_ID
PDF = ROOT / "Christopher M. Bishop, Hugh Bishop - Deep Learning_ Foundations and Concepts-Springer (2024).pdf"
PAGE_MARKER = re.compile(r"pdf-page:\s*(\d+)")
NUMBERED_HEADING = re.compile(r"^((?:\d+|[A-C])(?:\.\d+)*)\.?\s+(.+)$")
CHAPTER_HEADING = re.compile(r"^第\s*(\d+)\s*章\s*(.+)$")
DISPLAY_MATH = re.compile(r"(?<!\\)\$\$(.+?)(?<!\\)\$\$", re.DOTALL)
INLINE_MATH = re.compile(r"(?<!\\)\$(?!\$)(.+?)(?<!\\)\$", re.DOTALL)
MATH_TOKEN = re.compile(r"BISHOPMATH(?:DISPLAY|INLINE)\d{6}")
TAG = re.compile(r"\\tag\{([^{}]+)\}")


def chapter_ranges() -> dict[int, tuple[int, int]]:
    with fitz.open(PDF) as document:
        starts = [
            (int(match.group(1)), page)
            for level, title, page in document.get_toc()
            if level == 1 and (match := re.match(r"^(\d+)\s", title))
        ]
    return {
        number: (page, starts[index + 1][1] - 1 if index + 1 < len(starts) else 617)
        for index, (number, page) in enumerate(starts)
    }


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
        match = re.match(r"^((?:\d+|[A-C])(?:\.\d+)*)\s", title)
        depth = match.group(1).count(".") if match else (0 if item.find("strong") else 1)
        items.append({"text": value, "title": title, "pageLabel": page,
                      "depth": depth, "strong": bool(item.find("strong"))})
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


def compile_math(blocks: list[dict]) -> None:
    expressions = []
    targets = []
    for block in blocks:
        if block["kind"] == "formula":
            expressions.append({"tex": block["tex"], "display": True})
            targets.append(block)
        for segment in [*block.get("segments", []), *block.get("captionSegments", [])]:
            if isinstance(segment, dict) and "tex" in segment:
                expressions.append({"tex": segment["tex"], "display": False})
                targets.append(segment)
        for annotation in block.get("annotationSegments", []):
            for segment in annotation:
                if isinstance(segment, dict) and "tex" in segment:
                    expressions.append({"tex": segment["tex"], "display": False})
                    targets.append(segment)
        for item in block.get("items", []):
            for segment in item.get("segments", []):
                if isinstance(segment, dict) and "tex" in segment:
                    expressions.append({"tex": segment["tex"], "display": False})
                    targets.append(segment)
        for row in block.get("rows", []):
            for cell in row:
                for segment in cell.get("segments", []):
                    if isinstance(segment, dict) and "tex" in segment:
                        expressions.append({"tex": segment["tex"], "display": False})
                        targets.append(segment)
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
        if re.fullmatch(r"\\boldsymbol\{\\mathsf\{[A-Za-z]\}\}", target["tex"]):
            markup = markup.replace('mathvariant="sans-serif"', 'mathvariant="bold-sans-serif"')
        target["mathml"] = markup


def render_chapter(number: int | str, source: Path, page_range: tuple[int, int]) -> dict:
    raw = source.read_text(encoding="utf-8")
    if re.search(r"\b(?:TODO|TBD)\b|待补|此处略", raw, re.IGNORECASE):
        raise ValueError(f"Unfinished placeholder in {source}")
    protected, expressions = protect_math(raw)
    rendered = markdown.markdown(protected, extensions=["fenced_code", "tables", "footnotes", "sane_lists"], output_format="html5")
    soup = BeautifulSoup(rendered, "html.parser")
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
            elif str(node).strip() == "join-previous-paragraph-with-space":
                join_next_paragraph = True
                join_space = True
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
                elif number in {"A", "B", "C"}:
                    prefix = f"附录 {number}"
                    if not heading.startswith(prefix):
                        raise ValueError(f"Invalid appendix heading in {source}")
                    toc.append({"number": prefix, "title": heading.removeprefix(prefix).strip(), "block": block_id, "level": level})
                else:
                    expected = {
                        "frontmatter": "封面与出版信息",
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
        elif node.name == "figure":
            image = node.find("img")
            if image is None:
                raise ValueError(f"Figure without image in {source}")
            full_src = image.get("src", "")
            prefix = f"books/{BOOK_ID}/"
            image_dir = (f"chapter-{number:02d}" if isinstance(number, int)
                         else f"appendix-{number.lower()}" if number in {"A", "B", "C"}
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
                     "captionSegments": inline_segments(caption_text, expressions)}
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
                     "segments": inline_segments(content, expressions)}
        if join_next_paragraph:
            if block["kind"] != "paragraph" or not blocks or blocks[-1]["kind"] != "paragraph":
                raise ValueError(f"Paragraph continuation has no paragraph to join in {source}")
            previous = blocks[-1]
            if join_space:
                previous["text"] += " "
                previous["segments"].append(" ")
            previous["text"] += block["text"]
            previous["segments"].extend(block["segments"])
            previous.setdefault("continuedPdfPages", []).append(current_page)
            join_next_paragraph = False
            join_space = False
        else:
            blocks.append(block)

    if join_next_paragraph:
        raise ValueError(f"Paragraph continuation has no following paragraph in {source}")
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


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--chapter", required=True, help="0–20, A, B, C, frontmatter, contents, bibliography, or index")
    args = parser.parse_args()
    key = args.chapter
    number: int | str = int(key) if key.isdigit() else key.upper() if key.upper() in {"A", "B", "C"} else key.lower()
    if isinstance(number, int):
        filename = "preface.md" if number == 0 else f"chapter-{number:02d}.md"
        output_name = f"chapter-{number:02d}.json"
        page_range = (5, 10) if number == 0 else chapter_ranges().get(number)
    elif number in {"A", "B", "C"}:
        filename = f"appendix-{number.lower()}.md"
        output_name = f"appendix-{number.lower()}.json"
        page_range = {"A": (618, 624), "B": (625, 627), "C": (628, 631)}[number]
    elif number in {"frontmatter", "contents", "bibliography", "index"}:
        filename = f"{number}.md"
        output_name = f"{number}.json"
        page_range = {
            "frontmatter": (1, 4), "contents": (11, 20),
            "bibliography": (632, 647), "index": (648, 656),
        }[number]
    else:
        raise SystemExit(f"Unknown chapter/unit: {key}")
    source = BOOK / "chapters" / filename
    if not source.is_file():
        raise SystemExit(f"Missing chapter source: {source}")
    if not page_range:
        raise SystemExit(f"Unknown chapter: {number}")
    chapter = render_chapter(number, source, page_range)
    output = BOOK / output_name
    output.write_text(json.dumps(chapter, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(f"Wrote {output}: {len(chapter['blocks'])} blocks, {len(chapter['images'])} images, {len(chapter['toc'])} headings")


if __name__ == "__main__":
    main()
