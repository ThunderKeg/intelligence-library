"""Compile the visually checked MacKay chapter 46 into an unpublished draft."""

import importlib.util
import json
import re
from pathlib import Path


BOOK = Path(__file__).resolve().parents[1]
PARSER = Path(__file__).with_name("build_chapter_01.py")
SPEC = importlib.util.spec_from_file_location("mackay_chapter_builder_46", PARSER)
BUILDER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(BUILDER)
SOURCE = BOOK / "translation" / "chapter-46"
OUTPUT = BOOK / "chapter-46.draft.json"
PAGES = range(561, 567)
HEADING = re.compile(r"^(46\.\d+)\s+(.+)$")
FOOTNOTE_URL = "http://www.inference.phy.cam.ac.uk/mackay/itila/Files.html"


def reject_image(source: str) -> str:
    raise ValueError(f"Chapter 46 has no source image: {source}")


def preserve_exercises_heading(blocks: list[dict]) -> None:
    """The print heading includes a solid right-pointing triangle."""
    matches = [block for block in blocks if block["kind"] == "heading"
               and block["level"] == 2 and block["text"] == "46.4　习题"]
    if len(matches) != 1:
        raise ValueError("Expected one section 46.4 heading")
    matches[0]["html"] = (
        '<h2><span class="ch46-exercise-heading-icon" aria-hidden="true">'
        '▶</span> 46.4　习题</h2>'
    )


def preserve_section_term(blocks: list[dict]) -> None:
    """Keep the technical term intact on narrow screens without changing TOC text."""
    matches = [block for block in blocks if block["id"] == "p564-b004"]
    if len(matches) != 1 or matches[0]["kind"] != "heading" or matches[0]["level"] != 2:
        raise ValueError("Expected section 46.2 heading at p564-b004")
    if matches[0]["text"] != "46.2　用于图像去卷积的监督式神经网络":
        raise ValueError("Section 46.2 title changed")
    matches[0]["html"] = (
        '<h2>46.2　用于图像去卷积的'
        '<span class="ch46-term">监督式神经网络</span></h2>'
    )


def main() -> None:
    blocks = [
        block
        for page in PAGES
        for block in BUILDER.compile_page(
            page,
            source=SOURCE / f"pdf-{page}.md",
            image_resolver=reject_image,
            chapter_start=561,
            chapter_number=46,
        )
    ]
    if blocks[0]["kind"] != "heading" or blocks[0]["level"] != 1:
        raise ValueError("Chapter 46 title is missing")
    if blocks[0]["text"] != "第 46 章　去卷积":
        raise ValueError(f"Unexpected chapter title: {blocks[0]['text']}")
    if sum(block["kind"] == "intro" for block in blocks) != 1:
        raise ValueError("Chapter 46 needs one marked editor introduction")
    BUILDER.compile_math(blocks)
    preserve_exercises_heading(blocks)
    preserve_section_term(blocks)
    sections = [block for block in blocks
                if block["kind"] == "heading" and block["level"] == 2]
    numbers = [HEADING.match(block["text"]).group(1) for block in sections]
    if numbers != [f"46.{number}" for number in range(1, 5)]:
        raise ValueError(f"Section order error: {numbers}")
    numbered = [block["number"] for block in blocks
                if block["kind"] == "formula" and block["number"]]
    if numbered != [f"(46.{number})" for number in range(1, 17)]:
        raise ValueError(f"Formula sequence error: {numbered}")
    if any(block["kind"] in ("figure", "table", "code") for block in blocks):
        raise ValueError("Unexpected figure, table or code in chapter 46")
    exercises = [block["label"] for block in blocks if block["kind"] == "exercise"]
    if exercises != ["习题 46.1"]:
        raise ValueError(f"Exercise sequence error: {exercises}")
    footnotes = [block for block in blocks if block["kind"] == "footnote"]
    if len(footnotes) != 1 or footnotes[0]["id"] != "fn-46-1":
        raise ValueError("Expected only footnote 46-1")
    if footnotes[0]["text"] != FOOTNOTE_URL:
        raise ValueError("Footnote URL differs from the source")
    toc = [{"number": "46", "title": "去卷积", "block": blocks[0]["id"]}]
    for block in sections:
        match = HEADING.match(block["text"])
        toc.append({"number": match.group(1), "title": match.group(2),
                    "block": block["id"]})
    chapter = {
        "schemaVersion": 2,
        "bookId": "mackay-information-theory-2003",
        "title": blocks[0]["text"],
        "sourcePdfPages": [561, 566],
        "toc": toc,
        "blocks": blocks,
    }
    OUTPUT.write_text(json.dumps(chapter, ensure_ascii=False, separators=(",", ":")),
                      encoding="utf-8")
    print(f"Wrote {OUTPUT}: {len(blocks)} blocks, {len(toc)} TOC entries")


if __name__ == "__main__":
    main()
