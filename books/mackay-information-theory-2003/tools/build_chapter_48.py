"""Compile the visually checked MacKay chapter 48 into an unpublished draft."""

import importlib.util
import json
import re
from html import escape
from pathlib import Path


BOOK = Path(__file__).resolve().parents[1]
PARSER = Path(__file__).with_name("build_chapter_01.py")
SPEC = importlib.util.spec_from_file_location("mackay_chapter_builder_48", PARSER)
BUILDER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(BUILDER)
SOURCE = BOOK / "translation" / "chapter-48"
ASSETS = BOOK / "assets" / "chapter-48"
OUTPUT = BOOK / "chapter-48.draft.json"
PAGES = range(586, 594)
HEADING = re.compile(r"^(48\.\d+)\s+(.+)$")
IMAGE = re.compile(r"^\.\./\.\./assets/chapter-48/([\w.-]+\.png)$")
EXPECTED_IMAGES = {
    "figure-48-1.png", "table-48-2.png",
    *(f"figure-48-{number}.png" for number in range(3, 12)),
}


def image_path(source: str) -> str:
    match = IMAGE.fullmatch(source)
    if not match or match.group(1) not in EXPECTED_IMAGES:
        raise ValueError(f"Unexpected chapter 48 image path: {source}")
    path = ASSETS / match.group(1)
    if not path.is_file():
        raise FileNotFoundError(path)
    return f"assets/chapter-48/{match.group(1)}"


def preserve_heading_design(blocks: list[dict]) -> None:
    first = blocks[0]
    title_parts = ("第 48 章　", "卷积码与 Turbo 码")
    if first["kind"] != "heading" or first["level"] != 1 or first["text"] != "".join(title_parts):
        raise ValueError("Chapter 48 title changed")
    first["html"] = "<h1>" + "".join(
        f'<span style="white-space:nowrap">{escape(part)}</span>' for part in title_parts
    ) + "</h1>"

    section_parts = {
        "48.1": ("48.1　", "卷积码导论"),
        "48.2": ("48.2　", "线性反馈", "移位寄存器"),
        "48.3": ("48.3　", "卷积码译码"),
        "48.4": ("48.4　", "Turbo 码"),
        "48.5": ("48.5　", "卷积码与 Turbo 码的", "奇偶校验矩阵"),
        "48.6": ("48.6　", "解答"),
    }
    sections = [block for block in blocks if block["kind"] == "heading" and block["level"] == 2]
    if len(sections) != len(section_parts):
        raise ValueError("Chapter 48 section count changed")
    for block, (number, parts) in zip(sections, section_parts.items()):
        if block["text"] != "".join(parts) or not block["text"].startswith(number):
            raise ValueError(f"Section {number} title changed: {block['text']}")
        block["html"] = (
            '<h2><span aria-hidden="true">▶</span> '
            + "".join(f'<span style="white-space:nowrap">{escape(part)}</span>' for part in parts)
            + "</h2>"
        )


def preserve_octals_table_caption(blocks: list[dict]) -> None:
    """Keep the printed Table 48.2 diagram and its copyable bilingual caption together."""
    diagrams = [block for block in blocks if block["kind"] == "figure"
                and block["src"].endswith("table-48-2.png")]
    captions = [block for block in blocks if block["kind"] == "paragraph"
                and block["text"].startswith("表 48.2　")]
    if len(diagrams) != 1 or len(captions) != 1:
        raise ValueError("Expected original Table 48.2 diagram and caption")
    diagram, caption = diagrams[0], captions[0]
    if diagram["pdfPage"] != 587 or caption["pdfPage"] != 587:
        raise ValueError("Table 48.2 must remain on PDF 587")
    if blocks.index(caption) != blocks.index(diagram) + 1:
        raise ValueError("Table 48.2 caption moved away from its diagram")
    diagram["caption"] = caption["text"]
    diagram["captionSegments"] = caption["segments"]
    diagram["sourceTable"] = True
    blocks.remove(caption)


def main() -> None:
    present = {path.name for path in ASSETS.glob("*.png")}
    if present != EXPECTED_IMAGES:
        raise ValueError(f"Chapter 48 asset set differs: {present ^ EXPECTED_IMAGES}")
    blocks = [
        block for page in PAGES
        for block in BUILDER.compile_page(
            page, source=SOURCE / f"pdf-{page}.md", image_resolver=image_path,
            chapter_start=586, chapter_number=48,
        )
    ]
    if sum(block["kind"] == "intro" for block in blocks) != 1:
        raise ValueError("Chapter 48 needs exactly one marked editor introduction")
    preserve_heading_design(blocks)
    preserve_octals_table_caption(blocks)
    BUILDER.compile_math(blocks)
    for block in blocks:
        if block["kind"] == "figure" and block["width"] >= 560:
            block["wide"] = True

    numbered = [block["number"] for block in blocks
                if block["kind"] == "formula" and block["number"]]
    if numbered != [f"(48.{number})" for number in range(1, 4)]:
        raise ValueError(f"Formula sequence changed: {numbered}")
    figures = [block for block in blocks if block["kind"] == "figure"]
    if len(figures) != len(EXPECTED_IMAGES) or {
            Path(block["src"]).name for block in figures} != EXPECTED_IMAGES:
        raise ValueError("One or more original graphics missing")
    exercises = [block["label"] for block in blocks if block["kind"] == "exercise"]
    if exercises != [f"▷ 习题 48.{number}" for number in range(1, 4)]:
        raise ValueError(f"Exercise sequence or triangle marker changed: {exercises}")
    if any(block["kind"] in ("table", "code", "footnote") for block in blocks):
        raise ValueError("Unexpected table, code, or footnote block in chapter 48")
    sections = [block for block in blocks if block["kind"] == "heading" and block["level"] == 2]
    toc = [{"number": "48", "title": "卷积码与 Turbo 码", "block": blocks[0]["id"]}]
    for block in sections:
        match = HEADING.match(block["text"])
        if not match:
            raise ValueError(f"Bad section heading: {block['text']}")
        toc.append({"number": match.group(1), "title": match.group(2), "block": block["id"]})
    chapter = {
        "schemaVersion": 2,
        "bookId": "mackay-information-theory-2003",
        "title": blocks[0]["text"],
        "sourcePdfPages": [586, 593],
        "toc": toc,
        "blocks": blocks,
    }
    OUTPUT.write_text(json.dumps(chapter, ensure_ascii=False, separators=(",", ":")),
                      encoding="utf-8")
    print(f"Wrote {OUTPUT}: {len(blocks)} blocks, {len(toc)} TOC entries")


if __name__ == "__main__":
    main()
