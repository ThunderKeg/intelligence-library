"""Build reviewed Sutton/Barto page transcriptions as structured reader chapters.

This script only reads translated page sources and writes the selected chapter JSON.
It does not register chapters or mark editorial review as complete.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BOOK = ROOT / "books" / "sutton-barto-reinforcement-learning-2e"
RANGES = {3: (47, 72), 4: (73, 90), 5: (91, 118), 6: (119, 140), 7: (141, 158), 8: (159, 194), 9: (197, 242), 10: (243, 256), 11: (257, 286), 12: (287, 320), 13: (321, 338), 14: (341, 376), 15: (377, 420), 16: (421, 458), 17: (459, 480)}
HEADING = re.compile(r"^(#{1,3})\s+(.+)$", re.S)
IMAGE = re.compile(r"^!\[([^]]*)\]\((?:\.\./\.\./)?(assets/[\w./-]+)\)$")
DISPLAY = re.compile(r"^\\\[\s*(.*?)\s*\\\]$", re.S)
DISPLAY_DOLLAR = re.compile(r"^\$\$\s*(.*?)\s*\$\$$", re.S)
NUMBERED = re.compile(r"^公式(?:（(\d+\.\d+)）)?：\s*(.*)$", re.S)
INLINE_TOKEN = re.compile(r"\\\((.*?)\\\)|\*\*(.+?)\*\*|`([^`\n]+)`|(?<!\*)\*([^*\n]+)\*(?!\*)", re.S)
MATH_TOKEN = re.compile(r"\\\((.*?)\\\)", re.S)
EXERCISE = re.compile(r"^\*\*([∗＊*]?习题\s*\d+\.\d+.*?)\*\*\s*(.*)$", re.S)
FOOTNOTE = re.compile(r"^(脚注\s*\d+[：:])\s*(.*)$", re.S)
BIBLIO = re.compile(r"^\*\*(\d+(?:\.\d+)+(?:[–-]\d+(?:\.\d+)*)?)\*\*\s*(.*)$", re.S)
TAG = re.compile(r"\\tag\{(\d+\.\d+)\}")
FIGURE_CAPTION = re.compile(r"^(?:\*\*(图\s*\d+\.\d+)[：:]?\*\*|(图\s*\d+\.\d+)[：:])\s*(.*)$", re.S)
FIGURE_ANNOTATION = re.compile(r"^(?:\*\*)?图内文字译注[：:](?:\*\*)?\s*(.*)$", re.S)


def chunks(source: str) -> list[str]:
    source = re.sub(r"<!--.*?-->", "", source, flags=re.S)
    # Markdown allows blank lines inside fenced code. Keep each entire fence as
    # one chunk before splitting the surrounding prose into paragraphs.
    fence = re.compile(r"^```[^\n]*\n.*?^```[ \t]*$", re.M | re.S)
    result: list[str] = []
    cursor = 0
    for match in fence.finditer(source):
        result.extend(chunk.strip(" \t\r\n") for chunk in re.split(r"\n\s*\n", source[cursor:match.start()]) if chunk.strip())
        result.append(match.group().strip())
        cursor = match.end()
    result.extend(chunk.strip(" \t\r\n") for chunk in re.split(r"\n\s*\n", source[cursor:]) if chunk.strip())
    if any(chunk.count("```") % 2 for chunk in result):
        raise ValueError("Unclosed Markdown code fence")
    return result


def table_cells(line: str) -> list[str]:
    if not line.startswith("|") or not line.endswith("|"):
        raise ValueError(f"Malformed table row: {line[:80]}")
    return [cell.strip().replace(r"\|", "|") for cell in re.split(r"(?<!\\)\|", line[1:-1])]


def parse_table(chunk: str) -> dict:
    lines = chunk.splitlines()
    if len(lines) < 2 or not re.fullmatch(r"[\s|:-]+", lines[1]):
        raise ValueError(f"Malformed Markdown table: {chunk[:80]}")
    headers = table_cells(lines[0])
    rows = [table_cells(line) for line in lines[2:]]
    if any(len(row) != len(headers) for row in rows):
        raise ValueError(f"Inconsistent table width: {chunk[:80]}")
    return {"kind": "table", "headers": headers, "rows": rows}


def parse_ordered_list(chunk: str) -> dict:
    items: list[dict] = []
    ancestors: dict[int, dict] = {}
    for line in chunk.splitlines():
        match = re.fullmatch(r"(\s*)(\d+)\.\s+(.+)", line)
        if not match:
            raise ValueError(f"Malformed ordered list line: {line[:80]}")
        depth = len(match[1]) // 3
        item = {"text": match[3]}
        if depth == 0:
            items.append(item)
        else:
            parent = ancestors.get(depth - 1)
            if parent is None:
                raise ValueError(f"Ordered list skips nesting level: {line[:80]}")
            parent.setdefault("children", []).append(item)
            parent["ordered"] = True
        ancestors[depth] = item
        for deeper in tuple(key for key in ancestors if key > depth):
            del ancestors[deeper]
    return {"kind": "list", "ordered": True, "items": items}


def parse_page(page: int, chapter: int, blocks: list[dict]) -> None:
    path = BOOK / "translation" / f"chapter-{chapter:02d}" / f"page-{page:02d}.md"
    if not path.exists():
        raise ValueError(f"Missing source page: {path}")
    source = path.read_text(encoding="utf-8")
    if not source.strip():
        raise ValueError(f"Empty source page: {path}")
    sequence = 0
    for chunk in chunks(source):
        markers = {":::algorithm", ":::end-algorithm", ":::source-box", ":::end-source-box"}
        if not chunk.startswith("```") and any(re.search(rf"(?m)^{re.escape(marker)}$", chunk) for marker in markers) and chunk not in markers:
            raise ValueError(f"Box marker needs a blank line on page {page}: {chunk[:80]}")
        trailing = None
        heading = HEADING.fullmatch(chunk)
        image = IMAGE.fullmatch(chunk)
        display = DISPLAY.fullmatch(chunk) or DISPLAY_DOLLAR.fullmatch(chunk)
        numbered = NUMBERED.fullmatch(chunk)
        exercise = EXERCISE.fullmatch(chunk)
        footnote = FOOTNOTE.fullmatch(chunk)
        biblio = BIBLIO.fullmatch(chunk)
        caption = FIGURE_CAPTION.fullmatch(chunk)
        annotation = FIGURE_ANNOTATION.fullmatch(chunk)
        if chunk in {":::algorithm", ":::end-algorithm", ":::source-box", ":::end-source-box"}:
            block = {"kind": "box-marker", "marker": chunk}
        elif heading:
            block = {"kind": "heading", "level": len(heading[1]), "text": heading[2]}
        elif chunk.startswith("> 导读："):
            block = {"kind": "intro", "text": chunk[2:].replace("\n", " ")}
        elif chunk.startswith("> "):
            block = {"kind": "quote", "text": re.sub(r"(?m)^> ?", "", chunk).replace("\n", " ")}
        elif image:
            if not (BOOK / image[2]).is_file():
                raise ValueError(f"Image missing on page {page}: {image[2]}")
            block = {"kind": "figure", "src": image[2], "alt": image[1], "wide": True}
        elif caption and blocks and blocks[-1]["kind"] == "figure" and blocks[-1]["page"] == page:
            block = blocks[-1]
            content = (caption[1] or caption[2]) + "：" + caption[3].replace("\n", " ")
            main, separator, annotation = content.partition("图内文字译注：")
            block["caption"] = main.strip()
            if separator:
                block["annotations"] = [s.strip() for s in annotation.split("；") if s.strip()]
            continue
        elif chunk.startswith("图注：") and blocks and blocks[-1]["kind"] == "figure":
            blocks[-1]["caption"] = chunk.removeprefix("图注：").replace("\n", " ")
            continue
        elif annotation:
            if not blocks or blocks[-1]["kind"] != "figure":
                raise ValueError(f"Figure annotation not adjacent to figure on page {page}")
            blocks[-1]["annotations"] = [s.strip() for s in annotation[1].split("；") if s.strip()]
            continue
        elif display:
            tex = display[1].strip()
            match = TAG.search(tex)
            number = match[1] if match else None
            if match:
                tex = TAG.sub("", tex).strip()
            block = {"kind": "formula", "tex": tex, "text": tex}
            if number:
                block["number"] = number
        elif numbered:
            expression = numbered[2].strip().rstrip("。")
            math = re.fullmatch(r"\\\((.*?)\\\)(.*)", expression, re.S)
            if not math:
                math = re.fullmatch(r"\\\[(.*?)\\\](.*)", expression, re.S)
            if not math:
                raise ValueError(f"Numbered formula lacks TeX on page {page}: {expression[:80]}")
            tex = math[1]
            tag = TAG.search(tex)
            if tag and numbered[1] and tag[1] != numbered[1]:
                raise ValueError(f"Conflicting equation number on page {page}: {numbered[1]} != {tag[1]}")
            if tag:
                tex = TAG.sub("", tex).strip()
            block = {"kind": "formula", "tex": tex, "text": tex}
            trailing = math[2].strip()
            if numbered[1] or tag:
                block["number"] = numbered[1] or tag[1]
        elif chunk.startswith("```" ) and chunk.endswith("```"):
            first, rest = chunk.split("\n", 1)
            block = {"kind": "code", "language": first[3:] or "text", "text": rest.rsplit("\n```", 1)[0]}
        elif chunk.startswith("|"):
            block = parse_table(chunk)
        elif re.match(r"^\d+\.\s", chunk):
            block = parse_ordered_list(chunk)
        elif exercise:
            block = {"kind": "exercise", "label": exercise[1], "text": exercise[2].replace("\n", " ")}
        elif footnote:
            block = {"kind": "footnote", "label": footnote[1], "text": footnote[2].replace("\n", " ")}
        elif biblio:
            block = {"kind": "bibliographical-note", "label": biblio[1], "text": biblio[2].replace("\n", " ")}
        elif chunk.startswith("**") and chunk.endswith("**"):
            block = {"kind": "heading", "level": 3, "text": chunk.strip("*")}
        elif re.fullmatch(r"(?:[-*] .+\n?)+", chunk):
            block = {"kind": "list", "items": [{"text": line[2:]} for line in chunk.splitlines()]}
        else:
            previous = blocks[-1] if blocks else None
            if previous and previous["kind"] in {"bibliographical-note", "bibliographical-note-continuation"}:
                block = {"kind": "bibliographical-note-continuation", "label": previous["label"], "text": chunk.replace("\n", " ")}
            else:
                block = {"kind": "paragraph", "text": chunk.replace("\n", " ")}
        sequence += 1
        block["page"] = page
        block["id"] = f"p{page}-b{sequence:02d}"
        blocks.append(block)
        if trailing:
            sequence += 1
            blocks.append({"kind": "paragraph", "text": trailing, "page": page, "id": f"p{page}-b{sequence:02d}"})


def enrich_math(blocks: list[dict]) -> None:
    expressions: list[tuple[str, bool]] = []
    def math_tokens(value: str) -> list[tuple[str, bool]]:
        # Math may sit inside Markdown emphasis, such as **GTD(\(\lambda\))**.
        return [(match[1], False) for match in MATH_TOKEN.finditer(value)]

    def list_items(items: list) -> list[dict]:
        return [nested for item in items for nested in [item, *list_items(item.get("children", []))]]

    for block in blocks:
        if block["kind"] == "formula":
            expressions.append((block["tex"], True))
        for field in ("text", "label", "caption"):
            if field not in block or block["kind"] == "formula":
                continue
            expressions.extend(math_tokens(block[field]))
        for field in ("annotations", "headers"):
            for value in block.get(field, []):
                expressions.extend(math_tokens(value))
        for row in block.get("rows", []):
            for value in row:
                expressions.extend(math_tokens(value))
        for item in list_items(block.get("items", [])):
            expressions.extend(math_tokens(item["text"]))
    unique = list(dict.fromkeys(expressions))
    result = subprocess.run(
        ["node", str(ROOT / "scripts" / "tex_to_mathml.js")],
        input=json.dumps([{"tex": tex, "display": display} for tex, display in unique]),
        text=True, encoding="utf-8", capture_output=True, check=True,
    )
    rendered = json.loads(result.stdout)
    if len(rendered) != len(unique):
        raise ValueError("MathML conversion count mismatch")
    math = dict(zip(unique, rendered, strict=True))

    def decorate(value: str) -> tuple[str, list | None]:
        segments: list = []
        start = 0
        for match in INLINE_TOKEN.finditer(value):
            if match.start() > start:
                segments.append(value[start:match.start()])
            if match[1] is not None:
                segments.append({"mathml": math[(match[1], False)], "tex": match[1], "text": match[1]})
            elif match[2] is not None:
                inner, nested = decorate(match[2])
                segment = {"strong": True, "text": inner}
                if nested:
                    segment["segments"] = nested
                segments.append(segment)
            elif match[3] is not None:
                segments.append({"code": True, "text": match[3]})
            else:
                inner, nested = decorate(match[4])
                segment = {"em": True, "text": inner}
                if nested:
                    segment["segments"] = nested
                segments.append(segment)
            start = match.end()
        if not segments:
            return value, None
        if start < len(value):
            segments.append(value[start:])
        plain = "".join(part if isinstance(part, str) else part.get("text", "") for part in segments)
        return plain, segments

    for block in blocks:
        if block["kind"] == "formula":
            block["mathml"] = math[(block.pop("tex"), True)]
            continue
        for field in ("text", "caption"):
            if field in block:
                block[field], segments = decorate(block[field])
                if segments:
                    block[field + "Segments" if field == "caption" else "segments"] = segments
        for field in ("annotations", "headers"):
            if field in block:
                value_segments = []
                values = []
                for value in block[field]:
                    plain, segments = decorate(value)
                    values.append(plain)
                    value_segments.append(segments)
                block[field] = values
                if field == "annotations":
                    block["annotationSegments"] = value_segments
                elif any(value_segments):
                    block["headers"] = [{"text": value, "segments": seg} if seg else value for value, seg in zip(values, value_segments, strict=True)]
        if "rows" in block:
            rows = []
            for row in block["rows"]:
                cells = []
                for cell in row:
                    plain, segments = decorate(cell)
                    cells.append({"text": plain, "segments": segments} if segments else plain)
                rows.append(cells)
            block["rows"] = rows
        for item in list_items(block.get("items", [])):
            item["text"], segments = decorate(item["text"])
            if segments:
                item["segments"] = segments


def box_algorithms(blocks: list[dict]) -> list[dict]:
    output = []
    index = 0
    while index < len(blocks):
        block = blocks[index]
        if block["kind"] == "box-marker" and block["marker"] in {":::algorithm", ":::source-box"}:
            algorithm = block["marker"] == ":::algorithm"
            terminator = ":::end-algorithm" if algorithm else ":::end-source-box"
            closing = next((i for i in range(index + 1, len(blocks)) if blocks[i]["kind"] == "box-marker" and blocks[i]["marker"] == terminator), None)
            if closing is None or closing == index + 1:
                raise ValueError(f"Unclosed or empty source box at {block['id']}")
            if any(child["kind"] == "box-marker" for child in blocks[index + 1:closing]):
                raise ValueError(f"Nested source box at {block['id']}")
            output.append({"kind": "box", "algorithm": algorithm, "outlined": not algorithm, "id": block["id"] + "-box", "page": block["page"], "blocks": blocks[index + 1:closing]})
            index = closing + 1
        elif block["kind"] == "box-marker":
            raise ValueError(f"Unexpected source box close at {block['id']}")
        elif block["kind"] == "heading" and block["level"] == 3 and index + 1 < len(blocks) and blocks[index + 1]["kind"] in {"code", "list"}:
            output.append({"kind": "box", "id": block["id"] + "-box", "page": block["page"], "blocks": [block, blocks[index + 1]]})
            index += 2
        else:
            output.append(block)
            index += 1
    return output


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("chapter", type=int, choices=RANGES)
    args = parser.parse_args()
    chapter = args.chapter
    first, last = RANGES[chapter]
    blocks: list[dict] = []
    for page in range(first, last + 1):
        parse_page(page, chapter, blocks)
    enrich_math(blocks)
    title = next((block["text"] for block in blocks if block["kind"] == "heading" and block["level"] == 1), None)
    if not title:
        raise ValueError("Missing chapter title")
    toc = []
    for block in blocks:
        if block["kind"] != "heading" or block["level"] not in (1, 2, 3):
            continue
        match = re.match(r"^(\d+(?:\.\d+)+)(?![\d.])", block["text"])
        if block["level"] != 1 and match is None:
            continue
        entry = {"number": str(chapter) if block["level"] == 1 else match[1],
                 "title": block["text"] if block["level"] == 1 else block["text"][len(match[1]):].strip(),
                 "block": block["id"], "level": block["level"]}
        if "segments" in block:
            entry["segments"] = block["segments"]
        toc.append(entry)
    nested = box_algorithms(blocks)
    output = BOOK / f"chapter-{chapter:02d}.json"
    output.write_text(json.dumps({"bookId": BOOK.name, "title": title, "toc": toc, "blocks": nested}, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(f"Wrote {output}: {len(blocks)} blocks, {len(toc)} TOC entries, {sum(b['kind']=='formula' for b in blocks)} displayed formulas")


if __name__ == "__main__":
    main()
