"""Compile the page-checked MacKay chapter 22 into an unpublished draft."""

import importlib.util
import json
import re
from pathlib import Path


BOOK = Path(__file__).resolve().parents[1]
PARSER = Path(__file__).with_name("build_chapter_01.py")
SPEC = importlib.util.spec_from_file_location("mackay_chapter_builder_22", PARSER)
BUILDER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(BUILDER)
SOURCE = BOOK / "translation" / "chapter-22"
ASSETS = BOOK / "assets" / "chapter-22"
OUTPUT = BOOK / "chapter-22.draft.json"
PAGES = range(312, 323)
IMAGE = re.compile(r"^\.\./\.\./assets/chapter-22/([\w.-]+\.png)$")
HEADING = re.compile(r"^(22\.\d+)\s+(.+)$")
IMAGES = {
    "figure-22-1.png", "figure-22-3a.png", "figure-22-3b.png",
    "figure-22-5.png", "figure-22-6.png", "figure-22-7.png",
    "figure-22-8.png", "figure-22-9.png", "figure-22-10.png",
    "exercise-22-5-data.png", "exercise-22-10-window.png",
}


def image_path(source: str) -> str:
    match = IMAGE.fullmatch(source)
    if not match or match.group(1) not in IMAGES:
        raise ValueError(f"Unexpected chapter 22 image path: {source}")
    path = ASSETS / match.group(1)
    if not path.is_file():
        raise FileNotFoundError(path)
    return f"assets/chapter-22/{match.group(1)}"


def algorithm_box(blocks: list[dict], *, first: str | None,
                  first_number: str | None, caption: str, number: int) -> list[dict]:
    if first:
        start = next(index for index, block in enumerate(blocks)
                     if block["pdfPage"] == 316 and block["kind"] == "paragraph"
                     and block["text"].startswith(first))
    else:
        start = next(index for index, block in enumerate(blocks)
                     if block["pdfPage"] == 316 and block["kind"] == "formula"
                     and block["number"] == first_number)
    end = next(index for index, block in enumerate(blocks)
               if block["pdfPage"] == 316 and block["kind"] == "paragraph"
               and block["text"].startswith(caption))
    children = blocks[start:end]
    if not children or any(block["pdfPage"] != 316 for block in children):
        raise ValueError(f"Unexpected algorithm {number} extent")
    expected = (range(22, 27) if number == 2 else range(27, 29))
    formulas = [block["number"] for block in children if block["kind"] == "formula"]
    if formulas != [f"(22.{index})" for index in expected]:
        raise ValueError(f"Algorithm {number} formula set: {formulas}")
    box = {
        "id": f"box-22-{number}", "kind": "box", "pdfPage": 316,
        "page": 5, "outlined": True, "blocks": children,
    }
    label = {**blocks[end], "kind": "caption"}
    return blocks[:start] + [box, label] + blocks[end + 1:]


def main() -> None:
    blocks = [
        block
        for page in PAGES
        for block in BUILDER.compile_page(
            page, source=SOURCE / f"pdf-{page}.md", image_resolver=image_path,
            chapter_start=312, chapter_number=22,
        )
    ]
    if blocks[0]["kind"] != "heading" or blocks[0]["level"] != 1:
        raise ValueError("Chapter 22 title is missing")
    if sum(block["kind"] == "intro" for block in blocks) != 1:
        raise ValueError("Chapter 22 needs one clearly marked editor introduction")
    sections = [block for block in blocks if block["kind"] == "heading" and block["level"] == 2]
    if [HEADING.match(block["text"]).group(1) for block in sections] != [f"22.{i}" for i in range(1, 7)]:
        raise ValueError(f"Chapter 22 sections missing or out of order: {sections}")
    formulas = [block for block in blocks if block["kind"] == "formula"]
    numbers = [block["number"] for block in formulas if block["number"]]
    if numbers != [f"(22.{i})" for i in range(1, 42)]:
        raise ValueError(f"Chapter 22 formulas missing or out of order: {numbers}")
    exercises = [block["label"] for block in blocks if block["kind"] == "exercise"]
    if [re.search(r"22\.\d+", label).group() for label in exercises] != [f"22.{i}" for i in range(4, 17)]:
        raise ValueError(f"Chapter 22 exercises missing or out of order: {exercises}")
    images = [block for block in blocks if block["kind"] == "figure"]
    if {Path(block["src"]).name for block in images} != IMAGES or len(images) != len(IMAGES):
        raise ValueError(f"Unexpected chapter 22 image set: {[block['src'] for block in images]}")
    for block in images:
        if block["width"] >= 800:
            block["wide"] = True
    tables = [block for block in blocks if block["kind"] == "table"]
    if len(tables) != 1 or len(tables[0]["rows"]) != 8:
        raise ValueError("Figure 22.9 transcription needs header and seven scientist rows")

    toc = [{"number": "22", "title": "最大似然与聚类", "block": blocks[0]["id"]}]
    for block in sections:
        match = HEADING.match(block["text"])
        toc.append({"number": match.group(1), "title": match.group(2), "block": block["id"]})
    BUILDER.compile_math(blocks)
    blocks = algorithm_box(blocks, first="分配步骤。", first_number=None,
                           caption="算法 22.2", number=2)
    blocks = algorithm_box(blocks, first=None, first_number="(22.27)",
                           caption="算法 22.4", number=4)
    chapter = {
        "schemaVersion": 2,
        "bookId": "mackay-information-theory-2003",
        "title": blocks[0]["text"],
        "sourcePdfPages": [312, 322],
        "toc": toc,
        "blocks": blocks,
    }
    OUTPUT.write_text(json.dumps(chapter, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(f"Wrote {OUTPUT}: {len(blocks)} blocks, {len(toc)} TOC entries, "
          f"{len(numbers)} numbered formulas, {len(images)} source images, "
          f"{len(exercises)} exercises, {len(tables)} table")


if __name__ == "__main__":
    main()
