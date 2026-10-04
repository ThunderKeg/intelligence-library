"""Compile the visually checked MacKay Part V title page as an unpublished draft."""

import importlib.util
import json
from pathlib import Path


BOOK = Path(__file__).resolve().parents[1]
PARSER = Path(__file__).with_name("build_chapter_01.py")
SPEC = importlib.util.spec_from_file_location("mackay_part_v_builder", PARSER)
BUILDER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(BUILDER)


def part_image(source: str) -> str:
    if source != "../../assets/part-V-emblem.png":
        raise ValueError(f"Unexpected Part V image: {source}")
    path = BOOK / "assets" / "part-V-emblem.png"
    if not path.is_file():
        raise FileNotFoundError(path)
    return "assets/part-V-emblem.png"


def main() -> None:
    blocks = BUILDER.compile_page(
        479,
        source=BOOK / "translation" / "part-V" / "pdf-479.md",
        image_resolver=part_image,
        chapter_start=479,
        chapter_number=0,
    )
    if [block["kind"] for block in blocks] != ["heading", "figure"]:
        raise ValueError("Part V title page must contain only the heading and original artwork")
    if blocks[0]["text"] != "第五部分　神经网络":
        raise ValueError("Part V heading changed unexpectedly")
    blocks[0]["segments"] = ["第五部分\n神经网络"]
    if blocks[1]["src"] != "assets/part-V-emblem.png":
        raise ValueError("Part V original artwork is missing")
    chapter = {
        "schemaVersion": 2,
        "bookId": "mackay-information-theory-2003",
        "title": blocks[0]["text"],
        "sourcePdfPages": [479, 479],
        "toc": [{"number": "第五部分", "title": "神经网络", "block": blocks[0]["id"]}],
        "blocks": blocks,
    }
    output = BOOK / "chapter-V.draft.json"
    output.write_text(json.dumps(chapter, ensure_ascii=False, separators=(",", ":")),
                      encoding="utf-8")
    print(f"Wrote {output}: {len(blocks)} blocks")


if __name__ == "__main__":
    main()
