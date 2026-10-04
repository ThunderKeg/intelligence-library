"""Compile the original 'About Chapter 13' page for unpublished review."""

import importlib.util
import json
from pathlib import Path


BOOK = Path(__file__).resolve().parents[1]
PARSER = Path(__file__).with_name("build_chapter_01.py")
spec = importlib.util.spec_from_file_location("mackay_chapter_builder", PARSER)
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)


def no_image(source: str) -> str:
    raise ValueError(f"Unexpected About Chapter 13 image: {source}")


def main():
    blocks = builder.compile_page(
        217,
        source=BOOK / "translation" / "chapter-13" / "about-chapter-13" / "pdf-217.md",
        image_resolver=no_image,
        chapter_start=217,
        chapter_number=13,
    )
    if [block["kind"] for block in blocks] != ["heading"] + ["paragraph"] * 2:
        raise ValueError("About Chapter 13 must contain the title and two source paragraphs")
    builder.compile_math(blocks)
    chapter = {
        "schemaVersion": 2,
        "bookId": "mackay-information-theory-2003",
        "title": "关于第 13 章",
        "sourcePdfPages": [217, 217],
        "toc": [{"number": "导页", "title": "关于第 13 章", "block": blocks[0]["id"]}],
        "blocks": blocks,
    }
    output = BOOK / "chapter-13-intro.draft.json"
    output.write_text(json.dumps(chapter, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(f"Wrote {output}: {len(blocks)} blocks")


if __name__ == "__main__":
    main()
