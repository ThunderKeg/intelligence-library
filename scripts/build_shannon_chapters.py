"""Compile the checked Shannon Markdown into the reader's static chapter JSON."""

from __future__ import annotations

import json
import re
import struct
import subprocess
from pathlib import Path

import markdown
from bs4 import BeautifulSoup, Comment, NavigableString, Tag


ROOT = Path(__file__).resolve().parents[1]
BOOK_ID = "shannon-mathematical-theory-1948"
BOOK = ROOT / "books" / BOOK_ID
MATH_CONVERTER = ROOT / "scripts" / "tex_to_mathml.js"
PAGE_MARKER = re.compile(r"pdf-page:\s*(\d+)")
DISPLAY_MATH = re.compile(r"(?<!\\)\$\$(.+?)(?<!\\)\$\$", re.DOTALL)
INLINE_MATH = re.compile(r"(?<!\\)\$(?!\$)(.+?)(?<!\\)\$", re.DOTALL)
MATH_TOKEN = re.compile(r"SHANNONMATH(?:DISPLAY|INLINE)\d{6}")
SECTION_NUMBER = re.compile(r"^(\d+)\.\s*(.+)$")
APPENDIX_NUMBER = re.compile(r"^附录\s*(\d+)(?:[：:]\s*|\s+)?(.*)$")

# The overlapping page at each Part boundary belongs to whichever heading follows it.
CHAPTERS = [
    ("00", "chapter-00.md", 1, 3, "序", "引言"),
    ("01", "chapter-01.md", 3, 19, "I", "无噪离散系统"),
    ("02", "chapter-02.md", 19, 28, "II", "有噪离散信道"),
    ("a1-a4", "appendix-1-4.md", 28, 31, "附录 1—4", "附录 1—4"),
    ("03", "chapter-03.md", 32, 41, "III", "数学预备知识"),
    ("04", "chapter-04.md", 41, 47, "IV", "连续信道"),
    ("05", "chapter-05.md", 47, 51, "V", "连续信源的速率"),
    ("a5-a7", "appendix-5-7.md", 52, 55, "附录 5—7", "附录 5—7"),
]


def protect_math(raw: str) -> tuple[str, dict[str, tuple[str, bool]]]:
    expressions: dict[str, tuple[str, bool]] = {}

    def replace_display(match: re.Match[str]) -> str:
        token = f"SHANNONMATHDISPLAY{len(expressions):06d}"
        expressions[token] = (match.group(1).strip(), True)
        return token

    def replace_inline(match: re.Match[str]) -> str:
        token = f"SHANNONMATHINLINE{len(expressions):06d}"
        expressions[token] = (match.group(1).strip(), False)
        return token

    return INLINE_MATH.sub(replace_inline, DISPLAY_MATH.sub(replace_display, raw)), expressions


def compile_math(expressions: dict[str, tuple[str, bool]]) -> dict[str, str]:
    if not expressions:
        return {}
    payload = [{"tex": tex, "display": display} for tex, display in expressions.values()]
    result = subprocess.run(
        ["node", str(MATH_CONVERTER)],
        input=json.dumps(payload, ensure_ascii=False),
        text=True,
        encoding="utf-8",
        capture_output=True,
        check=False,
    )
    if result.returncode:
        raise ValueError(f"KaTeX conversion failed: {result.stderr.strip()}")
    values = json.loads(result.stdout)
    if len(values) != len(expressions):
        raise ValueError("MathML expression count differs from source TeX count")
    return dict(zip(expressions, values))


