"""Compile visually checked MacKay Appendix B as an unpublished reader draft."""

import importlib.util
import json
import re
from html import escape
from pathlib import Path


BOOK = Path(__file__).resolve().parents[1]
PARSER = Path(__file__).with_name("build_chapter_01.py")
SPEC = importlib.util.spec_from_file_location("mackay_appendix_b_builder", PARSER)
BUILDER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(BUILDER)
SOURCE = BOOK / "translation" / "appendix-B"
ASSETS = BOOK / "assets" / "appendix-B"
OUTPUT = BOOK / "chapter-B.draft.json"
PAGES = range(613, 617)
TITLE = "附录 B　一些物理学知识"
IMAGES = {"figure-B-1.png", "figure-B-2.png"}
IMAGE = re.compile(r"^\.\./\.\./assets/appendix-B/(figure-B-[12]\.png)$")
BOXES = {
    "p613-b013": "box-b-infinite-states",
    "p614-b002": "box-b-long-range-correlations",
}
CAPTIONS = {
    "p615-b001": "p615-b002",
    "p615-b003": "p615-b004",
}
ITALIC_SUBHEADINGS = {
    "导数发散的点为什么有趣？",
    "一个会发生相变的玩具系统",
    "更一般地说",
}


def image_path(source: str) -> str:
    match = IMAGE.fullmatch(source)
    if not match:
        raise ValueError(f"Unexpected Appendix B image path: {source}")
    path = ASSETS / match.group(1)
    if not path.is_file():
        raise FileNotFoundError(path)
    return f"assets/appendix-B/{match.group(1)}"


def walk(blocks: list[dict]):
    for block in blocks:
        if block["kind"] == "box":
            yield from walk(block["blocks"])
        else:
            yield block


def preserve_headings(blocks: list[dict]) -> None:
    first = blocks[0]
    if first["kind"] != "heading" or first["level"] != 1 or first["text"] != TITLE:
        raise ValueError("Appendix B title changed")
    first["html"] = (
        '<h1 style="text-align:center">'
        '<span style="display:block;border-bottom:3px solid currentColor;'
        'padding-bottom:.45em;margin-bottom:.45em">附录 B</span>'
        '<span style="display:block;font-style:italic;white-space:nowrap">'
        '一些物理学知识</span></h1>'
    )
    sections = [block for block in blocks if block["kind"] == "heading" and block["level"] == 2]
    if [block["text"] for block in sections] != ["B.1　关于相变"]:
        raise ValueError("Appendix B section heading changed")
    sections[0]["html"] = (
        '<h2><span aria-hidden="true">▶</span> '
        '<span style="white-space:nowrap">B.1</span>　'
        '<span style="white-space:nowrap">关于相变</span></h2>'
    )
    subheadings = [block for block in blocks if block["kind"] == "heading" and block["level"] == 3]
    if {block["text"] for block in subheadings} != ITALIC_SUBHEADINGS or len(subheadings) != 3:
        raise ValueError("Appendix B's three italic subheadings changed")
    for block in subheadings:
        block["html"] = (
            '<h3 style="font-style:italic;font-weight:normal">'
            f'{escape(block["text"])}</h3>'
        )


def attach_captions(blocks: list[dict]) -> None:
    for figure_id, caption_id in CAPTIONS.items():
        index = next((i for i, block in enumerate(blocks) if block["id"] == figure_id), -1)
        if index < 0 or index + 1 >= len(blocks) or blocks[index + 1]["id"] != caption_id:
            raise ValueError(f"Figure and caption became separated: {figure_id}")
        figure, caption = blocks[index], blocks[index + 1]
        if figure["kind"] != "figure" or caption["kind"] != "paragraph":
            raise ValueError(f"Wrong caption structure near {figure_id}")
        expected_label = "图 B.1　" if figure_id == "p615-b001" else "图 B.2　"
        if not caption["text"].startswith(expected_label):
            raise ValueError(f"Figure label changed: {caption_id}")
        figure["caption"] = caption["text"]
        figure["captionSegments"] = caption["segments"]
        figure["wide"] = True
        blocks.pop(index + 1)


def outline_boxes(blocks: list[dict]) -> None:
    for quote_id, box_id in BOXES.items():
        index = next((i for i, block in enumerate(blocks) if block["id"] == quote_id), -1)
        if index < 0 or blocks[index]["kind"] != "quote":
            raise ValueError(f"Printed conclusion is not a single source quote: {quote_id}")
        quote = blocks[index]
        paragraph = {**quote, "kind": "paragraph"}
        blocks[index] = {
            "id": box_id,
            "kind": "box",
            "pdfPage": quote["pdfPage"],
            "page": quote["page"],
            "outlined": True,
            "shadow": True,
            "blocks": [paragraph],
        }


def main() -> None:
    if {path.name for path in ASSETS.glob("*.png")} != IMAGES:
        raise ValueError("Appendix B figure asset set changed")
    blocks = [
        block for page in PAGES
        for block in BUILDER.compile_page(
            page, source=SOURCE / f"pdf-{page}.md", image_resolver=image_path,
            chapter_start=613, chapter_number=0,
        )
    ]
    if sum(block["kind"] == "intro" for block in blocks) != 1:
        raise ValueError("Appendix B needs exactly one editor introduction")
    # Convert mathematics while formulas and image captions are still top-level.
    BUILDER.compile_math(blocks)
    preserve_headings(blocks)
    attach_captions(blocks)
    outline_boxes(blocks)
    flat = list(walk(blocks))
    numbered = [block["number"] for block in flat if block["kind"] == "formula" and block["number"]]
    if numbered != [f"(B.{n})" for n in range(1, 13)]:
        raise ValueError(f"Appendix B numbered formula sequence changed: {numbered}")
    if any(block["kind"] == "formula" and not block["number"] for block in flat):
        raise ValueError("Unexpected unnumbered Appendix B formula")
    figures = [block for block in flat if block["kind"] == "figure"]
    if [Path(block["src"]).name for block in figures] != sorted(IMAGES) or any(
        not block.get("caption") or not block.get("wide") for block in figures
    ):
        raise ValueError("Appendix B figures or captions changed")
    if [block["id"] for block in blocks if block["kind"] == "box"] != list(BOXES.values()):
        raise ValueError("Appendix B's two shadowed conclusion boxes changed")
    if any(block["kind"] in {"table", "exercise", "code", "footnote", "quote"} for block in flat):
        raise ValueError("Unexpected table, exercise, code, footnote or quote")
    if [block["pdfPage"] for block in blocks] != sorted(block["pdfPage"] for block in blocks):
        raise ValueError("Appendix B page order changed")
    chapter = {
        "schemaVersion": 2,
        "bookId": "mackay-information-theory-2003",
        "title": TITLE,
        "sourcePdfPages": [613, 616],
        "toc": [
            {"number": "B", "title": "一些物理学知识", "block": blocks[0]["id"]},
            {"number": "B.1", "title": "关于相变", "block": "p613-b003"},
        ],
        "blocks": blocks,
    }
    OUTPUT.write_text(json.dumps(chapter, ensure_ascii=False, separators=(",", ":")),
                      encoding="utf-8")
    print(f"Wrote {OUTPUT}: {len(blocks)} top-level blocks, {len(numbered)} numbered formulas")


if __name__ == "__main__":
    main()
