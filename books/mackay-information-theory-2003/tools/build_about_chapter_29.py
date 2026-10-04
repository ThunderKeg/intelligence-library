"""Compile the original 'About Chapter 29' page for unpublished review."""

import importlib.util
import json
from pathlib import Path


BOOK = Path(__file__).resolve().parents[1]
PARSER = Path(__file__).with_name("build_chapter_01.py")
spec = importlib.util.spec_from_file_location("mackay_chapter_builder", PARSER)
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)


def no_image(source: str) -> str:
    raise ValueError(f"Unexpected About Chapter 29 image: {source}")


def main():
    blocks = builder.compile_page(
        368,
        source=BOOK / "translation" / "chapter-29-intro" / "pdf-368.md",
        image_resolver=no_image,
        chapter_start=368,
        chapter_number=29,
    )
    expected = (["heading"] + ["paragraph"] * 5 +
                ["formula", "paragraph", "formula", "paragraph"])
    if [block["kind"] for block in blocks] != expected:
        raise ValueError("About Chapter 29 must contain its title, seven paragraphs and two formulas")
    if blocks[0]["text"] != "关于第 29 章":
        raise ValueError("About Chapter 29 title changed")
    numbers = [block["number"] for block in blocks if block["kind"] == "formula"]
    if numbers != ["(29.1)", "(29.2)"]:
        raise ValueError(f"About Chapter 29 requires equations (29.1)–(29.2): {numbers}")
    builder.compile_math(blocks)
    chapter = {
        "schemaVersion": 2,
        "bookId": "mackay-information-theory-2003",
        "title": "关于第 29 章",
        "sourcePdfPages": [368, 368],
        "toc": [{"number": "导页", "title": "关于第 29 章", "block": blocks[0]["id"]}],
        "blocks": blocks,
    }
    output = BOOK / "chapter-29-intro.draft.json"
    output.write_text(json.dumps(chapter, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(f"Wrote {output}: {len(blocks)} blocks, 2 numbered formulas")


if __name__ == "__main__":
    main()
