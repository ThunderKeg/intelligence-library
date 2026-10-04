"""Compile the fourth part title page for unpublished review."""

import importlib.util
import json
from pathlib import Path


BOOK = Path(__file__).resolve().parents[1]
PARSER = Path(__file__).with_name("build_chapter_01.py")
spec = importlib.util.spec_from_file_location("mackay_chapter_builder", PARSER)
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)


def part_image(source: str) -> str:
    if source != "../../assets/part-IV-emblem.png":
        raise ValueError(f"Unexpected part IV image: {source}")
    path = BOOK / "assets" / "part-IV-emblem.png"
    if not path.is_file():
        raise FileNotFoundError(path)
    return "assets/part-IV-emblem.png"


def main():
    blocks = builder.compile_page(
        293,
        source=BOOK / "translation" / "part-IV" / "pdf-293.md",
        image_resolver=part_image,
        chapter_start=293,
        chapter_number=0,
    )
    if [block["kind"] for block in blocks] != ["heading", "figure"]:
        raise ValueError("Part IV title page must include heading and original artwork")
    blocks[0]["segments"] = ["第四部分\n概率与推断"]
    chapter = {
        "schemaVersion": 2,
        "bookId": "mackay-information-theory-2003",
        "title": "第四部分　概率与推断",
        "sourcePdfPages": [293, 293],
        "toc": [{"number": "第四部分", "title": "概率与推断", "block": blocks[0]["id"]}],
        "blocks": blocks,
    }
    output = BOOK / "chapter-IV.draft.json"
    output.write_text(json.dumps(chapter, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(f"Wrote {output}: {len(blocks)} blocks")


if __name__ == "__main__":
    main()