def insert_math(soup: BeautifulSoup, expressions: dict[str, tuple[str, bool]], mathml: dict[str, str]) -> None:
    for node in list(soup.find_all(string=True)):
        if isinstance(node, Comment):
            continue
        matches = list(MATH_TOKEN.finditer(str(node)))
        if not matches:
            continue
        value = str(node)
        if any(expressions[match.group()][1] for match in matches):
            if len(matches) != 1 or value.strip() != matches[0].group():
                raise ValueError(f"Display equation shares a paragraph with text: {value[:100]}")
            token = matches[0].group()
            tex, _ = expressions[token]
            wrapper = soup.new_tag("div", attrs={"class": "book-formula"})
            math = BeautifulSoup(mathml[token], "html.parser").math
            if math is None:
                raise ValueError(f"MathML missing math root: {tex[:80]}")
            math["display"] = "block"
            math["data-tex"] = tex
            wrapper.append(math)
            if node.parent.name == "p" and node.parent.get_text(strip=True) == token:
                node.parent.replace_with(wrapper)
            else:
                node.replace_with(wrapper)
            continue
        last = 0
        for match in matches:
            if match.start() > last:
                node.insert_before(NavigableString(value[last:match.start()]))
            token = match.group()
            tex, _ = expressions[token]
            math = BeautifulSoup(mathml[token], "html.parser").math
            if math is None:
                raise ValueError(f"MathML missing math root: {tex[:80]}")
            math["display"] = "inline"
            math["data-tex"] = tex
            node.insert_before(math)
            last = match.end()
        if last < len(value):
            node.insert_before(NavigableString(value[last:]))
        node.extract()


def validate_and_style(soup: BeautifulSoup, *, allow_code: bool) -> list[str]:
    images: list[str] = []
    if soup.find(["script", "style", "iframe", "object", "embed"]):
        raise ValueError("Unsupported active HTML in source")
    for tag in soup.find_all(True):
        if any(key.lower().startswith("on") for key in tag.attrs):
            raise ValueError(f"HTML event attribute on <{tag.name}>")
        if tag.name in ("ol", "ul"):
            tag["class"] = list(dict.fromkeys([*tag.get("class", []), "book-list"]))
        elif tag.name == "pre":
            if not allow_code:
                raise ValueError("Unexpected code block; check Markdown indentation against the PDF")
            tag["class"] = list(dict.fromkeys([*tag.get("class", []), "book-code"]))
        elif tag.name == "figure":
            tag["class"] = list(dict.fromkeys([*tag.get("class", []), "book-figure"]))
        elif tag.name == "figcaption":
            tag["class"] = list(dict.fromkeys([*tag.get("class", []), "figure-caption"]))
        elif tag.name == "table":
            tag["class"] = list(dict.fromkeys([*tag.get("class", []), "book-table"]))
            wrapper = soup.new_tag("div", attrs={"class": "table-scroll"})
            tag.wrap(wrapper)
        if tag.name == "img":
            src = tag.get("src", "")
            prefix = f"books/{BOOK_ID}/assets/"
            if not src.startswith(prefix) or ".." in Path(src).parts or not (ROOT / src).is_file():
                raise ValueError(f"Missing or invalid image: {src}")
            if not tag.get("alt", "").strip():
                raise ValueError(f"Missing image alt text: {src}")
            header = (ROOT / src).read_bytes()[:24]
            if not header.startswith(b"\x89PNG\r\n\x1a\n"):
                raise ValueError(f"Unexpected image format: {src}")
            width, height = struct.unpack(">II", header[16:24])
            tag["width"] = width
            tag["height"] = height
            tag["style"] = f"width:{width}px;max-width:100%;height:auto;aspect-ratio:{width}/{height}"
            tag["loading"] = "lazy"
            tag["decoding"] = "async"
            images.append(src)
        if tag.name == "a" and tag.get("href", "").lower().startswith("javascript:"):
            raise ValueError("Unsafe link in source")
    return sorted(set(images))


def heading_info(text: str, level: int, chapter_number: str) -> tuple[str, str]:
    if level == 1:
        return chapter_number, text
    if match := SECTION_NUMBER.match(text):
        return match.group(1), match.group(2)
    if match := APPENDIX_NUMBER.match(text):
        return f"附录 {match.group(1)}", match.group(2).strip()
    return "", text


