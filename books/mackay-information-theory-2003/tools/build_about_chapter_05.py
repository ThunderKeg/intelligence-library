"""Compile the original 'About Chapter 5' page for unpublished review."""

import importlib.util
import json
from pathlib import Path


BOOK = Path(__file__).resolve().parents[1]
PARSER = Path(__file__).with_name("build_chapter_01.py")
spec = importlib.util.spec_from_file_location("mackay_chapter_builder", PARSER)
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)


def no_image(source: str) -> str:
    raise ValueError(f"Unexpected About Chapter 5 image: {source}")


def main():
    blocks = builder.compile_page(
        102,
        source=BOOK / "translation" / "chapter-05" / "about-chapter-05" / "pdf-102.md",
        image_resolver=no_image,
        chapter_start=102,
        chapter_number=5,
    )
    if [block["kind"] for block in blocks] != [
        "heading", "paragraph", "paragraph", "paragraph", "paragraph", "paragraph", "table"
    ]:
        raise ValueError("About Chapter 5 paragraph or notation structure changed")
    for block in blocks:
        if block["kind"] == "table":
            block["notation"] = True
    builder.compile_math(blocks)
    chapter = {
        "schemaVersion": 2,
        "bookId": "mackay-information-theory-2003",
        "title": "关于第 5 章",
        "sourcePdfPages": [102, 102],
        "toc": [{"number": "导页", "title": "关于第 5 章", "block": blocks[0]["id"]}],
        "blocks": blocks,
    }
    output = BOOK / "chapter-05-intro.draft.json"
    output.write_text(json.dumps(chapter, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(f"Wrote {output}: {len(blocks)} blocks")


if __name__ == "__main__":
    main()
