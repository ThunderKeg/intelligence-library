"""Compile MacKay Part VII's source-checked title page as an unpublished draft."""

import importlib.util
import json
from pathlib import Path


BOOK = Path(__file__).resolve().parents[1]
PARSER = Path(__file__).with_name("build_chapter_01.py")
SPEC = importlib.util.spec_from_file_location("mackay_part_vii_builder", PARSER)
BUILDER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(BUILDER)
SOURCE = BOOK / "translation" / "part-VII" / "pdf-609.md"
OUTPUT = BOOK / "chapter-VII.draft.json"
IMAGE = BOOK / "assets" / "part-VII-emblem.png"


def part_image(source: str) -> str:
    if source != "../../assets/part-VII-emblem.png":
        raise ValueError(f"Unexpected Part VII graphic: {source}")
    if not IMAGE.is_file():
        raise FileNotFoundError(IMAGE)
    return "assets/part-VII-emblem.png"


def main() -> None:
    blocks = BUILDER.compile_page(
        609, source=SOURCE, image_resolver=part_image,
        chapter_start=609, chapter_number=0,
    )
    if [block["kind"] for block in blocks] != ["heading", "figure"]:
        raise ValueError("Part VII title page must have exactly a heading and original graphic")
    if blocks[0]["text"] != "第七部分　附录":
        raise ValueError("Part VII title changed")
    blocks[0]["segments"] = ["第七部分\n附录"]
    if blocks[1]["src"] != "assets/part-VII-emblem.png":
        raise ValueError("Part VII source graphic is missing")
    blocks[1]["wide"] = True
    chapter = {
        "schemaVersion": 2,
        "bookId": "mackay-information-theory-2003",
        "title": blocks[0]["text"],
        "sourcePdfPages": [609, 609],
        "toc": [{"number": "第七部分", "title": "附录", "block": blocks[0]["id"]}],
        "blocks": blocks,
    }
    OUTPUT.write_text(json.dumps(chapter, ensure_ascii=False, separators=(",", ":")),
                      encoding="utf-8")
    print(f"Wrote {OUTPUT}: {len(blocks)} blocks")


if __name__ == "__main__":
    main()
