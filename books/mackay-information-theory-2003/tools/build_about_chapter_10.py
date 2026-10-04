"""Compile the original 'About Chapter 10' page for unpublished review."""

import importlib.util
import json
from pathlib import Path


BOOK = Path(__file__).resolve().parents[1]
PARSER = Path(__file__).with_name("build_chapter_01.py")
spec = importlib.util.spec_from_file_location("mackay_chapter_builder", PARSER)
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)


def no_image(source: str) -> str:
    raise ValueError(f"Unexpected About Chapter 10 image: {source}")


def main():
    blocks = builder.compile_page(
        173,
        source=BOOK / "translation" / "chapter-10" / "about-chapter-10" / "pdf-173.md",
        image_resolver=no_image,
        chapter_start=173,
        chapter_number=10,
    )
    if [block["kind"] for block in blocks] != ["heading", "paragraph", "quote", "heading", "table"]:
        raise ValueError("About Chapter 10 paragraph/table structure changed")
    if len(blocks[4]["rows"]) != 13 or any(len(row) != 2 for row in blocks[4]["rows"]):
        raise ValueError("About Chapter 10 requires 12 complete symbol rows")
    builder.compile_math(blocks)
    chapter = {
        "schemaVersion": 2,
        "bookId": "mackay-information-theory-2003",
        "title": "关于第 10 章",
        "sourcePdfPages": [173, 173],
        "toc": [{"number": "导页", "title": "关于第 10 章", "block": blocks[0]["id"]}],
        "blocks": blocks,
    }
    output = BOOK / "chapter-10-intro.draft.json"
    output.write_text(json.dumps(chapter, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(f"Wrote {output}: {len(blocks)} blocks, 12 symbol rows")


if __name__ == "__main__":
    main()
