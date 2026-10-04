"""Compile the original 'About Chapter 6' page for unpublished review."""

import importlib.util
import json
from pathlib import Path


BOOK = Path(__file__).resolve().parents[1]
PARSER = Path(__file__).with_name("build_chapter_01.py")
spec = importlib.util.spec_from_file_location("mackay_chapter_builder", PARSER)
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)


def no_image(source: str) -> str:
    raise ValueError(f"Unexpected About Chapter 6 image: {source}")


def main():
    blocks = builder.compile_page(
        121,
        source=BOOK / "translation" / "chapter-06" / "about-chapter-06" / "pdf-121.md",
        image_resolver=no_image,
        chapter_start=121,
        chapter_number=6,
    )
    if [block["kind"] for block in blocks] != ["heading", "paragraph", "paragraph"]:
        raise ValueError("About Chapter 6 paragraph structure changed")
    builder.compile_math(blocks)
    chapter = {
        "schemaVersion": 2,
        "bookId": "mackay-information-theory-2003",
        "title": "关于第 6 章",
        "sourcePdfPages": [121, 121],
        "toc": [{"number": "导页", "title": "关于第 6 章", "block": blocks[0]["id"]}],
        "blocks": blocks,
    }
    output = BOOK / "chapter-06-intro.draft.json"
    output.write_text(json.dumps(chapter, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(f"Wrote {output}: {len(blocks)} blocks")


if __name__ == "__main__":
    main()
