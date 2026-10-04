"""Compile the second part title page for unpublished reader review."""

import importlib.util
import json
from pathlib import Path


BOOK = Path(__file__).resolve().parents[1]
PARSER = Path(__file__).with_name("build_chapter_01.py")
spec = importlib.util.spec_from_file_location("mackay_chapter_builder", PARSER)
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)


def part_image(source: str) -> str:
    if source != "../../assets/part-II-emblem.png":
        raise ValueError(f"Unexpected part II image: {source}")
    path = BOOK / "assets" / "part-II-emblem.png"
    if not path.is_file():
        raise FileNotFoundError(path)
    return "assets/part-II-emblem.png"


def main():
    blocks = builder.compile_page(
        149,
        source=BOOK / "translation" / "part-II" / "pdf-149.md",
        image_resolver=part_image,
        chapter_start=149,
        chapter_number=0,
    )
    if [block["kind"] for block in blocks] != ["heading", "figure"]:
        raise ValueError("Part II title page must include heading and original artwork")
    # The printed part title uses two lines; preserve that break on narrow screens.
    blocks[0]["segments"] = ["第二部分\n有噪信道编码"]
    chapter = {
        "schemaVersion": 2,
        "bookId": "mackay-information-theory-2003",
        "title": "第二部分　有噪信道编码",
        "sourcePdfPages": [149, 149],
        "toc": [{"number": "第二部分", "title": "有噪信道编码", "block": blocks[0]["id"]}],
        "blocks": blocks,
    }
    output = BOOK / "chapter-II.draft.json"
    output.write_text(json.dumps(chapter, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(f"Wrote {output}: {len(blocks)} blocks")


if __name__ == "__main__":
    main()
