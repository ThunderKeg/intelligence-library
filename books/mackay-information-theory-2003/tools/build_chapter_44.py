"""Compile the visually checked MacKay chapter 44 into an unpublished draft."""

import importlib.util
import json
import re
from pathlib import Path


BOOK = Path(__file__).resolve().parents[1]
PARSER = Path(__file__).with_name("build_chapter_01.py")
SPEC = importlib.util.spec_from_file_location("mackay_chapter_builder_44", PARSER)
BUILDER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(BUILDER)
SOURCE = BOOK / "translation" / "chapter-44"
ASSETS = BOOK / "assets" / "chapter-44"
OUTPUT = BOOK / "chapter-44.draft.json"
PAGES = range(539, 546)
HEADING = re.compile(r"^(44\.\d+)\s+(.+)$")
IMAGE = re.compile(r"^\.\./\.\./assets/chapter-44/(figure-44-[1-7]\.png)$")
IMAGES = {f"figure-44-{number}.png" for number in range(1, 8)}


def image_path(source: str) -> str:
    match = IMAGE.fullmatch(source)
    if not match or match.group(1) not in IMAGES:
        raise ValueError(f"Unexpected chapter 44 image path: {source}")
    path = ASSETS / match.group(1)
    if not path.is_file():
        raise FileNotFoundError(path)
    return f"assets/chapter-44/{match.group(1)}"


def preserve_title(block: dict) -> None:
    parts = ("第 44 章　", "多层网络中的", "监督学习")
    if block["text"] != "".join(parts):
        raise ValueError(f"Unexpected chapter title: {block['text']}")
    block["html"] = "<h1>" + "".join(
        f'<span class="mackay-ch44-title-part" style="white-space:nowrap">{part}</span>'
        for part in parts
    ) + "</h1>"


def preserve_section_terms(blocks: list[dict]) -> None:
    """Keep the book's technical terms intact in narrow section headings."""
    sections = {
        "44.2　传统方法如何训练回归网络": (
            "44.2　传统方法如何训练", ("回归网络", True)),
        "44.3　将神经网络学习视为推断": (
            "44.3　将", ("神经网络", True), "学习视为", ("推断", True)),
        "44.4　贝叶斯方法对监督式前馈神经网络的益处": (
            "44.4　贝叶斯方法对", ("监督式", True), ("前馈", True),
            ("神经网络", True), "的益处"),
    }
    found = set()
    for block in blocks:
        if block["kind"] != "heading" or block["text"] not in sections:
            continue
        parts = sections[block["text"]]
        if block["text"] != "".join(part[0] if isinstance(part, tuple) else part
                                     for part in parts):
            raise ValueError(f"Section title changed: {block['text']}")
        block["html"] = "<h2>" + "".join(
            f'<span class="mackay-ch44-term" style="white-space:nowrap">{part[0]}</span>'
            if isinstance(part, tuple) else part for part in parts
        ) + "</h2>"
        found.add(block["text"])
    if found != set(sections):
        raise ValueError(f"Missing section titles for term grouping: {set(sections) - found}")


def attach_classifier_table_captions(blocks: list[dict]) -> None:
    """Keep the five original classifier labels attached to their number grids."""
    positions = [index for index, block in enumerate(blocks) if block["kind"] == "table"]
    if len(positions) != 5:
        raise ValueError(f"Expected five exercise frequency grids: {positions}")
    expected = [f"分类器 {letter}" for letter in "ABCDE"]
    for index, label in zip(reversed(positions), reversed(expected)):
        table = blocks[index]
        caption = blocks[index - 1]
        if caption["kind"] != "paragraph" or caption["text"] != label:
            raise ValueError(f"Missing classifier caption {label}")
        if [cell["text"] for cell in table["rows"][0]] != (["$t\\backslash y$", "0", "1"]
                if label[-1] in "ABC" else ["$t\\backslash y$", "0", "?", "1"]):
            raise ValueError(f"Malformed classifier heading: {label}")
        if len(table["rows"]) != 3:
            raise ValueError(f"Malformed classifier rows: {label}")
        table["caption"] = label
        table["captionSegments"] = caption["segments"]
        del blocks[index - 1]


def main() -> None:
    blocks = [
        block
        for page in PAGES
        for block in BUILDER.compile_page(
            page,
            source=SOURCE / f"pdf-{page}.md",
            image_resolver=image_path,
            chapter_start=539,
            chapter_number=44,
        )
    ]
    if blocks[0]["kind"] != "heading" or blocks[0]["level"] != 1:
        raise ValueError("Chapter 44 title is missing")
    preserve_title(blocks[0])
    preserve_section_terms(blocks)
    if sum(block["kind"] == "intro" for block in blocks) != 1:
        raise ValueError("Chapter 44 needs one marked editor introduction")
    BUILDER.compile_math(blocks)
    attach_classifier_table_captions(blocks)
    for block in blocks:
        if block["kind"] == "figure" and block["width"] >= 560:
            block["wide"] = True
    sections = [block for block in blocks if block["kind"] == "heading" and block["level"] == 2]
    section_numbers = [HEADING.match(block["text"]).group(1) for block in sections]
    if section_numbers != [f"44.{number}" for number in range(1, 6)]:
        raise ValueError(f"Section order error: {section_numbers}")
    numbered = [block["number"] for block in blocks
                if block["kind"] == "formula" and block["number"]]
    if numbered != [f"(44.{number})" for number in range(1, 13)]:
        raise ValueError(f"Formula sequence error: {numbered}")
    figures = [block for block in blocks if block["kind"] == "figure"]
    if len(figures) != len(IMAGES) or {Path(block["src"]).name for block in figures} != IMAGES:
        raise ValueError("One or more source graphics missing")
    exercises = [block["label"] for block in blocks if block["kind"] == "exercise"]
    if [re.search(r"44\.\d+", label).group() for label in exercises] != ["44.1"]:
        raise ValueError(f"Exercise sequence error: {exercises}")
    toc = [{"number": "44", "title": "多层网络中的监督学习", "block": blocks[0]["id"]}]
    for block in sections:
        match = HEADING.match(block["text"])
        toc.append({"number": match.group(1), "title": match.group(2), "block": block["id"]})
    chapter = {
        "schemaVersion": 2,
        "bookId": "mackay-information-theory-2003",
        "title": blocks[0]["text"],
        "sourcePdfPages": [539, 545],
        "toc": toc,
        "blocks": blocks,
    }
    OUTPUT.write_text(json.dumps(chapter, ensure_ascii=False, separators=(",", ":")),
                      encoding="utf-8")
    print(f"Wrote {OUTPUT}: {len(blocks)} blocks, {len(toc)} TOC entries")


if __name__ == "__main__":
    main()
