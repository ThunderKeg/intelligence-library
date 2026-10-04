"""Compile the visually checked MacKay chapter 39 into an unpublished draft."""

import importlib.util
import json
import re
from pathlib import Path


BOOK = Path(__file__).resolve().parents[1]
PARSER = Path(__file__).with_name("build_chapter_01.py")
SPEC = importlib.util.spec_from_file_location("mackay_chapter_builder_39", PARSER)
BUILDER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(BUILDER)
SOURCE = BOOK / "translation" / "chapter-39"
ASSETS = BOOK / "assets" / "chapter-39"
OUTPUT = BOOK / "chapter-39.draft.json"
PAGES = range(483, 494)
HEADING = re.compile(r"^(39\.\d+)\s+(.+)$")
IMAGE = re.compile(r"^\.\./\.\./assets/chapter-39/([\w.-]+\.png)$")
IMAGES = {
    "figure-39-1.png", "activation-logistic.png", "activation-tanh.png",
    "activation-threshold.png", "figure-39-2.png", "figure-39-3.png",
    "figure-39-4.png", "figure-39-6.png", "exercise-39-5-led.png",
    "table-39-7.png",
}


def image_path(source: str) -> str:
    match = IMAGE.fullmatch(source)
    if not match or match.group(1) not in IMAGES:
        raise ValueError(f"Unexpected chapter 39 image path: {source}")
    path = ASSETS / match.group(1)
    if not path.is_file():
        raise FileNotFoundError(path)
    return f"assets/chapter-39/{match.group(1)}"


def group_chapter_title(block: dict) -> None:
    parts = ("第 39 章　", "作为分类器的", "单个神经元")
    if block["text"] != "".join(parts):
        raise ValueError(f"Unexpected chapter title: {block['text']}")
    block["html"] = "<h1>" + "".join(
        f'<span class="mackay-ch39-title-part">{part}</span>' for part in parts
    ) + "</h1>"


def preserve_special_layout(blocks: list[dict]) -> list[dict]:
    # The LED table is a graphic table: keep every original segment shape as a
    # source crop and attach the translated table caption to that image.
    table_positions = [i for i, block in enumerate(blocks)
                       if block["kind"] == "figure" and
                       block["src"] == "assets/chapter-39/table-39-7.png"]
    if len(table_positions) != 1:
        raise ValueError(f"Table 39.7 image missing or duplicated: {table_positions}")
    table_index = table_positions[0]
    caption = blocks[table_index + 1]
    if caption["kind"] != "paragraph" or not caption["text"].startswith("表 39.7"):
        raise ValueError("Table 39.7 caption missing")
    blocks[table_index]["caption"] = caption["text"]
    blocks[table_index]["captionSegments"] = caption["segments"]
    del blocks[table_index + 1]

    # The batch-learning directions and three displayed formulae form one
    # four-sided box in the printed source.
    starts = [i for i, block in enumerate(blocks)
              if block["pdfPage"] == 488 and block["kind"] == "paragraph" and
              block["text"].startswith("对每一对输入／目标值")]
    ends = [i for i, block in enumerate(blocks)
            if block["pdfPage"] == 488 and block["kind"] == "formula" and
            block["number"] == "(39.20)"]
    if len(starts) != 1 or len(ends) != 1 or ends[0] - starts[0] != 5:
        raise ValueError(f"Batch learning box malformed: {starts}, {ends}")
    start, end = starts[0], ends[0]
    members = blocks[start:end + 1]
    if [block.get("number") for block in members if block["kind"] == "formula"] != [
            "(39.18)", "(39.19)", "(39.20)"]:
        raise ValueError("Batch learning box formulas incomplete")
    blocks[start:end + 1] = [{
        "id": "box-39-batch-learning", "kind": "box", "pdfPage": 488,
        "page": 6, "outlined": True, "blocks": members,
    }]

    # The Octave listing has its own printed border; the prose caption is
    # outside that border in the source.
    code_positions = [i for i, block in enumerate(blocks)
                      if block["pdfPage"] == 490 and block["kind"] == "code"]
    if len(code_positions) != 1:
        raise ValueError(f"Algorithm 39.5 listing missing: {code_positions}")
    index = code_positions[0]
    code = blocks[index]
    if "endfunction" not in code["text"] or "g = - x' * e" not in code["text"]:
        raise ValueError("Algorithm 39.5 code incomplete")
    blocks[index] = {
        "id": "box-39-algorithm-39-5", "kind": "box", "pdfPage": 490,
        "page": 8, "outlined": True, "algorithm": True, "blocks": [code],
    }
    return blocks


def walk(blocks: list[dict]):
    for block in blocks:
        if block["kind"] == "box":
            yield from walk(block["blocks"])
        else:
            yield block


def main() -> None:
    blocks = [
        block
        for page in PAGES
        for block in BUILDER.compile_page(
            page,
            source=SOURCE / f"pdf-{page}.md",
            image_resolver=image_path,
            chapter_start=483,
            chapter_number=39,
        )
    ]
    if blocks[0]["kind"] != "heading" or blocks[0]["level"] != 1:
        raise ValueError("Chapter 39 title is missing")
    group_chapter_title(blocks[0])
    if sum(block["kind"] == "intro" for block in blocks) != 1:
        raise ValueError("Chapter 39 needs one marked editor introduction")
    # Compile while every formula and segment is top-level; the shared
    # converter does not descend into nested source-layout boxes.
    BUILDER.compile_math(blocks)
    blocks = preserve_special_layout(blocks)
    flat = list(walk(blocks))
    for block in flat:
        if block["kind"] == "figure" and (block["width"] >= 560 or
                                           block["src"] == "assets/chapter-39/figure-39-1.png"):
            block["wide"] = True
    sections = [block for block in flat if block["kind"] == "heading" and block["level"] == 2]
    section_numbers = [HEADING.match(block["text"]).group(1) for block in sections]
    if section_numbers != [f"39.{number}" for number in range(1, 6)]:
        raise ValueError(f"Section order error: {section_numbers}")
    numbered = [block["number"] for block in flat
                if block["kind"] == "formula" and block["number"]]
    if numbered != [f"(39.{number})" for number in range(1, 28)]:
        raise ValueError(f"Formula sequence error: {numbered}")
    if sum(block["kind"] == "formula" and not block["number"] for block in flat) != 1:
        raise ValueError("Chapter 39 needs one unnumbered formula from PDF493")
    if sum(block["kind"] == "figure" for block in flat) != len(IMAGES):
        raise ValueError("One or more source graphics missing")
    exercises = [block["label"] for block in flat if block["kind"] == "exercise"]
    if [re.search(r"39\.\d+", label).group() for label in exercises] != [
            f"39.{number}" for number in range(1, 7)]:
        raise ValueError(f"Exercise sequence error: {exercises}")
    toc = [{"number": "39", "title": "作为分类器的单个神经元", "block": blocks[0]["id"]}]
    for block in sections:
        match = HEADING.match(block["text"])
        toc.append({"number": match.group(1), "title": match.group(2), "block": block["id"]})
    chapter = {
        "schemaVersion": 2,
        "bookId": "mackay-information-theory-2003",
        "title": blocks[0]["text"],
        "sourcePdfPages": [483, 493],
        "toc": toc,
        "blocks": blocks,
    }
    OUTPUT.write_text(json.dumps(chapter, ensure_ascii=False, separators=(",", ":")),
                      encoding="utf-8")
    print(f"Wrote {OUTPUT}: {len(blocks)} top-level blocks, {len(toc)} TOC entries")


if __name__ == "__main__":
    main()
