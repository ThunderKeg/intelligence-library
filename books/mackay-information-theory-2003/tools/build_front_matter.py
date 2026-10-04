"""Compile the reviewed MacKay front matter into an unpublished reader draft."""

import importlib.util
import json
import re
from pathlib import Path


BOOK = Path(__file__).resolve().parents[1]
PARSER = Path(__file__).with_name("build_chapter_01.py")
spec = importlib.util.spec_from_file_location("mackay_chapter_builder", PARSER)
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)
OUTPUT = BOOK / "chapter-00.draft.json"
IMAGE = re.compile(r"^assets/([\w.-]+\.(?:png|jpg|svg|webp))$")
ROADMAP_ENTRY = re.compile(r"(?<!\d)(\d{1,2}) [^；。？]+[；。？]")


def keep_roadmap_terms_together(blocks):
    """Wrap roadmap labels between chapters without changing their text."""
    protected = 0
    for block in blocks:
        if block["kind"] != "list" or block["pdfPage"] not in range(6, 11):
            continue
        for item in block["items"]:
            text = item["text"]
            matches = list(ROADMAP_ENTRY.finditer(text))
            if not matches:
                continue
            if item["segments"] != [text]:
                raise ValueError(f"Unexpected rich roadmap list: {block['id']}")
            segments = []
            cursor = 0
            for match in matches:
                if cursor < match.start():
                    segments.append({"text": text[cursor:match.start()], "nowrap": True})
                    segments.append({"break": True})
                if match[1] == "21":
                    first = "21 通过完全枚举"
                    second = "进行精确推断" + match[0][-1]
                    if match[0] != first + second:
                        raise ValueError(f"Unexpected Chapter 21 label: {match[0]}")
                    segments.extend(({"text": first, "nowrap": True},
                                     {"break": True},
                                     {"text": second, "nowrap": True}))
                else:
                    segments.append({"text": match[0], "nowrap": True})
                segments.append({"break": True})
                cursor = match.end()
                protected += 1
            if cursor < len(text):
                segments.append(text[cursor:])
            if "".join(segment if isinstance(segment, str) else segment.get("text", "")
                       for segment in segments) != text:
                raise ValueError(f"Roadmap text changed: {block['id']}")
            item["segments"] = segments
    if protected != 320:
        raise ValueError(f"Expected 320 roadmap chapter labels, got {protected}")


def front_image(source: str) -> str:
    match = IMAGE.fullmatch(source)
    if not match:
        raise ValueError(f"Unexpected front-matter image path: {source}")
    path = BOOK / "assets" / "front-matter" / match.group(1)
    if not path.is_file():
        raise FileNotFoundError(path)
    return f"assets/front-matter/{match.group(1)}"


def main():
    blocks = [
        block
        for page in range(1, 15)
        for block in builder.compile_page(
            page,
            source=BOOK / "front-matter" / f"page-{page:02d}.md",
            image_resolver=front_image,
            chapter_start=1,
        )
    ]
    for block in blocks:
        if block["kind"] == "figure" and block["pdfPage"] in (6, 7, 8, 9, 10, 13, 14):
            block["wide"] = True
    if not blocks or blocks[0]["kind"] != "heading":
        raise ValueError("Front matter title missing")
    numbers = [block["number"] for block in blocks if block["kind"] == "formula"]
    if numbers != [f"(1.{n})" for n in range(1, 18)]:
        raise ValueError(f"Front matter formula numbers: {numbers}")
    builder.compile_math(blocks)
    keep_roadmap_terms_together(blocks)
    section_pages = [(1, "题名"), (3, "目录"), (5, "前言"), (13, "关于第 1 章")]
    toc = [
        {"number": "前置" if page == 1 else str(page), "title": title,
         "block": next(block["id"] for block in blocks if block["pdfPage"] == page)}
        for page, title in section_pages
    ]
    result = {"schemaVersion": 2, "bookId": "mackay-information-theory-2003",
              "title": "前言与第一章预备知识", "sourcePdfPages": [1, 14],
              "toc": toc, "blocks": blocks}
    OUTPUT.write_text(json.dumps(result, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(f"Wrote {OUTPUT}: {len(blocks)} blocks, {len(numbers)} formulas, "
          f"{sum(block['kind'] == 'figure' for block in blocks)} figures")


if __name__ == "__main__":
    main()
