"""Compile the visually checked MacKay chapter 47 into an unpublished draft."""

import importlib.util
import json
import re
from html import escape
from pathlib import Path


BOOK = Path(__file__).resolve().parents[1]
PARSER = Path(__file__).with_name("build_chapter_01.py")
SPEC = importlib.util.spec_from_file_location("mackay_chapter_builder_47", PARSER)
BUILDER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(BUILDER)
SOURCE = BOOK / "translation" / "chapter-47"
ASSETS = BOOK / "assets" / "chapter-47"
OUTPUT = BOOK / "chapter-47.draft.json"
PAGES = range(569, 586)
HEADING = re.compile(r"^(47\.\d+)\s+(.+)$")
IMAGE = re.compile(r"^\.\./\.\./assets/chapter-47/([\w.-]+\.png)$")
IMAGES = {path.name for path in ASSETS.glob("*.png")}
EXPECTED_IMAGES = {
    *(f"figure-47-{number}.png" for number in range(1, 13)),
    "figure-47-17.png", "figure-47-18-chart.png", "figure-47-19.png",
    "equation-47-16-matrix.png",
}


def image_path(source: str) -> str:
    match = IMAGE.fullmatch(source)
    if not match or match.group(1) not in EXPECTED_IMAGES:
        raise ValueError(f"Unexpected chapter 47 image path: {source}")
    path = ASSETS / match.group(1)
    if not path.is_file():
        raise FileNotFoundError(path)
    return f"assets/chapter-47/{match.group(1)}"


def preserve_heading_design(blocks: list[dict]) -> None:
    first = blocks[0]
    parts = ("第 47 章　", "低密度奇偶校验码")
    if first["kind"] != "heading" or first["level"] != 1 or first["text"] != "".join(parts):
        raise ValueError("Chapter 47 title changed")
    first["html"] = "<h1>" + "".join(
        f'<span style="white-space:nowrap">{escape(part)}</span>' for part in parts
    ) + "</h1>"
    sections = [block for block in blocks if block["kind"] == "heading" and block["level"] == 2]
    if [HEADING.match(block["text"]).group(1) for block in sections] != [
            f"47.{number}" for number in range(1, 11)]:
        raise ValueError("Section sequence changed")
    term_parts = {
        "p571-b010": ("47.3　", ("用和积算法译码",)),
        "p579-b010": ("47.6　改进 ", ("Gallager 码",)),
        "p581-b009": ("47.7　", ("低密度奇偶校验码",), ("的快速编码",)),
    }
    for block in sections:
        parts = term_parts.get(block["id"], (block["text"],))
        if "".join(part[0] if isinstance(part, tuple) else part for part in parts) != block["text"]:
            raise ValueError(f"Section title text changed: {block['id']}")
        block["html"] = (
            '<h2><span aria-hidden="true">▶</span> '
            + "".join(
                f'<span class="ch47-term">{escape(part[0])}</span>'
                if isinstance(part, tuple) else escape(part) for part in parts
            )
            + "</h2>"
        )


def preserve_fast_encoding_steps(blocks: list[dict]) -> None:
    """Displayed numbered equations split the six printed steps into list blocks."""
    step_lists = [block for block in blocks if block["kind"] == "list"
                  and block["pdfPage"] in (582, 583) and block["ordered"]]
    if len(step_lists) != 6 or any(len(block["items"]) != 1 for block in step_lists):
        raise ValueError(f"Expected six fast-encoding steps, got {len(step_lists)}")
    for number, block in enumerate(step_lists, 1):
        block["start"] = number


def preserve_algorithm(blocks: list[dict]) -> None:
    """The four GF(4) transform lines are one complete bordered source box."""
    positions = [i for i, block in enumerate(blocks)
                 if block["pdfPage"] == 580 and block["kind"] == "formula"]
    if len(positions) != 2 or positions[0] + 1 >= len(blocks):
        raise ValueError("Expected transform and equation 47.15 on PDF 580")
    index = positions[0]
    caption = blocks[index + 1]
    if caption["kind"] != "paragraph" or not caption["text"].startswith("算法 47.16"):
        raise ValueError("Missing algorithm 47.16 caption after transform")
    formula = blocks[index]
    if formula["number"]:
        raise ValueError("Transform formula unexpectedly numbered")
    blocks[index] = {
        "id": "box-47-algorithm-47-16", "kind": "box", "pdfPage": 580,
        "page": 12, "outlined": True, "algorithm": True, "blocks": [formula],
    }


