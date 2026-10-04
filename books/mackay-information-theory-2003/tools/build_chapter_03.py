"""Compile page-aligned chapter 3 for review; never register draft output."""

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
IMAGE = re.compile(r"^\.\./\.\./assets/chapter-03/([\w.-]+\.(?:png|jpg|svg|webp))$")
HEADING = re.compile(r"^(3(?:\.\d+)*)\s+(.+)$")


def chapter_image(source: str) -> str:
    match = IMAGE.fullmatch(source)
    if not match:
        raise ValueError(f"Unexpected chapter 3 image path: {source}")
    path = BOOK / "assets" / "chapter-03" / match.group(1)
    if not path.is_file():
        raise FileNotFoundError(path)
    return f"assets/chapter-03/{match.group(1)}"


def main():
    cli = argparse.ArgumentParser()
    cli.add_argument("--through", type=int, default=76, choices=range(60, 77))
    args = cli.parse_args()
    blocks = [
        block
        for page in range(60, args.through + 1)
        for block in builder.compile_page(
            page,
            source=BOOK / "translation" / "chapter-03" / f"pdf-{page:03d}.md",
            image_resolver=chapter_image,
            chapter_start=60,
            chapter_number=3,
        )
    ]
    if not blocks or blocks[0]["kind"] != "heading":
        raise ValueError("Chapter 3 heading missing")
    if not any(block["kind"] == "intro" for block in blocks):
        raise ValueError("Chapter 3 editor's introduction missing")
    for block in blocks:
        if block["kind"] == "figure" and block["width"] >= 560:
            block["wide"] = True
    toc = []
    for block in blocks:
        if block["kind"] != "heading":
            continue
        match = HEADING.match(block["text"])
        if block["level"] == 1:
            toc.append({"number": "3", "title": "进一步讨论推断", "block": block["id"]})
        elif match and block["level"] == 2:
            toc.append({"number": match.group(1), "title": match.group(2), "block": block["id"]})
    if args.through == 76 and [entry["number"] for entry in toc] != ["3"] + [f"3.{n}" for n in range(1, 7)]:
        raise ValueError(f"Unexpected chapter 3 sections: {toc}")
    numbers = [block["number"] for block in blocks if block["kind"] == "formula" and block["number"]]
    if len(numbers) != len(set(numbers)):
        raise ValueError("Duplicate chapter 3 equation number")
    if args.through == 76 and numbers != [f"(3.{n})" for n in range(1, 48)]:
        raise ValueError(f"Chapter 3 equations are missing or out of order: {numbers}")
    builder.compile_math(blocks)
    chapter = {
        "schemaVersion": 2,
        "bookId": "mackay-information-theory-2003",
        "title": blocks[0]["text"],
        "sourcePdfPages": [60, args.through],
        "toc": toc,
        "blocks": blocks,
    }
    suffix = "draft" if args.through == 76 else "partial"
    output = BOOK / f"chapter-03.{suffix}.json"
    output.write_text(json.dumps(chapter, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(f"Wrote {output}: {len(blocks)} blocks, {len(toc)} sections, {len(numbers)} numbered formulas")


if __name__ == "__main__":
    main()
