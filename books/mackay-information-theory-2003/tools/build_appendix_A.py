"""Compile the visually checked MacKay Appendix A as an unpublished draft."""

import importlib.util
import json
from html import escape
from pathlib import Path


BOOK = Path(__file__).resolve().parents[1]
PARSER = Path(__file__).with_name("build_chapter_01.py")
SPEC = importlib.util.spec_from_file_location("mackay_appendix_a_builder", PARSER)
BUILDER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(BUILDER)
SOURCE = BOOK / "translation" / "appendix-A"
OUTPUT = BOOK / "chapter-A.draft.json"
PAGES = range(610, 613)
TITLE = "附录 A　记号"


def no_image(source: str) -> str:
    raise ValueError(f"Appendix A has no printed images: {source}")


def main() -> None:
    blocks = [
        block for page in PAGES
        for block in BUILDER.compile_page(
            page, source=SOURCE / f"pdf-{page}.md", image_resolver=no_image,
            chapter_start=610, chapter_number=0,
        )
    ]
    if not blocks or blocks[0]["kind"] != "heading" or blocks[0]["text"] != TITLE:
        raise ValueError("Appendix A source heading changed")
    if sum(block["kind"] == "intro" for block in blocks) != 1:
        raise ValueError("Appendix A needs exactly one marked editor introduction")
    if [block["text"] for block in blocks if block["kind"] == "heading"] != [TITLE]:
        raise ValueError("Appendix A has unexpected section headings")
    number, title = "附录 A", "记号"
    blocks[0]["html"] = (
        '<h1 style="text-align:center">'
        '<span style="display:block;border-bottom:3px solid currentColor;'
        'padding-bottom:.45em;margin-bottom:.45em">'
        f'{escape(number)}</span>'
        '<span style="display:block;font-style:italic;white-space:nowrap">'
        f'{escape(title)}</span></h1>'
    )
    BUILDER.compile_math(blocks)
    formulas = [block for block in blocks if block["kind"] == "formula"]
    numbered = [block["number"] for block in formulas if block["number"]]
    if numbered != [f"(A.{n})" for n in range(1, 12)]:
        raise ValueError(f"Appendix A formula sequence changed: {numbered}")
    unnumbered = [block for block in formulas if not block["number"]]
    if len(unnumbered) != 1 or unnumbered[0]["pdfPage"] != 612 or not unnumbered[0]["tex"].startswith("\\delta_{mn}="):
        raise ValueError("Appendix A's unnumbered identity-matrix definition changed")
    if any(block["kind"] in {"figure", "table", "exercise", "code", "footnote", "box"}
           for block in blocks):
        raise ValueError("Unexpected nontext or exercise block in Appendix A")
    if [block["pdfPage"] for block in blocks] != sorted(block["pdfPage"] for block in blocks):
        raise ValueError("Appendix A original-page order changed")
    chapter = {
        "schemaVersion": 2,
        "bookId": "mackay-information-theory-2003",
        "title": TITLE,
        "sourcePdfPages": [610, 612],
        "toc": [{"number": "A", "title": title, "block": blocks[0]["id"]}],
        "blocks": blocks,
    }
    OUTPUT.write_text(json.dumps(chapter, ensure_ascii=False, separators=(",", ":")),
                      encoding="utf-8")
    print(f"Wrote {OUTPUT}: {len(blocks)} blocks, {len(formulas)} display formulas")


if __name__ == "__main__":
    main()
