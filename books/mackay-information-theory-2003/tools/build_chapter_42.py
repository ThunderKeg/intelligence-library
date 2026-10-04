"""Compile the visually checked MacKay chapter 42 into an unpublished draft."""

import importlib.util
import json
import re
from pathlib import Path


BOOK = Path(__file__).resolve().parents[1]
PARSER = Path(__file__).with_name("build_chapter_01.py")
SPEC = importlib.util.spec_from_file_location("mackay_chapter_builder_42", PARSER)
BUILDER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(BUILDER)
SOURCE = BOOK / "translation" / "chapter-42"
ASSETS = BOOK / "assets" / "chapter-42"
OUTPUT = BOOK / "chapter-42.draft.json"
PAGES = range(517, 534)
HEADING = re.compile(r"^(42\.\d+)\s+(.+)$")
IMAGE = re.compile(r"^\.\./\.\./assets/chapter-42/([\w.-]+\.png)$")
IMAGES = {path.name for path in ASSETS.glob("figure-42-*.png")}


def image_path(source: str) -> str:
    match = IMAGE.fullmatch(source)
    if not match or match.group(1) not in IMAGES:
        raise ValueError(f"Unexpected chapter 42 image path: {source}")
    path = ASSETS / match.group(1)
    if not path.is_file():
        raise FileNotFoundError(path)
    return f"assets/chapter-42/{match.group(1)}"


def preserve_title(block: dict) -> None:
    parts = ("第 42 章　", "Hopfield 网络")
    if block["text"] != "".join(parts):
        raise ValueError(f"Unexpected chapter title: {block['text']}")
    block["html"] = "<h1>" + "".join(
        f'<span class="mackay-ch42-title-part" style="white-space:nowrap">{part}</span>'
        for part in parts
    ) + "</h1>"


def outline_algorithm(blocks: list[dict]) -> None:
    """Keep algorithm 42.9 in its original full-border code frame."""
    positions = [i for i, block in enumerate(blocks)
                 if block["pdfPage"] == 528 and block["kind"] == "code"]
    if len(positions) != 1:
        raise ValueError(f"Expected one algorithm code block on PDF 528: {positions}")
    index = positions[0]
    caption = blocks[index + 1]
    if caption["kind"] != "paragraph" or not caption["text"].startswith("算法 42.9"):
        raise ValueError("Missing algorithm 42.9 caption")
    blocks[index] = {
        "id": "box-42-algorithm-42-9",
        "kind": "box", "pdfPage": 528, "page": 12,
        "outlined": True, "algorithm": True, "blocks": [blocks[index]],
    }


def main() -> None:
    if len(IMAGES) != 18:
        raise ValueError(f"Expected 18 source image assets, found {len(IMAGES)}")
    blocks = [
        block
        for page in PAGES
        for block in BUILDER.compile_page(
            page,
            source=SOURCE / f"pdf-{page}.md",
            image_resolver=image_path,
            chapter_start=517,
            chapter_number=42,
        )
    ]
    if blocks[0]["kind"] != "heading" or blocks[0]["level"] != 1:
        raise ValueError("Chapter 42 title is missing")
    preserve_title(blocks[0])
    if sum(block["kind"] == "intro" for block in blocks) != 1:
        raise ValueError("Chapter 42 needs one marked editor introduction")
    BUILDER.compile_math(blocks)
    outline_algorithm(blocks)
    for block in blocks:
        if block["kind"] == "figure" and block["width"] >= 400:
            block["wide"] = True
    sections = [block for block in blocks if block["kind"] == "heading" and block["level"] == 2]
    section_numbers = [HEADING.match(block["text"]).group(1) for block in sections]
    if section_numbers != [f"42.{number}" for number in range(1, 12)]:
        raise ValueError(f"Section order error: {section_numbers}")
    numbered = [block["number"] for block in blocks
                if block["kind"] == "formula" and block["number"]]
    if numbered != [f"(42.{number})" for number in range(1, 36)]:
        raise ValueError(f"Formula sequence error: {numbered}")
    figures = [block for block in blocks if block["kind"] == "figure"]
    if len(figures) != len(IMAGES) or {Path(block["src"]).name for block in figures} != IMAGES:
        raise ValueError("One or more source graphics missing")
    if sum(block["kind"] == "box" and block.get("algorithm") for block in blocks) != 1:
        raise ValueError("Outlined algorithm 42.9 is required")
    exercises = [block["label"] for block in blocks if block["kind"] == "exercise"]
    if [re.search(r"42\.\d+", label).group() for label in exercises] != [
            f"42.{number}" for number in range(1, 13)]:
        raise ValueError(f"Exercise sequence error: {exercises}")
    if sum(block.get("recommendedIcon", "").endswith("exercise-rat.png")
           for block in blocks) != 4:
        raise ValueError("Four recommended exercise icons are required")
    toc = [{"number": "42", "title": "Hopfield 网络", "block": blocks[0]["id"]}]
    for block in sections:
        match = HEADING.match(block["text"])
        toc.append({"number": match.group(1), "title": match.group(2), "block": block["id"]})
    chapter = {
        "schemaVersion": 2,
        "bookId": "mackay-information-theory-2003",
        "title": blocks[0]["text"],
        "sourcePdfPages": [517, 533],
        "toc": toc,
        "blocks": blocks,
    }
    OUTPUT.write_text(json.dumps(chapter, ensure_ascii=False, separators=(",", ":")),
                      encoding="utf-8")
    print(f"Wrote {OUTPUT}: {len(blocks)} blocks, {len(toc)} TOC entries")


if __name__ == "__main__":
    main()
