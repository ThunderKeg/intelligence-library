"""Compile MacKay Part VI's source-checked title page as an unpublished draft."""

import importlib.util
import json
from pathlib import Path


BOOK = Path(__file__).resolve().parents[1]
PARSER = Path(__file__).with_name("build_chapter_01.py")
SPEC = importlib.util.spec_from_file_location("mackay_part_vi_builder", PARSER)
BUILDER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(BUILDER)
SOURCE = BOOK / "translation" / "part-VI" / "pdf-567.md"
OUTPUT = BOOK / "chapter-VI.draft.json"
IMAGE = BOOK / "assets" / "part-VI-emblem.png"


def part_image(source: str) -> str:
    if source != "../../assets/part-VI-emblem.png":
        raise ValueError(f"Unexpected Part VI graphic: {source}")
    if not IMAGE.is_file():
        raise FileNotFoundError(IMAGE)
    return "assets/part-VI-emblem.png"


def main() -> None:
    blocks = BUILDER.compile_page(
        567, source=SOURCE, image_resolver=part_image,
        chapter_start=567, chapter_number=0,
    )
    if [block["kind"] for block in blocks] != ["heading", "figure"]:
        raise ValueError("Part VI title page must have exactly a heading and original graphic")
    if blocks[0]["text"] != "第六部分　稀疏图码":
        raise ValueError("Part VI title changed")
    blocks[0]["segments"] = ["第六部分\n稀疏图码"]
    if blocks[1]["src"] != "assets/part-VI-emblem.png":
        raise ValueError("Part VI source graphic is missing")
    blocks[1]["wide"] = True
    chapter = {
        "schemaVersion": 2,
        "bookId": "mackay-information-theory-2003",
        "title": blocks[0]["text"],
        "sourcePdfPages": [567, 567],
        "toc": [{"number": "第六部分", "title": "稀疏图码", "block": blocks[0]["id"]}],
        "blocks": blocks,
    }
    OUTPUT.write_text(json.dumps(chapter, ensure_ascii=False, separators=(",", ":")),
                      encoding="utf-8")
    print(f"Wrote {OUTPUT}: {len(blocks)} blocks")


if __name__ == "__main__":
    main()
