"""Compile the visually checked MacKay chapter 37 into an unpublished draft."""

import importlib.util
import json
import re
from pathlib import Path


BOOK = Path(__file__).resolve().parents[1]
PARSER = Path(__file__).with_name("build_chapter_01.py")
SPEC = importlib.util.spec_from_file_location("mackay_chapter_builder_37", PARSER)
BUILDER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(BUILDER)
SOURCE = BOOK / "translation" / "chapter-37"
ASSETS = BOOK / "assets" / "chapter-37"
OUTPUT = BOOK / "chapter-37.draft.json"
PAGES = range(469, 479)
HEADING = re.compile(r"^(37\.\d+)\s+(.+)$")
IMAGE = re.compile(r"^\.\./\.\./assets/chapter-37/([\w.-]+\.png)$")
IMAGES = [f"figure-37-{number}.png" for number in range(1, 5)]


def image_path(source: str) -> str:
    match = IMAGE.fullmatch(source)
    if not match or match.group(1) not in IMAGES:
        raise ValueError(f"Unexpected chapter 37 image path: {source}")
    path = ASSETS / match.group(1)
    if not path.is_file():
        raise FileNotFoundError(path)
    return f"assets/chapter-37/{match.group(1)}"


def group_chapter_title(block: dict) -> None:
    parts = ("第 37 章　", "贝叶斯推断", "与抽样理论")
    if block["text"] != "".join(parts):
        raise ValueError(f"Chapter 37 title changed unexpectedly: {block['text']}")
    block["html"] = "<h1>" + "".join(
        f'<span class="mackay-ch37-title-part">{part}</span>' for part in parts
    ) + "</h1>"


def main() -> None:
    blocks = [
        block
        for page in PAGES
        for block in BUILDER.compile_page(
            page,
            source=SOURCE / f"pdf-{page}.md",
            image_resolver=image_path,
            chapter_start=469,
            chapter_number=37,
        )
    ]
    if blocks[0]["kind"] != "heading" or blocks[0]["level"] != 1:
        raise ValueError("Chapter 37 title is missing")
    group_chapter_title(blocks[0])
    if sum(block["kind"] == "intro" for block in blocks) != 1:
        raise ValueError("Chapter 37 needs one clearly marked editor introduction")

    sections = [block for block in blocks
                if block["kind"] == "heading" and block["level"] == 2]
    section_numbers = [HEADING.match(block["text"]).group(1) for block in sections]
    if section_numbers != [f"37.{number}" for number in range(1, 6)]:
        raise ValueError(f"Chapter 37 sections missing or out of order: {section_numbers}")
    subheads = [block for block in blocks
                if block["kind"] == "heading" and block["level"] == 3]
    if [block["text"] for block in subheads] != ["延伸阅读"]:
        raise ValueError("Chapter 37 further-reading heading is missing")

    numbered = [block["number"] for block in blocks
                if block["kind"] == "formula" and block["number"]]
    if numbered != [f"(37.{number})" for number in range(1, 33)]:
        raise ValueError(f"Chapter 37 numbered formulas missing or out of order: {numbered}")
    unnumbered = [block for block in blocks
                  if block["kind"] == "formula" and not block["number"]]
    if [block["pdfPage"] for block in unnumbered] != [470, 470, 474]:
        raise ValueError("Chapter 37's three unnumbered displays are missing")

    figures = [block for block in blocks if block["kind"] == "figure"]
    if [Path(block["src"]).name for block in figures] != IMAGES:
        raise ValueError("Chapter 37 figures missing or out of order")
    for number, figure in enumerate(figures, 1):
        if figure["pdfPage"] != 473 or not figure.get("caption", "").startswith(f"图 37.{number}。"):
            raise ValueError(f"Figure 37.{number} or its caption missing")
        figure["wide"] = True

    tables = [block for block in blocks if block["kind"] == "table"]
    if len(tables) != 1 or tables[0]["pdfPage"] != 473:
        raise ValueError("Chapter 37 model-comparison data table missing")
    if [len(row) for row in tables[0]["rows"]] != [3, 3, 3, 3]:
        raise ValueError("Chapter 37 model-comparison data table malformed")
    cell_texts = [[cell["text"] for cell in row] for row in tables[0]["rows"]]
    if cell_texts != [
        ["接种方案", "A", "B"],
        ["患病", "1", "0"],
        ["未患病", "0", "1"],
        ["接受方案的总人数", "1", "1"],
    ]:
        raise ValueError(f"Chapter 37 table cell content changed: {cell_texts}")

    exercises = [block for block in blocks if block["kind"] == "exercise"]
    exercise_numbers = [re.search(r"37\.\d+", block["label"]).group()
                        for block in exercises]
    if exercise_numbers != [f"37.{number}" for number in range(1, 4)]:
        raise ValueError(f"Chapter 37 exercises missing or out of order: {exercise_numbers}")
    recommended = [block["label"] for block in exercises if block.get("recommendedIcon")]
    if recommended != ["习题 37.1"]:
        raise ValueError(f"Chapter 37 rat-icon exercise missing: {recommended}")
    marked = [block["label"] for block in exercises if block["label"].startswith("▷")]
    if marked != ["▷ 习题 37.2", "▷ 习题 37.3"]:
        raise ValueError(f"Chapter 37 triangle exercise markers missing: {marked}")
    lists = [block for block in blocks if block["kind"] == "list"]
    if len(lists) != 1 or not lists[0]["ordered"] or len(lists[0]["items"]) != 2:
        raise ValueError("Chapter 37 two-point confidence-interval conclusion missing")
    if any(block["kind"] in {"footnote", "code", "box", "quote", "caption"} for block in blocks):
        raise ValueError("Chapter 37 includes an unexpected footnote, code, box, quote, or loose caption")

    toc = [{"number": "37", "title": "贝叶斯推断与抽样理论", "block": blocks[0]["id"]}]
    for block in sections:
        match = HEADING.match(block["text"])
        toc.append({"number": match.group(1), "title": match.group(2), "block": block["id"]})
    BUILDER.compile_math(blocks)
    chapter = {
        "schemaVersion": 2,
        "bookId": "mackay-information-theory-2003",
        "title": blocks[0]["text"],
        "sourcePdfPages": [469, 478],
        "toc": toc,
        "blocks": blocks,
    }
    OUTPUT.write_text(json.dumps(chapter, ensure_ascii=False, separators=(",", ":")),
                      encoding="utf-8")
    print(f"Wrote {OUTPUT}: {len(blocks)} blocks, {len(toc)} TOC entries, "
          f"{len(numbered)} numbered + {len(unnumbered)} unnumbered formulas, "
          f"{len(figures)} figures, {len(exercises)} exercises, 1 table, 1 list")


if __name__ == "__main__":
    main()