def check_copyable_matrix(blocks: list[dict]) -> None:
    """Check the 12 × 28 transcription of printed equation (47.16)."""
    matches = [block for block in blocks if block["kind"] == "formula"
               and block["number"] == "(47.16)"]
    if len(matches) != 1 or matches[0]["pdfPage"] != 581:
        raise ValueError("Missing copyable equation (47.16) on PDF 581")
    tex = matches[0]["tex"]
    array = re.search(r"\\begin\{array\}\{c{16}\|c{12}\}(.*?)\\end\{array\}", tex)
    if not array:
        raise ValueError("Equation (47.16) lacks its 16|12 column separation")
    rows = [row.split("&") for row in array.group(1).split(r"\\")]
    if len(rows) != 12 or any(len(row) != 28 or set(row) - {"0", "1"} for row in rows):
        raise ValueError("Equation (47.16) is not a complete 12×28 binary matrix")
    if sum(bit == "1" for row in rows for bit in row) != 71:
        raise ValueError("Equation (47.16) should have 71 ones")
    if any(sum(bit == "1" for bit in row[:16]) != 4 for row in rows):
        raise ValueError("Equation (47.16) left block should have four ones per row")
    if any(sum(row[column] == "1" for row in rows) != 3 for column in range(16)):
        raise ValueError("Equation (47.16) left block should have three ones per column")


def preserve_difference_set_table(blocks: list[dict]) -> None:
    tables = [block for block in blocks if block["kind"] == "table" and block["pdfPage"] == 581]
    if len(tables) != 1:
        raise ValueError("Expected one difference-set table on PDF 581")
    rows = tables[0]["rows"]
    if len(rows) != 6 or len(rows[0]) != 1 or any(len(row) != 7 for row in rows[1:]):
        raise ValueError("Difference-set table shape changed")
    if rows[0][0]["text"] != "差集循环码（DIFFERENCE SET CYCLIC CODES）":
        raise ValueError("Difference-set table title changed")
    if rows[1][0]["text"] != "$N$" or rows[1][4]["text"] != "$273$":
        raise ValueError("Difference-set table N row changed")
    rows[0][0]["colspan"] = 7
    # The shared Markdown parser loses a strong wrapper when it surrounds math.
    # Retain the printed bold digits in copyable, bold MathML.
    bold_cells = {(2, column) for column in range(2, 7)} | {
        (4, 2), (4, 3), (4, 4), (5, 1), (5, 2), (5, 3),
    }
    for row_index, column_index in bold_cells:
        cell = rows[row_index][column_index]
        segments = cell["segments"]
        if len(segments) != 1 or "tex" not in segments[0]:
            raise ValueError(f"Expected one math segment in bold table cell {(row_index, column_index)}")
        segments[0]["tex"] = r"\mathbf{" + segments[0]["tex"] + "}"


