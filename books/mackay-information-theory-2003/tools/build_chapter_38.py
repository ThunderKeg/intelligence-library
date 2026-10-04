"""Compile the visually checked MacKay chapter 38 into an unpublished draft."""

import importlib.util
import json
import re
from pathlib import Path


BOOK = Path(__file__).resolve().parents[1]
PARSER = Path(__file__).with_name("build_chapter_01.py")
SPEC = importlib.util.spec_from_file_location("mackay_chapter_builder_38", PARSER)
BUILDER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(BUILDER)
SOURCE = BOOK / "translation" / "chapter-38"
OUTPUT = BOOK / "chapter-38.draft.json"
PAGES = range(480, 483)
HEADING = re.compile(r"^(38\.\d+)\s+(.+)$")


def reject_image(source: str) -> str:
    raise ValueError(f"Source chapter 38 has no image: {source}")


def group_chapter_title(block: dict) -> None:
    parts = ("第 38 章　", "神经网络导论")
    if block["text"] != "".join(parts):
        raise ValueError(f"Chapter 38 title changed unexpectedly: {block['text']}")
    block["html"] = "<h1>" + "".join(
        f'<span class="mackay-ch38-title-part">{part}</span>' for part in parts
    ) + "</h1>"


def main() -> None:
    blocks = [
        block
        for page in PAGES
        for block in BUILDER.compile_page(
            page,
            source=SOURCE / f"pdf-{page}.md",
            image_resolver=reject_image,
            chapter_start=480,
            chapter_number=38,
        )
    ]
    if blocks[0]["kind"] != "heading" or blocks[0]["level"] != 1:
        raise ValueError("Chapter 38 title is missing")
    if blocks[0]["text"] != "第 38 章　神经网络导论":
        raise ValueError("Chapter 38 title changed unexpectedly")
    group_chapter_title(blocks[0])
    if sum(block["kind"] == "intro" for block in blocks) != 1:
        raise ValueError("Chapter 38 needs one clearly marked editor introduction")
    sections = [block for block in blocks
                if block["kind"] == "heading" and block["level"] == 2]
    section_numbers = [HEADING.match(block["text"]).group(1) for block in sections]
    if section_numbers != ["38.1", "38.2"]:
        raise ValueError(f"Chapter 38 sections missing or out of order: {section_numbers}")
    lists = [block for block in blocks if block["kind"] == "list"]
    if len(lists) != 3 or [(block["pdfPage"], block["ordered"], len(block["items"]))
                           for block in lists] != [(480, False, 3), (481, True, 3), (481, True, 3)]:
        raise ValueError("Chapter 38's three lists are missing or malformed")
    nested = lists[2]["items"][1]
    if nested.get("ordered") is not False or len(nested.get("children", [])) != 2:
        raise ValueError("Chapter 38 biological-memory nested bullets are missing")
    if any(block["kind"] in {"formula", "figure", "table", "exercise", "code", "box", "footnote", "quote", "caption"}
           for block in blocks):
        raise ValueError("Source chapter 38 has no formulas, figures, tables, exercises, or other special blocks")
    toc = [{"number": "38", "title": "神经网络导论", "block": blocks[0]["id"]}]
    for block in sections:
        match = HEADING.match(block["text"])
        toc.append({"number": match.group(1), "title": match.group(2), "block": block["id"]})
    BUILDER.compile_math(blocks)
    chapter = {
        "schemaVersion": 2,
        "bookId": "mackay-information-theory-2003",
        "title": blocks[0]["text"],
        "sourcePdfPages": [480, 482],
        "toc": toc,
        "blocks": blocks,
    }
    OUTPUT.write_text(json.dumps(chapter, ensure_ascii=False, separators=(",", ":")),
                      encoding="utf-8")
    print(f"Wrote {OUTPUT}: {len(blocks)} blocks, {len(toc)} TOC entries, 3 lists")


if __name__ == "__main__":
    main()
