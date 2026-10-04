"""Compile the original 'About Chapter 31' page for unpublished review."""

import importlib.util
import json
from pathlib import Path


BOOK = Path(__file__).resolve().parents[1]
PARSER = Path(__file__).with_name("build_chapter_01.py")
SPEC = importlib.util.spec_from_file_location("mackay_chapter_builder_31_intro", PARSER)
BUILDER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(BUILDER)
SOURCE = BOOK / "translation" / "chapter-31-intro" / "pdf-411.md"
OUTPUT = BOOK / "chapter-31-intro.draft.json"


def no_image(source: str) -> str:
    raise ValueError(f"Unexpected About Chapter 31 image: {source}")


def main() -> None:
    blocks = BUILDER.compile_page(
        411,
        source=SOURCE,
        image_resolver=no_image,
        chapter_start=411,
        chapter_number=31,
    )
    kinds = [block["kind"] for block in blocks]
    if kinds != ["heading", "paragraph", "paragraph", "paragraph"]:
        raise ValueError(f"About Chapter 31 must have title and three paragraphs: {kinds}")
    if blocks[0]["text"] != "关于第 31 章":
        raise ValueError("About Chapter 31 title changed")
    if any(block["kind"] in {"figure", "formula", "exercise", "table"} for block in blocks):
        raise ValueError("The original About Chapter 31 page has no figure/formula/exercise/table")
    BUILDER.compile_math(blocks)
    chapter = {
        "schemaVersion": 2,
        "bookId": "mackay-information-theory-2003",
        "title": "关于第 31 章",
        "sourcePdfPages": [411, 411],
        "toc": [{"number": "导页", "title": "关于第 31 章", "block": blocks[0]["id"]}],
        "blocks": blocks,
    }
    OUTPUT.write_text(json.dumps(chapter, ensure_ascii=False, separators=(",", ":")),
                      encoding="utf-8")
    print(f"Wrote {OUTPUT}: {len(blocks)} blocks, three original paragraphs")


if __name__ == "__main__":
    main()
