"""Compile the first part title page for unpublished reader review."""

import importlib.util
import json
from pathlib import Path


BOOK = Path(__file__).resolve().parents[1]
PARSER = Path(__file__).with_name("build_chapter_01.py")
spec = importlib.util.spec_from_file_location("mackay_chapter_builder", PARSER)
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)


def part_image(source: str) -> str:
    if source != "../../assets/part-I-emblem.png":
        raise ValueError(f"Unexpected part I image: {source}")
    path = BOOK / "assets" / "part-I-emblem.png"
    if not path.is_file():
        raise FileNotFoundError(path)
    return "assets/part-I-emblem.png"


def main():
    blocks = builder.compile_page(
        77,
        source=BOOK / "translation" / "part-I" / "pdf-077.md",
        image_resolver=part_image,
        chapter_start=77,
        chapter_number=0,
    )
    if [block["kind"] for block in blocks] != ["heading", "figure"]:
        raise ValueError("Part I title page must include heading and original artwork")
    chapter = {
        "schemaVersion": 2,
        "bookId": "mackay-information-theory-2003",
        "title": "第一部分　数据压缩",
        "sourcePdfPages": [77, 77],
        "toc": [{"number": "第一部分", "title": "数据压缩", "block": blocks[0]["id"]}],
        "blocks": blocks,
    }
    output = BOOK / "chapter-I.draft.json"
    output.write_text(json.dumps(chapter, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(f"Wrote {output}: {len(blocks)} blocks")


if __name__ == "__main__":
    main()
