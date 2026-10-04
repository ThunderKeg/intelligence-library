"""Compile the page-checked MacKay chapter 27 into an unpublished draft."""

import importlib.util
import json
import re
from pathlib import Path


BOOK = Path(__file__).resolve().parents[1]
PARSER = Path(__file__).with_name("build_chapter_01.py")
SPEC = importlib.util.spec_from_file_location("mackay_chapter_builder_27", PARSER)
BUILDER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(BUILDER)
SOURCE = BOOK / "translation" / "chapter-27"
ASSETS = BOOK / "assets" / "chapter-27"
OUTPUT = BOOK / "chapter-27.draft.json"
PAGES = range(353, 355)
IMAGE = re.compile(r"^\.\./\.\./assets/chapter-27/(laplace-approximation-diagram\.png)$")


def image_path(source: str) -> str:
    match = IMAGE.fullmatch(source)
    if not match:
        raise ValueError(f"Unexpected chapter 27 image path: {source}")
    path = ASSETS / match.group(1)
    if not path.is_file():
        raise FileNotFoundError(path)
    return f"assets/chapter-27/{match.group(1)}"


def main() -> None:
    blocks = [
        block
        for page in PAGES
        for block in BUILDER.compile_page(
            page, source=SOURCE / f"pdf-{page}.md", image_resolver=image_path,
            chapter_start=353, chapter_number=27,
        )
    ]
    if blocks[0]["kind"] != "heading" or blocks[0]["level"] != 1:
        raise ValueError("Chapter 27 title is missing")
    if sum(block["kind"] == "intro" for block in blocks) != 1:
        raise ValueError("Chapter 27 needs one clearly marked editor introduction")
    sections = [block for block in blocks if block["kind"] == "heading" and block["level"] == 2]
    if [block["text"].split()[0] for block in sections] != ["27.1"]:
        raise ValueError(f"Chapter 27 sections missing or out of order: {sections}")
    numbers = [block["number"] for block in blocks if block["kind"] == "formula" and block["number"]]
    if numbers != [f"(27.{i})" for i in range(1, 15)]:
        raise ValueError(f"Chapter 27 formulas missing or out of order: {numbers}")
    exercises = [block["label"] for block in blocks if block["kind"] == "exercise"]
    if [re.search(r"27\.\d+", label).group() for label in exercises] != ["27.1", "27.2", "27.3"]:
        raise ValueError(f"Chapter 27 exercises missing or out of order: {exercises}")
    images = [block for block in blocks if block["kind"] == "figure"]
    if len(images) != 1 or Path(images[0]["src"]).name != "laplace-approximation-diagram.png":
        raise ValueError(f"Unexpected chapter 27 images: {[block['src'] for block in images]}")
    toc = [
        {"number": "27", "title": "拉普拉斯方法", "block": blocks[0]["id"]},
        {"number": "27.1", "title": "习题", "block": sections[0]["id"]},
    ]
    BUILDER.compile_math(blocks)
    chapter = {
        "schemaVersion": 2,
        "bookId": "mackay-information-theory-2003",
        "title": blocks[0]["text"],
        "sourcePdfPages": [353, 354],
        "toc": toc,
        "blocks": blocks,
    }
    OUTPUT.write_text(json.dumps(chapter, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(f"Wrote {OUTPUT}: {len(blocks)} blocks, {len(toc)} TOC entries, "
          f"{len(numbers)} numbered formulas, {len(images)} source image, "
          f"{len(exercises)} exercises")


if __name__ == "__main__":
    main()
