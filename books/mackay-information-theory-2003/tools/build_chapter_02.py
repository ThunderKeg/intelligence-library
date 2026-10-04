"""Compile the page-aligned chapter 2 translation for unpublished reader review."""

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
IMAGE = re.compile(r"^\.\./\.\./assets/chapter-02/([\w.-]+\.(?:png|jpg|svg|webp))$")
HEADING = re.compile(r"^(2(?:\.\d+)*)\s+(.+)$")


def chapter_image(source: str) -> str:
    match = IMAGE.fullmatch(source)
    if not match:
        raise ValueError(f"Unexpected chapter 2 image path: {source}")
    path = BOOK / "assets" / "chapter-02" / match.group(1)
    if not path.is_file():
        raise FileNotFoundError(path)
    return f"assets/chapter-02/{match.group(1)}"


def main():
    cli = argparse.ArgumentParser()
    cli.add_argument("--through", type=int, default=58, choices=range(34, 59))
    args = cli.parse_args()
    blocks = [
        block
        for page in range(34, args.through + 1)
        for block in builder.compile_page(
            page,
            source=BOOK / "translation" / "chapter-02" / f"pdf-{page:03d}.md",
            image_resolver=chapter_image,
            chapter_start=34,
            chapter_number=2,
        )
    ]
    if not blocks or blocks[0]["kind"] != "heading":
        raise ValueError("Chapter 2 heading missing")
    for block in blocks:
        if block["kind"] == "figure" and block["width"] >= 560:
            block["wide"] = True
    toc = []
    for block in blocks:
        if block["kind"] != "heading":
            continue
        match = HEADING.match(block["text"])
        if block["level"] == 1:
            toc.append({"number": "2", "title": "概率、熵与推断", "block": block["id"]})
        elif match and block["level"] == 2:
            toc.append({"number": match.group(1), "title": match.group(2), "block": block["id"]})
    expected_sections = ["2"] + [f"2.{n}" for n in range(1, 11 if args.through == 58 else 9)]
    if [entry["number"] for entry in toc] != expected_sections:
        raise ValueError(f"Unexpected chapter 2 sections: {toc}")
    numbers = [block["number"] for block in blocks if block["kind"] == "formula" and block["number"]]
    if len(numbers) != len(set(numbers)):
        raise ValueError("Duplicate chapter 2 equation number")
    if args.through == 58 and numbers != [f"(2.{number})" for number in range(1, 114)]:
        raise ValueError("Chapter 2 equations are missing or out of order")
    builder.compile_math(blocks)
    box_start = next((index for index, block in enumerate(blocks) if block["id"] == "p038-b001"), None)
    if box_start is None or [block["id"] for block in blocks[box_start:box_start + 7]] != [
        f"p038-b{number:03d}" for number in range(1, 8)
    ]:
        raise ValueError("Cox axioms box boundaries changed")
    box_children = blocks[box_start:box_start + 7]
    for child, prefix in zip(
        (box_children[1], box_children[2], box_children[3], box_children[5]),
        ("记号。", "公理 1。", "公理 2。", "公理 3。"),
    ):
        first = child["segments"][0]
        if isinstance(first, dict) and first.get("strong") is True and first.get("text") == prefix:
            continue
        if not isinstance(first, str) or not first.startswith(prefix):
            raise ValueError(f"Cox axioms label changed: {child['id']}")
        child["segments"][0:1] = [{"strong": True, "text": prefix}, first[len(prefix):]]
    blocks[box_start:box_start + 7] = [{
        "id": "box-2-4", "kind": "box", "pdfPage": 38, "page": 5,
        "outlined": True, "blocks": box_children,
    }]
    chapter = {
        "schemaVersion": 2,
        "bookId": "mackay-information-theory-2003",
        "title": blocks[0]["text"],
        "sourcePdfPages": [34, args.through],
        "toc": toc,
        "blocks": blocks,
    }
    suffix = "draft" if args.through == 58 else "partial"
    output = BOOK / f"chapter-02.{suffix}.json"
    output.write_text(json.dumps(chapter, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(f"Wrote {output}: {len(blocks)} blocks, {len(toc)} sections, {len(numbers)} numbered formulas")


if __name__ == "__main__":
    main()
