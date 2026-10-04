"""Compile the PDF-checked chapter 29 body into an unpublished reader draft."""

import importlib.util
import json
import re
from pathlib import Path


BOOK = Path(__file__).resolve().parents[1]
PARSER = Path(__file__).with_name("build_chapter_01.py")
SPEC = importlib.util.spec_from_file_location("mackay_chapter_builder_29", PARSER)
BUILDER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(BUILDER)
SOURCE = BOOK / "translation" / "chapter-29"
ASSETS = BOOK / "assets" / "chapter-29"
OUTPUT = BOOK / "chapter-29.draft.json"
PAGES = range(369, 399)
HEADING = re.compile(r"^(29\.\d+)\s+(.+)$")
IMAGE = re.compile(r"^\.\./\.\./assets/chapter-29/(figure-29-\d+\.png)$")
FIGURES = {f"figure-29-{number}.png" for number in range(1, 21)}
EXERCISES = [f"29.{number}" for number in range(1, 22) if number != 6]


def image_path(source: str) -> str:
    match = IMAGE.fullmatch(source)
    if not match or match.group(1) not in FIGURES:
        raise ValueError(f"Unexpected chapter 29 image path: {source}")
    path = ASSETS / match.group(1)
    if not path.is_file():
        raise FileNotFoundError(path)
    return f"assets/chapter-29/{match.group(1)}"


def outline(blocks: list[dict], first: int, last: int, box_id: str) -> list[dict]:
    children = blocks[first:last + 1]
    if not children or len({child["pdfPage"] for child in children}) != 1:
        raise ValueError(f"Invalid outlined box {box_id}")
    page = children[0]["pdfPage"]
    return blocks[:first] + [{
        "id": box_id,
        "kind": "box",
        "pdfPage": page,
        "page": page - 368,
        "outlined": True,
        "blocks": children,
    }] + blocks[last + 1:]


def wrap_source_boxes(blocks: list[dict]) -> list[dict]:
    """Keep the seven original outlined units, including formula (29.32)."""
    quotes370 = [i for i, block in enumerate(blocks)
                 if block["pdfPage"] == 370 and block["kind"] == "quote"]
    if len(quotes370) != 1:
        raise ValueError(f"PDF 370 outlined quote count: {len(quotes370)}")
    blocks[quotes370[0]]["kind"] = "paragraph"
    blocks = outline(blocks, quotes370[0], quotes370[0], "box-29-370")

    quote379 = [i for i, block in enumerate(blocks)
                if block["pdfPage"] == 379 and block["kind"] == "quote"]
    if len(quote379) != 2 or quote379[1] != quote379[0] + 2:
        raise ValueError(f"PDF 379 outlined rule segments: {quote379}")
    middle = blocks[quote379[0] + 1]
    if middle["kind"] != "formula" or middle["number"] != "(29.32)":
        raise ValueError("Rule of thumb lost formula (29.32)")
    for index in quote379:
        blocks[index]["kind"] = "paragraph"
    blocks = outline(blocks, quote379[0], quote379[1], "box-29-379")

    for page, expected in ((387, 3), (390, 2)):
        code_ids = [block["id"] for block in blocks
                    if block["pdfPage"] == page and block["kind"] == "code"]
        if len(code_ids) != expected:
            raise ValueError(f"PDF {page} outlined algorithm count: {len(code_ids)}")
        for number, code_id in enumerate(code_ids, 1):
            index = next(i for i, block in enumerate(blocks) if block["id"] == code_id)
            blocks = outline(blocks, index, index, f"box-29-{page}-{number}")
    return blocks


def main() -> None:
    blocks = [
        block
        for page in PAGES
        for block in BUILDER.compile_page(
            page, source=SOURCE / f"pdf-{page}.md", image_resolver=image_path,
            chapter_start=369, chapter_number=29,
        )
    ]
    if blocks[0]["kind"] != "heading" or blocks[0]["level"] != 1:
        raise ValueError("Chapter 29 title is missing")
    if sum(block["kind"] == "intro" for block in blocks) != 1:
        raise ValueError("Chapter 29 needs one clearly marked editor introduction")
    sections = [block for block in blocks
                if block["kind"] == "heading" and block["level"] == 2]
    section_numbers = [HEADING.match(block["text"]).group(1) for block in sections]
    if section_numbers != [f"29.{number}" for number in range(1, 13)]:
        raise ValueError(f"Chapter 29 sections missing or out of order: {section_numbers}")
    numbers = [block["number"] for block in blocks
               if block["kind"] == "formula" and block["number"]]
    if numbers != [f"(29.{number})" for number in range(3, 63)]:
        raise ValueError(f"Chapter 29 formulas missing or out of order: {numbers}")
    exercises = [block["label"] for block in blocks if block["kind"] == "exercise"]
    exercise_numbers = [re.search(r"29\.\d+", label).group() for label in exercises]
    if exercise_numbers != EXERCISES:
        raise ValueError(f"Chapter 29 exercises missing or out of order: {exercises}")
    figures = [block for block in blocks if block["kind"] == "figure"]
    if {Path(block["src"]).name for block in figures} != FIGURES or len(figures) != 20:
        raise ValueError(f"Unexpected chapter 29 figure set: {[block['src'] for block in figures]}")
    for block in figures:
        if block["width"] >= 560:
            block["wide"] = True
    footnotes = [block["id"] for block in blocks if block["kind"] == "footnote"]
    if footnotes != ["fn-29-1", "fn-29-2", "fn-29-3"]:
        raise ValueError(f"Chapter 29 footnotes missing or out of order: {footnotes}")
    tables = [block for block in blocks if block["kind"] == "table"]
    if (len(tables) != 1 or tables[0]["pdfPage"] != 389
            or len(tables[0]["rows"]) != 5
            or any(len(row) != 2 for row in tables[0]["rows"])
            or tables[0]["rows"][4][0]["text"] != "N := randbits(l)"
            or "随机的" not in tables[0]["rows"][4][1]["text"]):
        raise ValueError("PDF 389 integer-operator table lost its two-column structure")
    lists385 = [block for block in blocks if block["pdfPage"] == 385
                and block["kind"] == "list" and block["ordered"]]
    if len(lists385) != 1 or len(lists385[0]["items"]) != 1:
        raise ValueError("PDF 385 must continue the two-item property list")
    lists385[0]["start"] = 2
    toc = [{"number": "29", "title": "蒙特卡罗方法", "block": blocks[0]["id"]}]
    for block in sections:
        match = HEADING.match(block["text"])
        toc.append({"number": match.group(1), "title": match.group(2), "block": block["id"]})
    BUILDER.compile_math(blocks)
    blocks = wrap_source_boxes(blocks)
    chapter = {
        "schemaVersion": 2,
        "bookId": "mackay-information-theory-2003",
        "title": blocks[0]["text"],
        "sourcePdfPages": [369, 398],
        "toc": toc,
        "blocks": blocks,
    }
    OUTPUT.write_text(json.dumps(chapter, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(f"Wrote {OUTPUT}: {len(blocks)} blocks, {len(toc)} TOC entries, "
          f"{len(numbers)} numbered formulas, {len(figures)} figures, "
          f"{len(exercises)} exercises, {len(footnotes)} footnotes, 7 outlined boxes")


if __name__ == "__main__":
    main()