def compile_chapter(chapter: tuple[str, str, int, int, str, str]) -> dict:
    chapter_id, source_name, first_page, last_page, chapter_number, title = chapter
    source = BOOK / source_name
    raw = source.read_text(encoding="utf-8")
    if re.search(r"\b(?:TODO|TBD)\b|待补|此处略", raw, re.IGNORECASE):
        raise ValueError(f"Unfinished placeholder in {source}")
    page_markers = [int(value) for value in PAGE_MARKER.findall(raw)]
    if not page_markers or page_markers[0] != first_page:
        raise ValueError(f"First PDF page marker must be {first_page} in {source}")
    if page_markers != sorted(page_markers) or set(page_markers) != set(range(first_page, last_page + 1)):
        raise ValueError(f"Missing or out-of-order PDF page markers in {source}: {page_markers}")
    protected, expressions = protect_math(raw)
    html = markdown.markdown(
        protected,
        extensions=["fenced_code", "tables", "footnotes", "sane_lists"],
        output_format="html5",
    )
    soup = BeautifulSoup(html, "html.parser")
    insert_math(soup, expressions, compile_math(expressions))
    images = validate_and_style(soup, allow_code=chapter_id == "01")
    if soup.find(string=MATH_TOKEN):
        raise ValueError(f"Unresolved math token in {source}")

    current_page = first_page
    counters: dict[int, int] = {}
    blocks: list[dict] = []
    toc: list[dict] = []
    for node in soup.contents:
        if isinstance(node, Comment):
            if match := PAGE_MARKER.search(str(node)):
                current_page = int(match.group(1))
            continue
        if isinstance(node, NavigableString):
            if node.strip():
                raise ValueError(f"Unwrapped text in {source}: {str(node)[:80]}")
            continue
        if not isinstance(node, Tag):
            continue
        counters[current_page] = counters.get(current_page, 0) + 1
        block_id = f"p{current_page - first_page + 1:02d}-b{counters[current_page]:03d}"
        common = {"id": block_id, "page": current_page - first_page + 1, "pdfPage": current_page}
        if node.name in ("h1", "h2", "h3"):
            level = int(node.name[1])
            value = node.get_text(" ", strip=True)
            block = {**common, "kind": "heading", "level": level, "text": value}
            if node.find("math"):
                block["html"] = str(node)
            number, heading_title = heading_info(value, level, chapter_number)
            if chapter_id == "a1-a4" and number == "附录 2":
                heading_title = "熵公式的推导"
            toc.append({"number": number, "title": heading_title, "level": level, "block": block_id})
        elif node.name == "aside" and "chapter-guide" in node.get("class", []):
            block = {**common, "kind": "intro", "text": node.get_text(" ", strip=True)}
        else:
            block = {**common, "kind": "rich", "html": str(node), "text": node.get_text(" ", strip=True)}
        blocks.append(block)
        for comment in node.find_all(string=lambda value: isinstance(value, Comment)):
            if match := PAGE_MARKER.search(str(comment)):
                current_page = int(match.group(1))

    if not blocks or not toc or toc[0]["level"] != 1:
        raise ValueError(f"Missing content or top-level heading in {source}")
    if any(MATH_TOKEN.search(block.get("html", "")) for block in blocks):
        raise ValueError(f"Unresolved math token in {source}")
    return {
        "schemaVersion": 3,
        "bookId": BOOK_ID,
        "chapterId": chapter_id,
        "title": title,
        "sourcePdfPages": [first_page, last_page],
        "toc": toc,
        "images": images,
        "blocks": blocks,
    }


def main() -> None:
    for chapter in CHAPTERS:
        document = compile_chapter(chapter)
        output = BOOK / f"chapter-{chapter[0]}.json"
        output.write_text(json.dumps(document, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
        print(f"{output.relative_to(ROOT)}: {len(document['blocks'])} blocks, {len(document['images'])} images, {len(document['toc'])} headings")


if __name__ == "__main__":
    main()
