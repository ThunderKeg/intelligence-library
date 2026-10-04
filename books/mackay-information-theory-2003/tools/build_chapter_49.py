"""Compile visually checked MacKay chapter 49 into an unpublished draft."""

import importlib.util
import json
import re
from html import escape
from pathlib import Path


BOOK = Path(__file__).resolve().parents[1]
PARSER = Path(__file__).with_name("build_chapter_01.py")
SPEC = importlib.util.spec_from_file_location("mackay_chapter_builder_49", PARSER)
BUILDER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(BUILDER)
SOURCE = BOOK / "translation" / "chapter-49"
ASSETS = BOOK / "assets" / "chapter-49"
OUTPUT = BOOK / "chapter-49.draft.json"
PAGES = range(594, 600)
HEADING = re.compile(r"^(49\.\d+)\s+(.+)$")
IMAGE = re.compile(r"^\.\./\.\./assets/chapter-49/(figure-49-[1-9]\.png)$")
EXPECTED_IMAGES = {f"figure-49-{n}.png" for n in range(1, 10)}
TITLE = "第 49 章　重复—累积码"
SECTION_TITLES = (
    "49.1　编码器",
    "49.2　图表示法",
    "49.3　译码",
    "49.4　译码时间的经验分布",
    "49.5　广义奇偶校验矩阵",
)


def image_path(source: str) -> str:
    match = IMAGE.fullmatch(source)
    if not match or match.group(1) not in EXPECTED_IMAGES:
        raise ValueError(f"Unexpected chapter 49 image path: {source}")
    path = ASSETS / match.group(1)
    if not path.is_file():
        raise FileNotFoundError(path)
    return f"assets/chapter-49/{match.group(1)}"


def preserve_heading_design(blocks: list[dict]) -> None:
    first = blocks[0]
    if first["kind"] != "heading" or first["level"] != 1 or first["text"] != TITLE:
        raise ValueError("Chapter 49 title changed")
    number, title = "第 49 章　", "重复—累积码"
    first["html"] = (
        '<h1 style="text-align:center">'
        '<span style="display:block;border-bottom:3px solid currentColor;'
        'padding-bottom:.45em;margin-bottom:.45em">'
        f'{escape(number)}</span>'
        f'<span style="display:block;font-style:italic;white-space:nowrap">'
        f'{escape(title)}</span></h1>'
    )
    sections = [block for block in blocks if block["kind"] == "heading"
                and block["level"] == 2]
    if [block["text"] for block in sections] != list(SECTION_TITLES):
        raise ValueError(f"Chapter 49 section sequence changed: {[b['text'] for b in sections]}")
    for block in sections:
        number, title = block["text"].split("　", 1)
        block["html"] = (
            '<h2><span aria-hidden="true">▶</span> '
            f'<span style="white-space:nowrap">{escape(number)}</span>　'
            f'<span style="white-space:nowrap">{escape(title)}</span></h2>'
        )


def outline_encoder(blocks: list[dict]) -> list[dict]:
    """Keep the five printed steps and equation (49.1) inside one full frame."""
    starts = [i for i, block in enumerate(blocks)
              if block["pdfPage"] == 594 and block["kind"] == "list"
              and block["ordered"] and len(block["items"]) == 4]
    if len(starts) != 1:
        raise ValueError(f"Expected first four encoder steps: {starts}")
    start = starts[0]
    members = blocks[start:start + 3]
    if [block["kind"] for block in members] != ["list", "formula", "list"]:
        raise ValueError(f"Encoder outline has changed: {members}")
    if members[1]["number"] != "(49.1)" or not members[2]["ordered"] or len(members[2]["items"]) != 1:
        raise ValueError("Missing encoder recurrence or final fifth step")
    members[2]["start"] = 5
    box = {
        "id": "box-49-encoder", "kind": "box", "pdfPage": 594,
        "page": 1, "outlined": True, "blocks": members,
    }
    blocks[start:start + 3] = [box]
    return blocks


def walk(blocks: list[dict]):
    for block in blocks:
        if block["kind"] == "box":
            yield from walk(block["blocks"])
        else:
            yield block


def main() -> None:
    actual_images = {path.name for path in ASSETS.glob("*.png")}
    if actual_images != EXPECTED_IMAGES:
        raise ValueError(f"Chapter 49 asset set differs: {actual_images ^ EXPECTED_IMAGES}")
    blocks = [
        block for page in PAGES
        for block in BUILDER.compile_page(
            page, source=SOURCE / f"pdf-{page}.md", image_resolver=image_path,
            chapter_start=594, chapter_number=49,
        )
    ]
    if sum(block["kind"] == "intro" for block in blocks) != 1:
        raise ValueError("Chapter 49 needs exactly one marked editor introduction")
    # The shared MathML converter only visits top-level blocks.
    BUILDER.compile_math(blocks)
    preserve_heading_design(blocks)
    blocks = outline_encoder(blocks)
    flat = list(walk(blocks))
    for block in flat:
        if block["kind"] == "figure" and block["width"] >= 560:
            block["wide"] = True

    formulas = [block["number"] for block in flat if block["kind"] == "formula"
                and block["number"]]
    if formulas != [f"(49.{n})" for n in range(1, 12)]:
        raise ValueError(f"Formula sequence changed: {formulas}")
    figures = [block for block in flat if block["kind"] == "figure"]
    if len(figures) != 9 or {Path(block["src"]).name for block in figures} != EXPECTED_IMAGES:
        raise ValueError("Chapter 49 figures missing, duplicated or mislabeled")
    if any(not block.get("caption", "").startswith(f"图 49.{n}　")
           for n, block in enumerate(figures, 1)):
        raise ValueError("One or more source figure captions missing")
    exercises = [block["label"] for block in flat if block["kind"] == "exercise"]
    if exercises != ["习题 49.1"]:
        raise ValueError(f"Exercise 49.1 label or source icon changed: {exercises}")
    if any(block["kind"] in {"table", "code", "footnote"} for block in flat):
        raise ValueError("Unexpected table, code or footnote in chapter 49")
    if sum(block["kind"] == "box" for block in blocks) != 1:
        raise ValueError("Chapter 49 needs exactly one printed encoder frame")

    toc = [{"number": "49", "title": "重复—累积码", "block": blocks[0]["id"]}]
    for block in flat:
        if block["kind"] != "heading" or block["level"] != 2:
            continue
        match = HEADING.match(block["text"])
        if not match:
            raise ValueError(f"Bad section heading: {block['text']}")
        toc.append({"number": match.group(1), "title": match.group(2),
                    "block": block["id"]})
    if [entry["number"] for entry in toc] != ["49", *(f"49.{n}" for n in range(1, 6))]:
        raise ValueError(f"Chapter 49 table of contents changed: {toc}")
    chapter = {
        "schemaVersion": 2, "bookId": "mackay-information-theory-2003",
        "title": TITLE, "sourcePdfPages": [594, 599],
        "toc": toc, "blocks": blocks,
    }
    OUTPUT.write_text(json.dumps(chapter, ensure_ascii=False, separators=(",", ":")),
                      encoding="utf-8")
    print(f"Wrote {OUTPUT}: {len(blocks)} blocks, {len(toc)} TOC entries")


if __name__ == "__main__":
    main()
