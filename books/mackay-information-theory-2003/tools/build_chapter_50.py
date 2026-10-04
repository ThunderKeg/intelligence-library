"""Compile visually checked MacKay chapter 50 into an unpublished draft."""

import importlib.util
import json
import re
from html import escape
from pathlib import Path


BOOK = Path(__file__).resolve().parents[1]
PARSER = Path(__file__).with_name("build_chapter_01.py")
SPEC = importlib.util.spec_from_file_location("mackay_chapter_builder_50", PARSER)
BUILDER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(BUILDER)
SOURCE = BOOK / "translation" / "chapter-50"
ASSETS = BOOK / "assets" / "chapter-50"
OUTPUT = BOOK / "chapter-50.draft.json"
PAGES = range(601, 609)
HEADING = re.compile(r"^(50\.\d+)\s+(.+)$")
IMAGE = re.compile(r"^\.\./\.\./assets/chapter-50/(figure-50-[1-4]\.png)$")
EXPECTED_IMAGES = {f"figure-50-{n}.png" for n in range(1, 5)}
TITLE = "第 50 章　数字喷泉码"
SECTIONS = (
    "50.1　数字喷泉的编码器",
    "50.2　译码器",
    "50.3　设计度分布",
    "50.4　应用",
    "50.5　补充习题",
    "50.6　稀疏图码综述",
    "50.7　结论",
)
TRIANGLE_EXERCISES = {2, 3, 4, 9, 11, 12, 13}


def image_path(source: str) -> str:
    match = IMAGE.fullmatch(source)
    if not match or match.group(1) not in EXPECTED_IMAGES:
        raise ValueError(f"Unexpected chapter 50 image path: {source}")
    path = ASSETS / match.group(1)
    if not path.is_file():
        raise FileNotFoundError(path)
    return f"assets/chapter-50/{match.group(1)}"


def preserve_heading_design(blocks: list[dict]) -> None:
    first = blocks[0]
    if first["kind"] != "heading" or first["level"] != 1 or first["text"] != TITLE:
        raise ValueError("Chapter 50 title changed")
    number, title = "第 50 章　", "数字喷泉码"
    first["html"] = (
        '<h1 style="text-align:center">'
        '<span style="display:block;border-bottom:3px solid currentColor;'
        'padding-bottom:.45em;margin-bottom:.45em">'
        f'{escape(number)}</span>'
        '<span style="display:block;font-style:italic;white-space:nowrap">'
        f'{escape(title)}</span></h1>'
    )
    sections = [block for block in blocks if block["kind"] == "heading"
                and block["level"] == 2]
    if [block["text"] for block in sections] != list(SECTIONS):
        raise ValueError(f"Chapter 50 section sequence changed: {[b['text'] for b in sections]}")
    for block in sections:
        number, title = block["text"].split("　", 1)
        block["html"] = (
            '<h2><span aria-hidden="true">▶</span> '
            f'<span style="white-space:nowrap">{escape(number)}</span>　'
            f'<span style="white-space:nowrap">{escape(title)}</span></h2>'
        )


