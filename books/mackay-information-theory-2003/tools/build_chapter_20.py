"""Compile the page-checked MacKay chapter 20 into an unpublished draft."""

import importlib.util
import json
import re
from pathlib import Path


BOOK = Path(__file__).resolve().parents[1]
PARSER = Path(__file__).with_name("build_chapter_01.py")
SPEC = importlib.util.spec_from_file_location("mackay_chapter_builder_20", PARSER)
BUILDER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(BUILDER)
SOURCE = BOOK / "translation" / "chapter-20"
ASSETS = BOOK / "assets" / "chapter-20"
OUTPUT = BOOK / "chapter-20.draft.json"
PAGES = range(296, 305)
IMAGE = re.compile(r"^\.\./\.\./assets/chapter-20/([\w.-]+\.png)$")
HEADING = re.compile(r"^(20\.\d+)\s+(.+)$")
FIGURES = {
    "figure-20-1.png", "figure-20-3.png", "figure-20-4.png",
    "figure-20-5.png", "figure-20-6.png", "figure-20-8.png",
    "figure-20-9.png", "figure-20-10.png", "figure-20-11.png",
    "exercise-20-4-mixture.png",
}


def image_path(source: str) -> str:
    match = IMAGE.fullmatch(source)
    if not match:
        raise ValueError(f"Unexpected chapter 20 image path: {source}")
    path = ASSETS / match.group(1)
    if not path.is_file():
        raise FileNotFoundError(path)
    return f"assets/chapter-20/{match.group(1)}"


def algorithm_box(blocks: list[dict], page: int, first_text: str,
                  caption_text: str, expected_formulas: list[str]) -> list[dict]:
    start = next(index for index, block in enumerate(blocks)
                 if block["pdfPage"] == page and block["kind"] == "paragraph"
                 and block["text"].startswith(first_text))
    end = next(index for index, block in enumerate(blocks)
               if block["pdfPage"] == page and block["kind"] == "paragraph"
               and block["text"].startswith(caption_text))
    children = blocks[start:end]
    if not children or any(block["pdfPage"] != page for block in children):
        raise ValueError(f"Algorithm on PDF {page} crosses an unexpected page boundary")
    found = [block["number"] for block in children if block["kind"] == "formula"]
    if found != expected_formulas:
        raise ValueError(f"Algorithm formulas on PDF {page}: {found}")
    caption = {**blocks[end], "kind": "caption"}
    box = {
        "id": f"box-20-{2 if page == 298 else 7}",
        "kind": "box", "pdfPage": page, "page": page - 295,
        "outlined": True, "blocks": children,
    }
    return blocks[:start] + [box, caption] + blocks[end + 1:]


def main() -> None:
    blocks = [
        block
        for page in PAGES
        for block in BUILDER.compile_page(
            page, source=SOURCE / f"pdf-{page}.md", image_resolver=image_path,
            chapter_start=296, chapter_number=20,
        )
    ]
    if blocks[0]["kind"] != "heading" or blocks[0]["level"] != 1:
        raise ValueError("Chapter 20 title is missing")
    if sum(block["kind"] == "intro" for block in blocks) != 1:
        raise ValueError("Chapter 20 needs one clearly marked editor introduction")
    numbers = [block["number"] for block in blocks if block["kind"] == "formula" and block["number"]]
    if numbers != [f"(20.{i})" for i in range(1, 24)]:
        raise ValueError(f"Chapter 20 formulas missing or out of order: {numbers}")
    exercises = [block["label"] for block in blocks if block["kind"] == "exercise"]
    if [re.search(r"20\.\d+", label).group() for label in exercises] != [f"20.{i}" for i in range(1, 6)]:
        raise ValueError(f"Chapter 20 exercise labels missing or out of order: {exercises}")
    figures = [block for block in blocks if block["kind"] == "figure"]
    if {Path(block["src"]).name for block in figures} != FIGURES or len(figures) != len(FIGURES):
        raise ValueError(f"Unexpected chapter 20 figure set: {[block['src'] for block in figures]}")
    for block in figures:
        if block["width"] >= 560 or Path(block["src"]).name in {"figure-20-10.png", "figure-20-11.png"}:
            block["wide"] = True
    toc = [{"number": "20", "title": "一个推断任务示例：聚类", "block": blocks[0]["id"]}]
    for block in blocks:
        if block["kind"] == "heading" and block["level"] == 2:
            match = HEADING.match(block["text"])
            if not match:
                raise ValueError(f"Unexpected section heading: {block['text']}")
            toc.append({"number": match.group(1), "title": match.group(2), "block": block["id"]})
    if [entry["number"] for entry in toc] != ["20"] + [f"20.{i}" for i in range(1, 6)]:
        raise ValueError(f"Chapter 20 sections missing or out of order: {toc}")
    source303 = (SOURCE / "pdf-303.md").read_text(encoding="utf-8")
    if "$\\mathbf m^{(1)}=(m,0)$ 和 $\\mathbf m^{(1)}=(-m,0)$" not in source303:
        raise ValueError("Original PDF 303 repeated m^(1) notation was changed")

    BUILDER.compile_math(blocks)
    blocks = algorithm_box(blocks, 298, "初始化。", "算法 20.2", [f"(20.{i})" for i in range(3, 7)])
    blocks = algorithm_box(blocks, 301, "分配步骤。", "算法 20.7", [f"(20.{i})" for i in range(7, 10)])
    chapter = {
        "schemaVersion": 2,
        "bookId": "mackay-information-theory-2003",
        "title": blocks[0]["text"],
        "sourcePdfPages": [296, 304],
        "toc": toc,
        "blocks": blocks,
    }
    OUTPUT.write_text(json.dumps(chapter, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(f"Wrote {OUTPUT}: {len(blocks)} blocks, {len(toc)} TOC entries, "
          f"{len(numbers)} numbered formulas, {len(figures)} source images, {len(exercises)} exercises")


if __name__ == "__main__":
    main()
