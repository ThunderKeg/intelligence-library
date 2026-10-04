"""Compile the separate MacKay PDF494 chapter-40 preparatory exercise page."""

import importlib.util
import json
import re
from pathlib import Path


BOOK = Path(__file__).resolve().parents[1]
PARSER = Path(__file__).with_name("build_chapter_01.py")
SPEC = importlib.util.spec_from_file_location("mackay_chapter_builder_40_prelude", PARSER)
BUILDER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(BUILDER)
SOURCE = BOOK / "translation" / "chapter-40-prelude" / "pdf-494.md"
OUTPUT = BOOK / "chapter-40-prelude.draft.json"


def reject_image(source: str) -> str:
    raise ValueError(f"PDF494 has no figure: {source}")


def main() -> None:
    blocks = BUILDER.compile_page(
        494, source=SOURCE, image_resolver=reject_image,
        chapter_start=494, chapter_number=40,
    )
    if blocks[0]["kind"] != "heading" or blocks[0]["level"] != 1 or \
            blocks[0]["text"] != "阅读第 40 章之前的习题":
        raise ValueError("PDF494 preparatory title missing")
    labels = [re.search(r"40\.\d+", block["label"]).group()
              for block in blocks if block["kind"] == "exercise"]
    if labels != ["40.1", "40.2", "40.3"]:
        raise ValueError(f"PDF494 exercise order error: {labels}")
    if any(block["kind"] in {"figure", "formula", "table", "code", "footnote"}
           for block in blocks):
        raise ValueError("PDF494 has no figure, display formula, table, code or footnote")
    if not blocks[-1]["text"].endswith("Yaser Abu-Mostafa。"):
        raise ValueError("PDF494 closing attribution missing")
    BUILDER.compile_math(blocks)
    chapter = {
        "schemaVersion": 2,
        "bookId": "mackay-information-theory-2003",
        "title": blocks[0]["text"],
        "sourcePdfPages": [494, 494],
        "toc": [{"number": "40-prelude", "title": blocks[0]["text"], "block": blocks[0]["id"]}],
        "blocks": blocks,
    }
    OUTPUT.write_text(json.dumps(chapter, ensure_ascii=False, separators=(",", ":")),
                      encoding="utf-8")
    print(f"Wrote {OUTPUT}: {len(blocks)} blocks, 3 exercises")


if __name__ == "__main__":
    main()
