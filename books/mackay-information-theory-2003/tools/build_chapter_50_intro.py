"""Compile the separate MacKay PDF600 About Chapter 50 page as a draft."""

import importlib.util
import json
from pathlib import Path


BOOK = Path(__file__).resolve().parents[1]
PARSER = Path(__file__).with_name("build_chapter_01.py")
SPEC = importlib.util.spec_from_file_location("mackay_chapter_builder_50_intro", PARSER)
BUILDER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(BUILDER)
SOURCE = BOOK / "translation" / "chapter-50-intro" / "pdf-600.md"
OUTPUT = BOOK / "chapter-50-intro.draft.json"
TITLE = "关于第 50 章"


def reject_image(source: str) -> str:
    raise ValueError(f"PDF600 has no figure: {source}")


def main() -> None:
    blocks = BUILDER.compile_page(
        600, source=SOURCE, image_resolver=reject_image,
        chapter_start=600, chapter_number=50,
    )
    if [block["kind"] for block in blocks] != [
            "heading", "paragraph", "exercise", "paragraph", "paragraph",
            "paragraph", "paragraph"]:
        raise ValueError(f"PDF600 source structure changed: {[b['kind'] for b in blocks]}")
    if blocks[0]["text"] != TITLE or blocks[0]["level"] != 1:
        raise ValueError("PDF600 independent title missing")
    blocks[0]["html"] = (
        '<h1 style="border-top:3px solid currentColor;padding-top:.65em;'
        f'text-align:center;font-style:italic">{TITLE}</h1>'
    )
    if blocks[2]["label"] != "▷ 习题 50.1" or "（难度 3）" not in blocks[2]["text"]:
        raise ValueError("PDF600 exercise or source triangle missing")
    for letter, block in zip("abc", blocks[3:6]):
        if not block["text"].startswith(f"({letter}) "):
            raise ValueError(f"Exercise 50.1 part ({letter}) missing")
    if not (blocks[6]["text"].startswith("[") and blocks[6]["text"].endswith("]")):
        raise ValueError("PDF600 bracketed ball-and-bin comment missing")
    if any(block["kind"] in {"formula", "figure", "table", "code", "footnote"}
           for block in blocks):
        raise ValueError("PDF600 has no standalone formula, graphic, table, code or footnote")
    BUILDER.compile_math(blocks)
    if not any(isinstance(segment, dict)
               and segment.get("tex") == "N\\simeq K\\ln(K/\\delta)"
               for segment in blocks[5]["segments"]):
        raise ValueError("Exercise 50.1(c) formula changed")
    chapter = {
        "schemaVersion": 2, "bookId": "mackay-information-theory-2003",
        "title": TITLE, "sourcePdfPages": [600, 600],
        "toc": [{"number": "50-intro", "title": TITLE, "block": blocks[0]["id"]}],
        "blocks": blocks,
    }
    OUTPUT.write_text(json.dumps(chapter, ensure_ascii=False, separators=(",", ":")),
                      encoding="utf-8")
    print(f"Wrote {OUTPUT}: {len(blocks)} blocks, one source exercise")


if __name__ == "__main__":
    main()
