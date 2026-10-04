"""Compile the MacKay PDF516 postscript as a separate unpublished page."""

import importlib.util
import json
from pathlib import Path


BOOK = Path(__file__).resolve().parents[1]
PARSER = Path(__file__).with_name("build_chapter_01.py")
SPEC = importlib.util.spec_from_file_location("mackay_chapter_builder_41_postscript", PARSER)
BUILDER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(BUILDER)
SOURCE = BOOK / "translation" / "chapter-41-postscript" / "pdf-516.md"
OUTPUT = BOOK / "chapter-41-postscript.draft.json"
TITLE = "有监督神经网络附记"


def reject_image(source: str) -> str:
    raise ValueError(f"PDF516 has no figure: {source}")


def main() -> None:
    blocks = BUILDER.compile_page(
        516, source=SOURCE, image_resolver=reject_image,
        chapter_start=516, chapter_number=41,
    )
    if [block["kind"] for block in blocks] != [
            "heading", "paragraph", "quote", "paragraph", "quote"]:
        raise ValueError(f"PDF516 structure differs from source: {[b['kind'] for b in blocks]}")
    if blocks[0]["text"] != TITLE or blocks[0]["level"] != 1:
        raise ValueError("PDF516 postscript title missing")
    blocks[0]["html"] = (
        f'<h1 style="border-top:3px solid currentColor;padding-top:.65em">{TITLE}</h1>'
    )
    if any(block["kind"] in {"formula", "figure", "table", "code", "exercise"}
           for block in blocks):
        raise ValueError("PDF516 contains no formula, figure, table, code or exercise")
    BUILDER.compile_math(blocks)
    chapter = {
        "schemaVersion": 2,
        "bookId": "mackay-information-theory-2003",
        "title": TITLE,
        "sourcePdfPages": [516, 516],
        "toc": [{"number": "41-postscript", "title": TITLE, "block": blocks[0]["id"]}],
        "blocks": blocks,
    }
    OUTPUT.write_text(json.dumps(chapter, ensure_ascii=False, separators=(",", ":")),
                      encoding="utf-8")
    print(f"Wrote {OUTPUT}: {len(blocks)} blocks, 2 quotations")


if __name__ == "__main__":
    main()
