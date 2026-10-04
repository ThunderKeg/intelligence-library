"""Compile the original 'About Chapter 11' page for unpublished review."""

import importlib.util
import json
from pathlib import Path


BOOK = Path(__file__).resolve().parents[1]
PARSER = Path(__file__).with_name("build_chapter_01.py")
spec = importlib.util.spec_from_file_location("mackay_chapter_builder", PARSER)
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)


def no_image(source: str) -> str:
    raise ValueError(f"Unexpected About Chapter 11 image: {source}")


def main():
    blocks = builder.compile_page(
        188,
        source=BOOK / "translation" / "chapter-11" / "about-chapter-11" / "pdf-188.md",
        image_resolver=no_image,
        chapter_start=188,
        chapter_number=11,
    )
    if blocks[0]["kind"] != "heading" or blocks[0]["text"] != "关于第 11 章":
        raise ValueError("About Chapter 11 title changed")
    if any(block["kind"] in ("figure", "table", "exercise") for block in blocks):
        raise ValueError("Unexpected figure, table, or exercise in About Chapter 11")
    numbers = [block["number"] for block in blocks if block["kind"] == "formula"]
    if numbers != [f"(11.{number})" for number in range(1, 5)]:
        raise ValueError(f"About Chapter 11 requires equations (11.1)–(11.4): {numbers}")
    builder.compile_math(blocks)
    chapter = {
        "schemaVersion": 2,
        "bookId": "mackay-information-theory-2003",
        "title": "关于第 11 章",
        "sourcePdfPages": [188, 188],
        "toc": [{"number": "导页", "title": "关于第 11 章", "block": blocks[0]["id"]}],
        "blocks": blocks,
    }
    output = BOOK / "chapter-11-intro.draft.json"
    output.write_text(json.dumps(chapter, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(f"Wrote {output}: {len(blocks)} blocks, 4 numbered formulas")


if __name__ == "__main__":
    main()
