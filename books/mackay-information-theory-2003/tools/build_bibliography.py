"""Compile the page-checked MacKay bibliography as an unpublished reader draft."""

import importlib.util
import json
from collections import Counter
from pathlib import Path


BOOK = Path(__file__).resolve().parents[1]
PARSER = Path(__file__).with_name("build_chapter_01.py")
SPEC = importlib.util.spec_from_file_location("mackay_bibliography_builder", PARSER)
BUILDER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(BUILDER)
SOURCE = BOOK / "translation" / "bibliography"
OUTPUT = BOOK / "chapter-REF.draft.json"
PAGES = range(625, 632)
PER_PAGE = {625: 37, 626: 49, 627: 44, 628: 47, 629: 47, 630: 49, 631: 45}


def no_image(source: str) -> str:
    raise ValueError(f"Bibliography has no printed image: {source}")


def main() -> None:
    blocks = [
        block
        for page in PAGES
        for block in BUILDER.compile_page(
            page, source=SOURCE / f"pdf-{page}.md", image_resolver=no_image,
            chapter_start=625, chapter_number=0,
        )
    ]
    headings = [block for block in blocks if block["kind"] == "heading"]
    if len(headings) != 1 or headings[0]["level"] != 1 or headings[0]["text"] != "参考文献":
        raise ValueError("Bibliography heading changed")
    if blocks[0] is not headings[0]:
        raise ValueError("Bibliography heading must start the first page")
    headings[0]["html"] = (
        '<h1 style="text-align:center;border-top:3px solid currentColor;'
        'padding-top:.45em;font-style:italic;font-weight:normal">参考文献</h1>'
    )
    entries = [block for block in blocks if block["kind"] == "paragraph"]
    counts = Counter(block["pdfPage"] for block in entries)
    if counts != PER_PAGE:
        raise ValueError(f"Bibliography entry counts changed: {counts}")
    if len(entries) != 318:
        raise ValueError(f"Bibliography has {len(entries)} entries instead of 318")
    if not entries[0]["text"].startswith("Abrahamsen, P. (1997)"):
        raise ValueError("First bibliography entry changed")
    if not entries[-1]["text"].startswith("Ziv, J., and Lempel, A. (1978)"):
        raise ValueError("Last bibliography entry changed")
    for entry in entries:
        if "(" not in entry["text"] or "（" not in entry["text"]:
            raise ValueError(f"Missing original citation or English title: {entry['id']}")
        entry["kind"] = "reference-entry"
    if any(block["kind"] not in {"heading", "reference-entry"} for block in blocks):
        raise ValueError("Unexpected bibliography block kind")
    if len({block["id"] for block in blocks}) != len(blocks):
        raise ValueError("Duplicate bibliography block ID")
    if [block["pdfPage"] for block in blocks] != sorted(block["pdfPage"] for block in blocks):
        raise ValueError("Bibliography pages are out of order")
    chapter = {
        "schemaVersion": 2,
        "bookId": "mackay-information-theory-2003",
        "title": "参考文献",
        "sourcePdfPages": [625, 631],
        "toc": [{"number": "", "title": "参考文献", "block": blocks[0]["id"]}],
        "blocks": blocks,
    }
    OUTPUT.write_text(json.dumps(chapter, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(f"Wrote {OUTPUT}: {len(entries)} entries across {len(PER_PAGE)} original pages")


if __name__ == "__main__":
    main()
