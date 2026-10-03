"""Bundle the reviewed, page-aligned Chinese front matter for the reader."""

import json
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BOOK = ROOT / "books" / "sutton-barto-reinforcement-learning-2e"
SOURCE = BOOK / "frontmatter"
OUTPUT = BOOK / "chapter-00.json"
HEADING = re.compile(r"^(#{1,3})\s+(.+)$")
IMAGE = re.compile(r"^!\[([^]]*)\]\((assets/[\w./-]+)\)$")
INLINE_MATH = re.compile(r"\\\((.+?)\\\)")
math_pending = []


def marked_text(source: str):
    """Keep inline math and the original preface emphasis as structured segments."""
    segments = []
    position = 0
    for match in INLINE_MATH.finditer(source):
        if match.start() > position:
            segments.append(source[position:match.start()])
        segment = {"tex": match[1], "text": match[1]}
        math_pending.append(segment)
        segments.append(segment)
        position = match.end()
    if position < len(source):
        segments.append(source[position:])
    if not segments:
        segments = [source]
    expanded = []
    for segment in segments:
        if isinstance(segment, str) and "*想要*" in segment:
            before, after = segment.split("*想要*", 1)
            expanded.extend([before, {"em": True, "text": "想要"}, after])
        else:
            expanded.append(segment)
    if not any(isinstance(item, dict) for item in expanded):
        return source
    return {"text": INLINE_MATH.sub(lambda match: match[1], source).replace("*想要*", "想要"), "segments": expanded}


def table_cells(line: str) -> list[str]:
    """Split Markdown cells while preserving escaped vertical bars in notation."""
    if not line.startswith("|") or not line.endswith("|"):
        raise ValueError(f"Malformed notation row: {line}")
    return [cell.strip().replace(r"\|", "|") for cell in re.split(r"(?<!\\)\|", line[1:-1])]


def table_block(chunk: str) -> dict:
    lines = chunk.splitlines()
    if len(lines) < 3 or not re.fullmatch(r"\|(?:\s*:?-+:?\s*\|)+", lines[1]):
        raise ValueError(f"Malformed notation table: {chunk[:90]}")
    headers = [marked_text(cell) for cell in table_cells(lines[0])]
    rows = [[marked_text(cell) for cell in table_cells(line)] for line in lines[2:]]
    if any(len(row) != len(headers) for row in rows):
        raise ValueError(f"Notation table row width differs from header: {chunk[:90]}")
    return {"kind": "table", "notation": True, "headers": headers, "rows": rows}


def append_list_lines(items: list, chunk: str) -> None:
    for line in chunk.splitlines():
        match = re.fullmatch(r"(\s*)-\s+(.+)", line)
        if not match:
            raise ValueError(f"Malformed contents list line: {line}")
        depth = len(match[1]) // 2
        if depth not in (0, 1) or len(match[1]) != depth * 2:
            raise ValueError(f"Unsupported contents indentation: {line}")
        item = marked_text(match[2])
        if depth == 0:
            items.append(item)
        else:
            if not items:
                raise ValueError(f"Subsection without parent: {line}")
            parent = items[-1]
            if isinstance(parent, str):
                parent = {"text": parent}
                items[-1] = parent
            parent.setdefault("children", []).append(item)


blocks = []
heading_ids = {}
empty_pages = []
for page in range(1, 23):
    source = SOURCE / f"page-{page:02d}.md"
    if not source.exists():
        raise SystemExit(f"Missing front-matter page: {source}")
    chunks = [part.strip() for part in re.split(r"\n\s*\n", source.read_text(encoding="utf-8")) if part.strip()]
    if not chunks:
        empty_pages.append(page)
        continue
    count = 0
    for chunk in chunks:
        if chunk.startswith("<!--"):
            continue
        heading = HEADING.fullmatch(chunk)
        image = IMAGE.fullmatch(chunk)
        if heading:
            block = {"kind": "heading", "text": heading[2], "level": len(heading[1])}
            if heading[2] not in heading_ids:
                heading_ids[heading[2]] = f"f{page:02d}-t{count + 1:02d}"
        elif image:
            block = {"kind": "figure", "alt": image[1], "src": image[2]}
        elif chunk.startswith("封面文字译注："):
            if not blocks or blocks[-1]["kind"] != "figure":
                raise SystemExit("Cover annotation must follow the cover image")
            blocks[-1]["annotations"] = [item.strip() for item in chunk.removeprefix("封面文字译注：").split("；") if item.strip()]
            continue
        elif chunk.startswith("|"):
            block = table_block(chunk)
        elif re.match(r"^\s*-\s+", chunk):
            if blocks and blocks[-1]["kind"] == "list" and blocks[-1]["page"] == page:
                append_list_lines(blocks[-1]["items"], chunk)
                continue
            block = {"kind": "list", "items": [], "ordered": False}
            append_list_lines(block["items"], chunk)
        else:
            value = marked_text(chunk.replace("\n", " "))
            block = {"kind": "paragraph", **(value if isinstance(value, dict) else {"text": value})}
        count += 1
        block["id"] = f"f{page:02d}-t{count:02d}"
        block["page"] = page
        blocks.append(block)

