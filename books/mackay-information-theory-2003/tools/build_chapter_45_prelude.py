"""Compile the separate MacKay PDF546 About Chapter 45 page as a draft."""

import importlib.util
import json
import re
from pathlib import Path


BOOK = Path(__file__).resolve().parents[1]
PARSER = Path(__file__).with_name("build_chapter_01.py")
SPEC = importlib.util.spec_from_file_location("mackay_chapter_builder_45_prelude", PARSER)
BUILDER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(BUILDER)
SOURCE = BOOK / "translation" / "chapter-45-prelude" / "pdf-546.md"
OUTPUT = BOOK / "chapter-45-prelude.draft.json"
TITLE = "关于第 45 章"
URLS = {
    "http://www.inference.phy.cam.ac.uk/mackay/itprnn/software.html",
    "http://www.cs.toronto.edu/~radford/",
}


def reject_image(source: str) -> str:
    raise ValueError(f"PDF546 has no figure: {source}")


def main() -> None:
    blocks = BUILDER.compile_page(
        546, source=SOURCE, image_resolver=reject_image,
        chapter_start=546, chapter_number=45,
    )
    if [block["kind"] for block in blocks] != [
            "heading", "paragraph", "paragraph", "paragraph", "exercise",
            "paragraph", "paragraph"]:
        raise ValueError(f"PDF546 structure differs from source: {[b['kind'] for b in blocks]}")
    if blocks[0]["text"] != TITLE or blocks[0]["level"] != 1:
        raise ValueError("PDF546 independent title missing")
    blocks[0]["html"] = (
        f'<h1 style="border-top:3px solid currentColor;padding-top:.65em;'
        f'text-align:center;font-style:italic">{TITLE}</h1>'
    )
    if re.search(r"45\.\d+", blocks[4]["label"]).group() != "45.1":
        raise ValueError("PDF546 exercise 45.1 missing")
    if any(block["kind"] in {"formula", "figure", "table", "code", "footnote"}
           for block in blocks):
        raise ValueError("PDF546 has no display formula, figure, table, code or footnote")
    links = {segment["href"] for block in blocks for segment in block.get("segments", [])
             if isinstance(segment, dict) and "href" in segment}
    if links != URLS:
        raise ValueError(f"PDF546 source links differ: {links}")
    BUILDER.compile_math(blocks)
    chapter = {
        "schemaVersion": 2,
        "bookId": "mackay-information-theory-2003",
        "title": TITLE,
        "sourcePdfPages": [546, 546],
        "toc": [{"number": "45-prelude", "title": TITLE, "block": blocks[0]["id"]}],
        "blocks": blocks,
    }
    OUTPUT.write_text(json.dumps(chapter, ensure_ascii=False, separators=(",", ":")),
                      encoding="utf-8")
    print(f"Wrote {OUTPUT}: {len(blocks)} blocks, 1 exercise, 2 links")


if __name__ == "__main__":
    main()
