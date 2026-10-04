"""Compile the original two-page 'About Part IV' for unpublished review."""

import importlib.util
import json
from pathlib import Path


BOOK = Path(__file__).resolve().parents[1]
PARSER = Path(__file__).with_name("build_chapter_01.py")
spec = importlib.util.spec_from_file_location("mackay_chapter_builder", PARSER)
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)


def no_image(source: str) -> str:
    raise ValueError(f"Unexpected About Part IV image: {source}")


def main():
    blocks = []
    for page in (294, 295):
        blocks.extend(builder.compile_page(
            page,
            source=BOOK / "translation" / "part-IV" / "about-part-IV" / f"pdf-{page}.md",
            image_resolver=no_image,
            chapter_start=294,
            chapter_number=0,
        ))
    kinds = [block["kind"] for block in blocks]
    if kinds.count("heading") != 3 or kinds.count("list") != 1:
        raise ValueError(f"Unexpected About Part IV structure: {kinds}")
    builder.compile_math(blocks)
    chapter = {
        "schemaVersion": 2,
        "bookId": "mackay-information-theory-2003",
        "title": "关于第四部分",
        "sourcePdfPages": [294, 295],
        "toc": [{"number": "导页", "title": "关于第四部分", "block": blocks[0]["id"]}],
        "blocks": blocks,
    }
    output = BOOK / "chapter-IV-intro.draft.json"
    output.write_text(json.dumps(chapter, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(f"Wrote {output}: {len(blocks)} blocks")


if __name__ == "__main__":
    main()
