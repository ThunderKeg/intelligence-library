"""Compile the visually checked MacKay chapter 43 into an unpublished draft."""

import importlib.util
import json
import re
from pathlib import Path


BOOK = Path(__file__).resolve().parents[1]
PARSER = Path(__file__).with_name("build_chapter_01.py")
SPEC = importlib.util.spec_from_file_location("mackay_chapter_builder_43", PARSER)
BUILDER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(BUILDER)
SOURCE = BOOK / "translation" / "chapter-43"
ASSETS = BOOK / "assets" / "chapter-43"
OUTPUT = BOOK / "chapter-43.draft.json"
PAGES = range(534, 539)
HEADING = re.compile(r"^(43\.\d+)\s+(.+)$")
IMAGE = re.compile(r"^\.\./\.\./assets/chapter-43/(figure-43-[12]\.png)$")
IMAGES = {"figure-43-1.png", "figure-43-2.png"}


def image_path(source: str) -> str:
    match = IMAGE.fullmatch(source)
    if not match or match.group(1) not in IMAGES:
        raise ValueError(f"Unexpected chapter 43 image path: {source}")
    path = ASSETS / match.group(1)
    if not path.is_file():
        raise FileNotFoundError(path)
    return f"assets/chapter-43/{match.group(1)}"


def preserve_title(block: dict) -> None:
    parts = ("第 43 章　", "玻尔兹曼机")
    if block["text"] != "".join(parts):
        raise ValueError(f"Unexpected chapter title: {block['text']}")
    block["html"] = "<h1>" + "".join(
        f'<span class="mackay-ch43-title-part" style="white-space:nowrap">{part}</span>'
        for part in parts
    ) + "</h1>"


def preserve_section_terms(blocks: list[dict]) -> None:
    """Keep technical names intact in the two long section headings."""
    sections = {
        "43.1　从 Hopfield 网络到玻尔兹曼机": (
            "43.1　从 ", ("Hopfield 网络", True), "到", ("玻尔兹曼机", True)),
        "43.2　带隐单元的玻尔兹曼机": (
            "43.2　", ("带隐单元的", True), ("玻尔兹曼机", True)),
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
            f'<span class="mackay-ch43-term" style="white-space:nowrap">{part[0]}</span>'
            if isinstance(part, tuple) else part for part in parts
        ) + "</h2>"
        found.add(block["text"])
    if found != set(sections):
        raise ValueError(f"Missing section titles for term grouping: {set(sections) - found}")


def outline_activity_rule(blocks: list[dict]) -> None:
    """Rebuild the book's single full-border activity-rule frame."""
    positions = [i for i, block in enumerate(blocks)
                 if block["pdfPage"] == 534 and block["kind"] == "paragraph"
                 and block["text"].startswith("玻尔兹曼机的活动规则：")]
    if len(positions) != 1:
        raise ValueError(f"Expected one activity-rule heading: {positions}")
    index = positions[0]
    framed = blocks[index:index + 3]
    if ([block["kind"] for block in framed] != ["paragraph", "formula", "paragraph"]
            or framed[1]["number"] != "(43.3)"
            or not framed[2]["text"].startswith("否则将 $x_i=-1$")
            or any(block["pdfPage"] != 534 for block in framed)):
        raise ValueError("Malformed activity-rule frame")
    blocks[index:index + 3] = [{
        "id": "box-43-activity-rule", "kind": "box", "pdfPage": 534, "page": 1,
        "outlined": True, "blocks": framed,
    }]


def main() -> None:
    blocks = [
        block
        for page in PAGES
        for block in BUILDER.compile_page(
            page,
            source=SOURCE / f"pdf-{page}.md",
            image_resolver=image_path,
            chapter_start=534,
            chapter_number=43,
        )
    ]
    if blocks[0]["kind"] != "heading" or blocks[0]["level"] != 1:
        raise ValueError("Chapter 43 title is missing")
    preserve_title(blocks[0])
    preserve_section_terms(blocks)
    if sum(block["kind"] == "intro" for block in blocks) != 1:
        raise ValueError("Chapter 43 needs one marked editor introduction")
    BUILDER.compile_math(blocks)
    numbered = [block["number"] for block in blocks
                if block["kind"] == "formula" and block["number"]]
    if numbered != [f"(43.{number})" for number in range(1, 19)]:
        raise ValueError(f"Formula sequence error: {numbered}")
    outline_activity_rule(blocks)
    for block in blocks:
        if block["kind"] == "figure" and block["width"] >= 560:
            block["wide"] = True
    sections = [block for block in blocks if block["kind"] == "heading" and block["level"] == 2]
    section_numbers = [HEADING.match(block["text"]).group(1) for block in sections]
    if section_numbers != ["43.1", "43.2", "43.3"]:
        raise ValueError(f"Section order error: {section_numbers}")
    figures = [block for block in blocks if block["kind"] == "figure"]
    if len(figures) != len(IMAGES) or {Path(block["src"]).name for block in figures} != IMAGES:
        raise ValueError("One or more source graphics missing")
    if sum(block["kind"] == "box" and block.get("outlined") for block in blocks) != 1:
        raise ValueError("The outlined activity-rule frame is required")
    exercises = [block["label"] for block in blocks if block["kind"] == "exercise"]
    if [re.search(r"43\.\d+", label).group() for label in exercises] != [
            "43.1", "43.2", "43.3"]:
        raise ValueError(f"Exercise sequence error: {exercises}")
    if sum(block.get("recommendedIcon", "").endswith("exercise-rat.png")
           for block in blocks) != 1:
        raise ValueError("Exercise 43.1 recommended icon is required")
    toc = [{"number": "43", "title": "玻尔兹曼机", "block": blocks[0]["id"]}]
    for block in sections:
        match = HEADING.match(block["text"])
        toc.append({"number": match.group(1), "title": match.group(2), "block": block["id"]})
    chapter = {
        "schemaVersion": 2,
        "bookId": "mackay-information-theory-2003",
        "title": blocks[0]["text"],
        "sourcePdfPages": [534, 538],
        "toc": toc,
        "blocks": blocks,
    }
    OUTPUT.write_text(json.dumps(chapter, ensure_ascii=False, separators=(",", ":")),
                      encoding="utf-8")
    print(f"Wrote {OUTPUT}: {len(blocks)} blocks, {len(toc)} TOC entries")


if __name__ == "__main__":
    main()
