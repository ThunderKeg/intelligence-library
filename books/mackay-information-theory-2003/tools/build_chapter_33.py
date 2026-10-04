"""Compile the page-checked MacKay chapter 33 into an unpublished draft."""

import importlib.util
import json
import re
from pathlib import Path


BOOK = Path(__file__).resolve().parents[1]
PARSER = Path(__file__).with_name("build_chapter_01.py")
SPEC = importlib.util.spec_from_file_location("mackay_chapter_builder_33", PARSER)
BUILDER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(BUILDER)
SOURCE = BOOK / "translation" / "chapter-33"
ASSETS = BOOK / "assets" / "chapter-33"
OUTPUT = BOOK / "chapter-33.draft.json"
PAGES = range(434, 449)
HEADING = re.compile(r"^(33\.\d+)\s+(.+)$")
IMAGE = re.compile(r"^\.\./\.\./assets/chapter-33/([\w.-]+\.png)$")
IMAGES = [f"figure-33-{number}.png" for number in range(1, 7)]
CONCLUSION = "由变分自由能最小化得到的近似分布，总是倾向于比真实分布更加集中。"


def image_path(source: str) -> str:
    match = IMAGE.fullmatch(source)
    if not match or match.group(1) not in IMAGES:
        raise ValueError(f"Unexpected chapter 33 image path: {source}")
    path = ASSETS / match.group(1)
    if not path.is_file():
        raise FileNotFoundError(path)
    return f"assets/chapter-33/{match.group(1)}"


def outline_conclusion(blocks: list[dict]) -> list[dict]:
    """Preserve the source's four-sided conclusion box without quote styling."""
    indices = [index for index, block in enumerate(blocks)
               if block["pdfPage"] == 443 and block["kind"] == "quote"
               and block["text"] == CONCLUSION]
    if len(indices) != 1:
        raise ValueError(f"PDF443 outlined conclusion missing or duplicated: {indices}")
    index = indices[0]
    paragraph = dict(blocks[index])
    paragraph["kind"] = "paragraph"
    box = {
        "id": "box-33-concentration",
        "kind": "box",
        "pdfPage": 443,
        "page": 10,
        "outlined": True,
        "blocks": [paragraph],
    }
    return blocks[:index] + [box] + blocks[index + 1:]


def main() -> None:
    blocks = [
        block
        for page in PAGES
        for block in BUILDER.compile_page(
            page,
            source=SOURCE / f"pdf-{page}.md",
            image_resolver=image_path,
            chapter_start=434,
            chapter_number=33,
        )
    ]
    if blocks[0]["kind"] != "heading" or blocks[0]["level"] != 1:
        raise ValueError("Chapter 33 title is missing")
    if sum(block["kind"] == "intro" for block in blocks) != 1:
        raise ValueError("Chapter 33 needs one clearly marked editor introduction")
    sections = [block for block in blocks
                if block["kind"] == "heading" and block["level"] == 2]
    section_numbers = [HEADING.match(block["text"]).group(1) for block in sections]
    if section_numbers != [f"33.{number}" for number in range(1, 11)]:
        raise ValueError(f"Chapter 33 sections missing or out of order: {section_numbers}")
    numbered = [block["number"] for block in blocks
                if block["kind"] == "formula" and block["number"]]
    if numbered != [f"(33.{number})" for number in range(1, 63)]:
        raise ValueError(f"Chapter 33 numbered formulas missing or out of order: {numbered}")
    unnumbered = [block for block in blocks
                  if block["kind"] == "formula" and not block["number"]]
    if [block["pdfPage"] for block in unnumbered] != [446, 446, 447]:
        raise ValueError("Chapter 33's three unnumbered display equations are missing")
    exercises = [block for block in blocks if block["kind"] == "exercise"]
    exercise_numbers = [re.search(r"33\.\d+", block["label"]).group()
                        for block in exercises]
    if exercise_numbers != [f"33.{number}" for number in range(1, 8)]:
        raise ValueError(f"Chapter 33 exercises missing or out of order: {exercise_numbers}")
    recommended = [block["label"] for block in exercises if block.get("recommendedIcon")]
    if recommended != [f"习题 33.{number}" for number in (1, 5, 6, 7)]:
        raise ValueError(f"Chapter 33 rat-icon exercises missing: {recommended}")
    marked = [block["label"] for block in exercises if block["label"].startswith("▷")]
    if marked != ["▷ 习题 33.2", "▷ 习题 33.3"]:
        raise ValueError(f"Chapter 33 triangle exercise markers missing: {marked}")
    figures = [block for block in blocks if block["kind"] == "figure"]
    names = [Path(block["src"]).name for block in figures]
    if names != IMAGES:
        raise ValueError(f"Chapter 33 figures missing or out of order: {names}")
    if any(not block.get("caption", "").startswith(f"图 33.{index}。")
           for index, block in enumerate(figures, start=1)):
        raise ValueError("Chapter 33 figure caption missing")
    for block in figures:
        if block["width"] >= 800:
            block["wide"] = True
    tables = [block for block in blocks if block["kind"] == "table"]
    if len(tables) != 1 or tables[0]["pdfPage"] != 446 or len(tables[0]["rows"]) != 5:
        raise ValueError("Exercise 33.7's 4x4 probability table is missing")
    if any(len(row) != 5 for row in tables[0]["rows"]):
        raise ValueError("Exercise 33.7 probability table has a missing cell")
    lists = [block for block in blocks if block["kind"] == "list"]
    if len(lists) != 1 or not lists[0]["ordered"] or len(lists[0]["items"]) != 2:
        raise ValueError("PDF437's two numbered reasons are missing")
    if any(block["kind"] in {"code", "footnote"} for block in blocks):
        raise ValueError("The source chapter 33 has no code or footnotes")
    toc = [{"number": "33", "title": "变分方法", "block": blocks[0]["id"]}]
    for block in sections:
        match = HEADING.match(block["text"])
        toc.append({"number": match.group(1), "title": match.group(2), "block": block["id"]})
    BUILDER.compile_math(blocks)
    blocks = outline_conclusion(blocks)
    if len([block for block in blocks if block["kind"] == "quote"]) != 1:
        raise ValueError("PDF443 student's question should remain an ordinary quotation")
    chapter = {
        "schemaVersion": 2,
        "bookId": "mackay-information-theory-2003",
        "title": blocks[0]["text"],
        "sourcePdfPages": [434, 448],
        "toc": toc,
        "blocks": blocks,
    }
    OUTPUT.write_text(json.dumps(chapter, ensure_ascii=False, separators=(",", ":")),
                      encoding="utf-8")
    print(f"Wrote {OUTPUT}: {len(blocks)} top-level blocks, {len(toc)} TOC entries, "
          f"{len(numbered)} numbered + {len(unnumbered)} unnumbered formulas, "
          f"{len(figures)} figures, {len(exercises)} exercises, 1 table, "
          "1 outlined conclusion")


if __name__ == "__main__":
    main()
