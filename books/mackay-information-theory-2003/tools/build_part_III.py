"""Compile the third part title page for unpublished review."""

import importlib.util
import json
from pathlib import Path


BOOK = Path(__file__).resolve().parents[1]
PARSER = Path(__file__).with_name("build_chapter_01.py")
spec = importlib.util.spec_from_file_location("mackay_chapter_builder", PARSER)
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)


def part_image(source: str) -> str:
    if source != "../../assets/part-III-emblem.png":
        raise ValueError(f"Unexpected part III image: {source}")
    path = BOOK / "assets" / "part-III-emblem.png"
    if not path.is_file():
        raise FileNotFoundError(path)
    return "assets/part-III-emblem.png"


def main():
    blocks = builder.compile_page(
        203,
        source=BOOK / "translation" / "part-III" / "pdf-203.md",
        image_resolver=part_image,
        chapter_start=203,
        chapter_number=0,
    )
    if [block["kind"] for block in blocks] != ["heading", "figure"]:
        raise ValueError("Part III title page must include heading and original artwork")
    blocks[0]["segments"] = ["第三部分\n信息论的更多主题"]
    chapter = {
        "schemaVersion": 2,
        "bookId": "mackay-information-theory-2003",
        "title": "第三部分　信息论的更多主题",
        "sourcePdfPages": [203, 203],
        "toc": [{"number": "第三部分", "title": "信息论的更多主题", "block": blocks[0]["id"]}],
        "blocks": blocks,
    }
    output = BOOK / "chapter-III.draft.json"
    output.write_text(json.dumps(chapter, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(f"Wrote {output}: {len(blocks)} blocks")


if __name__ == "__main__":
    main()