if empty_pages != [6]:
    raise SystemExit(f"Unexpected blank pages in front matter: {empty_pages}")
if sum(block["kind"] == "figure" for block in blocks) != 1:
    raise SystemExit("Expected one front-matter cover image")
if sum(block["kind"] == "table" for block in blocks) < 4:
    raise SystemExit("Expected notation tables from physical pages 19–22")

if math_pending:
    converted = subprocess.run(
        ["node", str(ROOT / "scripts" / "tex_to_mathml.js")],
        input=json.dumps([{"tex": item["tex"], "display": False} for item in math_pending]),
        text=True,
        encoding="utf-8",
        capture_output=True,
        check=True,
    )
    for item, mathml in zip(math_pending, json.loads(converted.stdout), strict=True):
        item["mathml"] = mathml


section_links = {}
for number in range(1, 18):
    chapter_id = f"{number:02d}"
    chapter_data = json.loads((BOOK / f"chapter-{chapter_id}.json").read_text(encoding="utf-8"))
    for section in chapter_data["toc"]:
        section_number = section.get("number", "")
        if re.fullmatch(r"\d+\.\d+(?:\.\d+)?", section_number):
            section_links[section_number] = (
                f"?book={BOOK.name}&chapter={chapter_id}#read-{section['block']}")


def contents_link(title: str) -> str:
    section = re.match(r"^(\d+\.\d+(?:\.\d+)?)\s", title)
    if section:
        if section[1] not in section_links:
            raise ValueError(f"Original contents section has no reader target: {title}")
        return section_links[section[1]]
    chapter = re.match(r"^(\d{1,2})\s", title)
    if chapter:
        return f"?book={BOOK.name}&chapter={int(chapter[1]):02d}"
    for label, target in (("第一部分", "I"), ("第二部分", "II"), ("第三部分", "III"),
                          ("参考文献", "REF"), ("索引", "IDX")):
        if title.startswith(label):
            return f"?book={BOOK.name}&chapter={target}"
    for label in ("第二版前言", "第一版前言", "记号表"):
        if title.startswith(label):
            return f"#read-{heading_ids[label]}"
    raise ValueError(f"Original contents entry has no reader target: {title}")


contents_links = 0


def link_contents_item(item: str | dict) -> tuple[dict, int]:
    entry = {"text": item} if isinstance(item, str) else item
    entry["href"] = contents_link(entry["text"])
    total = 1
    if entry.get("children"):
        linked_children = []
        for child in entry["children"]:
            linked, count = link_contents_item(child)
            linked_children.append(linked)
            total += count
        entry["children"] = linked_children
    return entry, total


for block in blocks:
    if block["page"] not in range(7, 13):
        continue
    if block["kind"] == "heading" and block["level"] == 2:
        block["href"] = contents_link(block["text"])
        contents_links += 1
    elif block["kind"] == "list":
        linked = []
        for item in block["items"]:
            entry, count = link_contents_item(item)
            linked.append(entry)
            contents_links += count
        block["items"] = linked
if contents_links != 191:
    raise ValueError(f"Expected 191 original contents links, found {contents_links}")

toc = []
for name, number, title in [
    ("强化学习：导论", "封面", "书名与出版信息"),
    ("目录", "目录", "原书目录"),
    ("第二版前言", "前言", "第二版前言"),
    ("第一版前言", "前言", "第一版前言"),
    ("记号表", "记号", "记号表"),
]:
    if name not in heading_ids:
        raise SystemExit(f"Missing front-matter heading: {name}")
    toc.append({"number": number, "title": title, "block": heading_ids[name]})

chapter = {
    "bookId": "sutton-barto-reinforcement-learning-2e",
    "title": "卷首：书名、目录、前言与记号表",
    "toc": toc,
    "blocks": blocks,
    "emptySourcePages": empty_pages,
}
OUTPUT.write_text(json.dumps(chapter, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
print(f"Wrote {OUTPUT}: {len(blocks)} blocks, {sum(block['kind'] == 'table' for block in blocks)} tables")
