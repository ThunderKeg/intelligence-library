"""Compile MacKay's source-checked About Part VI page as an unpublished draft."""

import importlib.util
import json
from pathlib import Path


BOOK = Path(__file__).resolve().parents[1]
PARSER = Path(__file__).with_name("build_chapter_01.py")
SPEC = importlib.util.spec_from_file_location("mackay_about_part_vi_builder", PARSER)
BUILDER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(BUILDER)
SOURCE = BOOK / "translation" / "part-VI" / "about-part-VI" / "pdf-568.md"
OUTPUT = BOOK / "chapter-VI-intro.draft.json"
TITLE = "关于第六部分"


def reject_image(source: str) -> str:
    raise ValueError(f"About Part VI has no source graphic: {source}")


def main() -> None:
    blocks = BUILDER.compile_page(
        568, source=SOURCE, image_resolver=reject_image,
        chapter_start=568, chapter_number=0,
    )
    if [block["kind"] for block in blocks] != [
            "heading", "paragraph", "paragraph", "paragraph", "paragraph"]:
        raise ValueError(f"PDF568 structure differs from source: {[b['kind'] for b in blocks]}")
    if blocks[0]["text"] != TITLE or blocks[0]["level"] != 1:
        raise ValueError("PDF568 independent heading is missing")
    blocks[0]["html"] = (
        '<h1 style="border-top:3px solid currentColor;padding-top:.65em;'
        f'text-align:center;font-style:italic">{TITLE}</h1>'
    )
    BUILDER.compile_math(blocks)
    chapter = {
        "schemaVersion": 2,
        "bookId": "mackay-information-theory-2003",
        "title": TITLE,
        "sourcePdfPages": [568, 568],
        "toc": [{"number": "第六部分导页", "title": TITLE, "block": blocks[0]["id"]}],
        "blocks": blocks,
    }
    OUTPUT.write_text(json.dumps(chapter, ensure_ascii=False, separators=(",", ":")),
                      encoding="utf-8")
    print(f"Wrote {OUTPUT}: {len(blocks)} blocks, 1 TOC entry")


if __name__ == "__main__":
    main()