def preserve_figure_captions(blocks: list[dict]) -> None:
    """Keep Figure 47.2's printed caption after its (a)-(c) explanations."""
    delayed = [block for block in blocks if block["pdfPage"] == 570
               and block["kind"] == "paragraph" and block["text"].startswith("图 47.2　")]
    if len(delayed) != 1:
        raise ValueError("Expected one delayed Figure 47.2 caption")
    delayed[0]["kind"] = "caption"

    # Other captions followed editorial translation notes in Markdown. Attach
    # them to their image without losing any words, math, or source figure order.
    figure_numbers = {3, 5, 6, 7, 8, 12, 17, 18, 19}
    attached = set()
    for figure in [block for block in blocks if block["kind"] == "figure"]:
        name = Path(figure["src"]).name
        match = re.fullmatch(r"figure-47-(\d+)(?:-chart)?\.png", name)
        if not match or int(match.group(1)) not in figure_numbers:
            continue
        number = int(match.group(1))
        if figure.get("caption"):
            raise ValueError(f"Figure 47.{number} already has a caption")
        index = blocks.index(figure)
        candidates = []
        for following in blocks[index + 1:]:
            if following["pdfPage"] != figure["pdfPage"] or following["kind"] in ("figure", "heading"):
                break
            if following["kind"] == "paragraph" and following["text"].startswith(f"图 47.{number}　"):
                candidates.append(following)
        if len(candidates) != 1:
            raise ValueError(f"Expected one Figure 47.{number} caption, got {len(candidates)}")
        caption = candidates[0]
        figure["caption"] = caption["text"]
        figure["captionSegments"] = caption["segments"]
        blocks.remove(caption)
        attached.add(number)
    if attached != figure_numbers:
        raise ValueError(f"Missing figure captions: {figure_numbers - attached}")
    algorithm_caption = [block for block in blocks if block["pdfPage"] == 580
                         and block["kind"] == "paragraph"
                         and block["text"].startswith("算法 47.16　")]
    if len(algorithm_caption) != 1:
        raise ValueError("Expected one Algorithm 47.16 caption")
    algorithm_caption[0]["kind"] = "caption"


def main() -> None:
    if IMAGES != EXPECTED_IMAGES:
        raise ValueError(f"Chapter 47 source assets differ: {IMAGES ^ EXPECTED_IMAGES}")
    blocks = [
        block for page in PAGES
        for block in BUILDER.compile_page(
            page, source=SOURCE / f"pdf-{page}.md", image_resolver=image_path,
            chapter_start=569, chapter_number=47,
        )
    ]
    if sum(block["kind"] == "intro" for block in blocks) != 1:
        raise ValueError("Chapter 47 needs one marked editor introduction")
    preserve_heading_design(blocks)
    preserve_fast_encoding_steps(blocks)
    preserve_difference_set_table(blocks)
    check_copyable_matrix(blocks)
    BUILDER.compile_math(blocks)
    preserve_algorithm(blocks)
    preserve_figure_captions(blocks)
    for block in blocks:
        if block["kind"] == "figure" and block["width"] >= 560:
            block["wide"] = True
    numbered = [block["number"] for block in blocks
                if block["kind"] == "formula" and block["number"]]
    expected_numbers = [f"(47.{number})" for number in range(1, 31)]
    if numbered != expected_numbers:
        raise ValueError(f"Formula sequence changed: {numbered}")
    figures = [block for block in blocks if block["kind"] == "figure"]
    if len(figures) != len(EXPECTED_IMAGES) or {
            Path(block["src"]).name for block in figures} != EXPECTED_IMAGES:
        raise ValueError("One or more source graphics missing")
    if sum(block["kind"] == "table" for block in blocks) != 4:
        raise ValueError("Expected four source tables")
    exercises = [block["label"] for block in blocks if block["kind"] == "exercise"]
    if exercises != [f"习题 47.{number}" for number in range(1, 5)]:
        raise ValueError(f"Exercise sequence changed: {exercises}")
    footnotes = [block for block in blocks if block["kind"] == "footnote"]
    if len(footnotes) != 1 or footnotes[0]["id"] != "fn-47-1":
        raise ValueError("Expected only chapter 47 footnote 1")
    sections = [block for block in blocks if block["kind"] == "heading" and block["level"] == 2]
    toc = [{"number": "47", "title": "低密度奇偶校验码", "block": blocks[0]["id"]}]
    for block in sections:
        match = HEADING.match(block["text"])
        toc.append({"number": match.group(1), "title": match.group(2), "block": block["id"]})
    chapter = {
        "schemaVersion": 2,
        "bookId": "mackay-information-theory-2003",
        "title": blocks[0]["text"],
        "sourcePdfPages": [569, 585],
        "toc": toc,
        "blocks": blocks,
    }
    OUTPUT.write_text(json.dumps(chapter, ensure_ascii=False, separators=(",", ":")),
                      encoding="utf-8")
    print(f"Wrote {OUTPUT}: {len(blocks)} blocks, {len(toc)} TOC entries")


if __name__ == "__main__":
    main()
