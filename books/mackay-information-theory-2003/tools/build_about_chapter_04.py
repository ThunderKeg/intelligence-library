"""Compile the independent 'About Chapter 4' page for unpublished review."""

import importlib.util
import json
from pathlib import Path


BOOK = Path(__file__).resolve().parents[1]
PARSER = Path(__file__).with_name("build_chapter_01.py")
spec = importlib.util.spec_from_file_location("mackay_chapter_builder", PARSER)
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)


def no_image(source: str) -> str:
    raise ValueError(f"Unexpected About Chapter 4 image: {source}")


def main():
    blocks = builder.compile_page(
        78,
        source=BOOK / "translation" / "chapter-04" / "about-chapter-04" / "pdf-078.md",
        image_resolver=no_image,
        chapter_start=78,
        chapter_number=4,
    )
    if not blocks or blocks[0]["kind"] != "heading":
        raise ValueError("About Chapter 4 heading missing")
    for block in blocks:
        if block["kind"] == "table":
            block["notation"] = True
    builder.compile_math(blocks)
    chapter = {
        "schemaVersion": 2,
        "bookId": "mackay-information-theory-2003",
        "title": "关于第 4 章",
        "sourcePdfPages": [78, 78],
        "toc": [{"number": "导页", "title": "关于第 4 章", "block": blocks[0]["id"]}],
        "blocks": blocks,
    }
    output = BOOK / "chapter-04-intro.draft.json"
    output.write_text(json.dumps(chapter, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(f"Wrote {output}: {len(blocks)} blocks")


if __name__ == "__main__":
    main()
