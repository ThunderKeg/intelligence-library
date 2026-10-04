"""Compile MacKay's independent 'About Chapter 3' page for reader review."""

import importlib.util
import json
import re
from pathlib import Path


BOOK = Path(__file__).resolve().parents[1]
PARSER = Path(__file__).with_name("build_chapter_01.py")
spec = importlib.util.spec_from_file_location("mackay_chapter_builder", PARSER)
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)
IMAGE = re.compile(r"^\.\./\.\./\.\./assets/chapter-03/([\w.-]+\.(?:png|jpg|svg|webp))$")


def about_image(source: str) -> str:
    match = IMAGE.fullmatch(source)
    if not match:
        raise ValueError(f"Unexpected About Chapter 3 image path: {source}")
    path = BOOK / "assets" / "chapter-03" / match.group(1)
    if not path.is_file():
        raise FileNotFoundError(path)
    return f"assets/chapter-03/{match.group(1)}"


def main():
    blocks = builder.compile_page(
        59,
        source=BOOK / "translation" / "chapter-03" / "about-chapter-03" / "pdf-059.md",
        image_resolver=about_image,
        chapter_start=59,
        chapter_number=3,
    )
    if not blocks or blocks[0]["kind"] != "heading":
        raise ValueError("About Chapter 3 heading missing")
    for block in blocks:
        if block["kind"] == "table":
            block["notation"] = True
        if block["kind"] == "figure" and block["width"] >= 560:
            block["wide"] = True
    builder.compile_math(blocks)
    output = BOOK / "chapter-03-intro.draft.json"
    output.write_text(json.dumps({
        "schemaVersion": 2,
        "bookId": "mackay-information-theory-2003",
        "title": "关于第 3 章",
        "sourcePdfPages": [59, 59],
        "toc": [{"number": "导页", "title": "关于第 3 章", "block": blocks[0]["id"]}],
        "blocks": blocks,
    }, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(f"Wrote {output}: {len(blocks)} blocks")


if __name__ == "__main__":
    main()