def outline_range(blocks: list[dict], *, first: str, last: str,
                  box_id: str, page: int, shadow: bool = False) -> list[dict]:
    starts = [i for i, block in enumerate(blocks) if block["id"] == first]
    ends = [i for i, block in enumerate(blocks) if block["id"] == last]
    if len(starts) != 1 or len(ends) != 1 or starts[0] > ends[0]:
        raise ValueError(f"Missing outlined range {first}..{last}")
    start, end = starts[0], ends[0]
    members = blocks[start:end + 1]
    if any(block["pdfPage"] != page for block in members):
        raise ValueError(f"Outline crosses original page: {box_id}")
    box = {
        "id": box_id, "kind": "box", "pdfPage": page,
        "page": page - PAGES.start + 1, "outlined": True,
        "blocks": members,
    }
    if shadow:
        box["shadow"] = True  # The scoped site style reproduces the printed lower-right shadow.
    blocks[start:end + 1] = [box]
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
        raise ValueError(f"Chapter 50 asset set differs: {actual_images ^ EXPECTED_IMAGES}")
    blocks = [
        block for page in PAGES
        for block in BUILDER.compile_page(
            page, source=SOURCE / f"pdf-{page}.md", image_resolver=image_path,
            chapter_start=601, chapter_number=50,
        )
    ]
    if sum(block["kind"] == "intro" for block in blocks) != 1:
        raise ValueError("Chapter 50 needs exactly one marked editor introduction")
    # The shared MathML converter visits top-level blocks, so compile before nesting frames.
    BUILDER.compile_math(blocks)
    preserve_heading_design(blocks)
    blocks = outline_range(blocks, first="p602-b008", last="p602-b009",
                           box_id="box-50-encoder", page=602)
    blocks = outline_range(blocks, first="p603-b004", last="p603-b009",
                           box_id="box-50-decoder", page=603)
    blocks = outline_range(blocks, first="p608-b007", last="p608-b007",
                           box_id="box-50-conclusion", page=608, shadow=True)
    if [block["id"] for block in blocks if block["kind"] == "box"] != [
        "box-50-encoder", "box-50-decoder", "box-50-conclusion"
    ]:
        raise ValueError("The three printed frames changed")
    encoder, decoder, conclusion = [block for block in blocks if block["kind"] == "box"]
    if [b["kind"] for b in encoder["blocks"]] != ["paragraph", "list"]:
        raise ValueError("Two-step encoder frame changed")
    if not encoder["blocks"][1]["ordered"] or len(encoder["blocks"][1]["items"]) != 2:
        raise ValueError("Two encoder steps missing")
    if [b["kind"] for b in decoder["blocks"]] != [
        "list", "paragraph", "paragraph", "formula", "paragraph", "list"
    ] or decoder["blocks"][3]["number"] != "(50.1)":
        raise ValueError("Decoder frame or equation (50.1) changed")
    decoder["blocks"][-1]["start"] = 2
    if len(conclusion["blocks"]) != 1 or conclusion["blocks"][0]["kind"] != "paragraph":
        raise ValueError("Conclusion must be one printed shadowed sentence")
    flat = list(walk(blocks))
    for block in flat:
        if block["kind"] == "figure" and block["width"] >= 560:
            block["wide"] = True

    formulas = [block["number"] for block in flat if block["kind"] == "formula" and block["number"]]
    if formulas != [f"(50.{n})" for n in range(1, 7)]:
        raise ValueError(f"Chapter 50 formula sequence changed: {formulas}")
    figures = [block for block in flat if block["kind"] == "figure"]
    if len(figures) != 4 or {Path(block["src"]).name for block in figures} != EXPECTED_IMAGES:
        raise ValueError("Chapter 50 figures missing, duplicated or mislabeled")
    if any(not block.get("caption", "").startswith(f"图 50.{n}　")
           for n, block in enumerate(figures, 1)):
        raise ValueError("One or more chapter 50 source figure captions missing")
    exercises = [block["label"] for block in flat if block["kind"] == "exercise"]
    expected_exercises = [
        ("▷ " if n in TRIANGLE_EXERCISES else "") + f"习题 50.{n}"
        for n in range(2, 14)
    ]
    if exercises != expected_exercises:
        raise ValueError(f"Chapter 50 exercise label/source icon changed: {exercises}")
    if any(block["kind"] in {"table", "code", "footnote"} for block in flat):
        raise ValueError("Unexpected table, code or footnote in chapter 50")

    toc = [{"number": "50", "title": "数字喷泉码", "block": blocks[0]["id"]}]
    for block in flat:
        if block["kind"] != "heading" or block["level"] != 2:
            continue
        match = HEADING.match(block["text"])
        if not match:
            raise ValueError(f"Bad section heading: {block['text']}")
        toc.append({"number": match.group(1), "title": match.group(2),
                    "block": block["id"]})
    if [entry["number"] for entry in toc] != ["50", *(f"50.{n}" for n in range(1, 8))]:
        raise ValueError(f"Chapter 50 table of contents changed: {toc}")
    chapter = {
        "schemaVersion": 2, "bookId": "mackay-information-theory-2003",
        "title": TITLE, "sourcePdfPages": [601, 608],
        "toc": toc, "blocks": blocks,
    }
    OUTPUT.write_text(json.dumps(chapter, ensure_ascii=False, separators=(",", ":")),
                      encoding="utf-8")
    print(f"Wrote {OUTPUT}: {len(blocks)} top-level blocks, {len(toc)} TOC entries")


if __name__ == "__main__":
    main()
