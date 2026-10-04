"""Compile the page-aligned Chapter 4 translation for unpublished review."""

import argparse
import importlib.util
import json
import re
from pathlib import Path


BOOK = Path(__file__).resolve().parents[1]
PARSER = Path(__file__).with_name("build_chapter_01.py")
spec = importlib.util.spec_from_file_location("mackay_chapter_builder", PARSER)
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)
IMAGE = re.compile(r"^\.\./\.\./assets/chapter-04/([\w.-]+\.(?:png|jpg|svg|webp))$")
HEADING = re.compile(r"^(4(?:\.\d+)*)\s+(.+)$")


def chapter_image(source: str) -> str:
    match = IMAGE.fullmatch(source)
    if not match:
        raise ValueError(f"Unexpected chapter 4 image path: {source}")
    path = BOOK / "assets" / "chapter-04" / match.group(1)
    if not path.is_file():
        raise FileNotFoundError(path)
    return f"assets/chapter-04/{match.group(1)}"


def main():
    cli = argparse.ArgumentParser()
    cli.add_argument("--through", type=int, default=101, choices=range(79, 102))
    args = cli.parse_args()
    blocks = [
        block
        for page in range(79, args.through + 1)
        for block in builder.compile_page(
            page,
            source=BOOK / "translation" / "chapter-04" / f"pdf-{page:03d}.md",
            image_resolver=chapter_image,
            chapter_start=79,
            chapter_number=4,
        )
    ]
    if not blocks or blocks[0]["kind"] != "heading":
        raise ValueError("Chapter 4 heading missing")
    if not any(block["kind"] == "intro" for block in blocks):
        raise ValueError("Chapter 4 editor's introduction missing")
    for block in blocks:
        if block["kind"] == "figure" and block["width"] >= 560:
            block["wide"] = True
    toc = []
    for block in blocks:
        if block["kind"] != "heading":
            continue
        match = HEADING.match(block["text"])
        if block["level"] == 1:
            toc.append({"number": "4", "title": "信源编码定理", "block": block["id"]})
        elif match and block["level"] == 2:
            toc.append({"number": match.group(1), "title": match.group(2), "block": block["id"]})
    if args.through == 101 and [entry["number"] for entry in toc] != ["4"] + [f"4.{n}" for n in range(1, 9)]:
        raise ValueError(f"Unexpected chapter 4 sections: {toc}")
    numbers = [block["number"] for block in blocks if block["kind"] == "formula" and block["number"]]
    if len(numbers) != len(set(numbers)):
        raise ValueError("Duplicate chapter 4 equation number")
    if args.through == 101 and numbers != [f"(4.{n})" for n in range(1, 56)]:
        raise ValueError(f"Chapter 4 equations are missing or out of order: {numbers}")
    builder.compile_math(blocks)
    chapter = {
        "schemaVersion": 2,
        "bookId": "mackay-information-theory-2003",
        "title": blocks[0]["text"],
        "sourcePdfPages": [79, args.through],
        "toc": toc,
        "blocks": blocks,
    }
    suffix = "draft" if args.through == 101 else "partial"
    output = BOOK / f"chapter-04.{suffix}.json"
    output.write_text(json.dumps(chapter, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(f"Wrote {output}: {len(blocks)} blocks, {len(toc)} sections, {len(numbers)} numbered formulas")


if __name__ == "__main__":
    main()
