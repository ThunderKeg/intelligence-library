"""Extract a candidate checklist; extraction is never translation or PDF review.

Text and original-page PNGs are temporary aids under tmp/convex. The checked-in
inventory records provenance, original contents, page ranges, and unreviewed
heading/caption/equation candidates. It cannot prove completeness or semantics.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import unicodedata
from collections import Counter
from pathlib import Path

import fitz

from common import BOOK, BOOK_ID, CHAPTERS, PDF, ROOT, TMP, chapter_for_page, parse_pages

NUMBER = r"(?:[1-9]\d*|[ABC])\.\d+(?:[a-z])?"
EQUATION = re.compile(rf"^\(({NUMBER})\)$")
CAPTION = re.compile(rf"^(Figure|Table|Algorithm|Example)\s+({NUMBER})(?:\s|\.|$)")
SECTION = re.compile(r"^((?:\d+|[ABC])(?:\.\d+){1,3})(?:\s+(.+))?$")


def normal(value: str) -> str:
    return unicodedata.normalize("NFKC", value).strip()


def page_lines(page: fitz.Page) -> list[dict]:
    values = []
    for block in page.get_text("dict")["blocks"]:
        if block["type"] != 0:
            continue
        for line in block["lines"]:
            spans = line["spans"]
            values.append({
                "text": normal("".join(span["text"] for span in spans)),
                "bbox": [round(value, 2) for value in line["bbox"]],
                "size": round(max((span["size"] for span in spans), default=0), 2),
                "headingFont": all("CMSSBX" in span["font"] for span in spans if span["text"].strip()),
            })
    return values


def heading_candidates(lines: list[dict], page: int) -> list[dict]:
    # CMSSBX headings below the running header. Equations with isolated math
    # glyphs, ordinary prose, and bold exercise numbers are not headings.
    chosen = [line for line in lines if line["headingFont"] and line["size"] >= 9.5
              and line["bbox"][1] > 110 and line["text"]]
    merged: list[dict] = []
    for line in sorted(chosen, key=lambda item: (round(item["bbox"][1], 0), item["bbox"][0])):
        if merged and abs(merged[-1]["bbox"][1] - line["bbox"][1]) < 1.5:
            merged[-1]["text"] += " " + line["text"]
            merged[-1]["bbox"][2] = max(merged[-1]["bbox"][2], line["bbox"][2])
        else:
            merged.append(dict(line))
    result = []
    for line in merged:
        match = SECTION.match(line["text"])
        result.append({
            "text": line["text"], "number": match.group(1) if match else None,
            "levelCandidate": (match.group(1).count(".") + 1 if match else
                               (1 if line["size"] >= 20 else 2 if line["size"] >= 14 else 4)),
            "bbox": line["bbox"], "status": "unreviewed",
            "method": "font-and-position-candidate",
        })
    return result


def contents_rows(document: fitz.Document) -> list[dict]:
    result = []
    for page_number in range(7, 11):
        rows: list[list[dict]] = []
        for line in sorted(page_lines(document[page_number - 1]), key=lambda item: (round(item["bbox"][1]), item["bbox"][0])):
            if line["bbox"][1] <= 110:
                continue
            if rows and abs(rows[-1][0]["bbox"][1] - line["bbox"][1]) < 2:
                rows[-1].append(line)
            else:
                rows.append([line])
        for row in rows:
            # Three-digit page numbers often share the last PDF text line with
            # the dotted leader; do not require a separate page-number object.
            joined = " ".join(item["text"] for item in sorted(row, key=lambda item: item["bbox"][0]))
            match = re.match(r"^(.+?)\s+(\d+|[ivxlcdm]+)$", joined)
            if not match:
                continue
            title, label = match.groups()
            title = re.sub(r"(?:\.\s*){2,}", " ", title).strip()
            title = re.sub(r"\s+", " ", title)
            if title:
                result.append({"contentsPdfPage": page_number, "text": title,
                               "printedPage": label,
                               "targetPdfPageCandidate": int(label) + 14 if label.isdigit() else 11 if label == "xi" else None,
                               "status": "unreviewed"})
    return result


def render_pages(pages: list[int], dpi: int) -> None:
    """Use Poppler for original-page review images, never publish these images."""
    executable = shutil.which("pdftoppm")
    if executable is None:
        raise RuntimeError("pdftoppm is required for the original-page render step")
    target = TMP / "pages"
    target.mkdir(parents=True, exist_ok=True)
    for number in pages:
        output = target / f"page-{number:03d}.png"
        if output.exists():
            continue
        subprocess.run([executable, "-f", str(number), "-l", str(number), "-r", str(dpi),
                        "-singlefile", "-png", str(PDF), str(output.with_suffix(""))],
                       check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
        if number % 25 == 0:
            print(f"Rendered through PDF page {number}", flush=True)


def apply_source_corrections(pages: list[dict], source_sha256: str) -> None:
    """Keep explicit, PDF-verified locations when regenerating candidates."""
    path = BOOK / "source-inventory-corrections.json"
    if not path.is_file():
        return
    corrections = json.loads(path.read_text(encoding="utf-8"))
    if corrections["sourcePdfSha256"] != source_sha256:
        raise ValueError("Source corrections belong to a different PDF")
    by_page = {page["pdfPage"]: page for page in pages}
    for addition in corrections["equationAdditions"]:
        page = by_page[addition["pdfPage"]]
        candidate = addition["candidate"]
        existing = [item for item in page["equationCandidates"] if item["number"] == candidate["number"]]
        if not existing:
            page["equationCandidates"].append(candidate)
            page["equationCandidates"].sort(key=lambda item: (item["bbox"][1], item["bbox"][0]))


def extract() -> dict:
    document = fitz.open(PDF)
    if len(document) != 714:
        raise ValueError("Unexpected PDF page count; recheck ranges before using this tool")
    text_dir = TMP / "text"
    text_dir.mkdir(parents=True, exist_ok=True)
    pages = []
    all_text = []
    for index, page in enumerate(document):
        page_number = index + 1
        raw = page.get_text("text", sort=False)
        lines = page_lines(page)
        text_path = text_dir / f"page-{page_number:03d}.txt"
        text_path.write_text(raw, encoding="utf-8")
        all_text.append(f"\n\n===== PDF PAGE {page_number}; PRINTED LABEL {page.get_label()} =====\n\n{raw}")
        equations = [{"number": match.group(1), "bbox": line["bbox"], "status": "unreviewed",
                      "method": "isolated-parenthesized-number"}
                     for line in lines if (match := EQUATION.fullmatch(line["text"]))]
        captions = [{"kind": match.group(1).lower(), "number": match.group(2), "text": line["text"],
                     "bbox": line["bbox"], "status": "unreviewed"}
                    for line in lines if (match := CAPTION.match(line["text"]))]
        exercise_numbers = []
        if "Exercises" in raw[:100]:
            exercise_numbers = sorted(set(re.findall(r"(?m)^((?:\d+|[ABC])\.\d+)\s", normal(raw))),
                                      key=lambda value: [int(x) if x.isdigit() else x for x in value.split(".")])
        pages.append({
            "pdfPage": page_number, "printedLabel": page.get_label(),
            "chapterId": chapter_for_page(page_number).id,
            "sizePoints": [round(page.rect.width, 2), round(page.rect.height, 2)],
            "sourceTextFile": text_path.relative_to(ROOT).as_posix(),
            "reviewRenderFile": (TMP / "pages" / f"page-{page_number:03d}.png").relative_to(ROOT).as_posix(),
            "textCharacterCount": len(raw.strip()),
            "blankCandidate": not raw.strip() and not page.get_images() and not page.get_drawings(),
            "headingCandidates": heading_candidates(lines, page_number),
            "equationCandidates": equations, "captionCandidates": captions,
            "exerciseNumberCandidates": exercise_numbers,
            "embeddedRasterObjectCount": len(page.get_images()),
            "vectorDrawingObjectCount": len(page.get_drawings()),
            "reviewStatus": "unreviewed",
        })
    (TMP / "source-text.txt").write_text("".join(all_text), encoding="utf-8")
    original_contents = contents_rows(document)
    (TMP / "original-contents.txt").write_text(
        "\n\n".join(f"PDF {number}\n{document[number - 1].get_text()}" for number in range(7, 11)),
        encoding="utf-8")
    source_sha256 = hashlib.sha256(PDF.read_bytes()).hexdigest()
    apply_source_corrections(pages, source_sha256)
    return {
        "schemaVersion": 1, "bookId": BOOK_ID,
        "source": {"file": PDF.name, "sha256": source_sha256,
                   "pdfPages": len(document), "pageLabelRules": document.get_page_labels(),
                   "editionNote": "Publication page states: first published 2004; seventh printing with corrections 2009."},
        "scope": "Machine-extracted audit candidates only; not a translation, completeness finding, or semantic review.",
        "knownLimitations": [
            "Text extraction can reorder, omit, or corrupt formulas, ligatures, and diagram labels.",
            "Candidates are not a complete count of unnumbered formulas, tables, illustrations, or subheadings.",
            "Every page, figure, table cell, formula, footnote, exercise, and reference still requires original-page review.",
            "Original-page PNGs are review aids under tmp/convex and must never be embedded in the reading site.",
        ],
        "bookmarkCorrections": [
            {"title": "Appendices", "bookmarkPdfPage": 644, "actualPdfPage": 645,
             "evidence": "Printed contents page x gives 631; PDF page 644 is chapter 11 exercises, page 645 bears Appendices."},
            {"title": "References", "bookmarkPdfPage": 698, "actualPdfPage": 699,
             "evidence": "Printed contents page x gives 685; PDF page 698 is appendix C bibliography, page 699 bears References."},
        ],
        "originalContents": original_contents,
        "pdfBookmarksUncorrected": [{"level": level, "title": title, "pdfPage": page}
                                   for level, title, page in document.get_toc()],
        "chapters": [{"id": chapter.id, "titleEnglish": chapter.english_title,
                      "sourceMarkdown": f"translation/{chapter.source_name}",
                      "sourcePdfPages": [chapter.first, chapter.last],
                      "printedPageLabels": [document[chapter.first - 1].get_label(), document[chapter.last - 1].get_label()],
                      "blankPdfPageCandidates": [page["pdfPage"] for page in pages
                                                 if page["chapterId"] == chapter.id and page["blankCandidate"]],
                      "translationStatus": "unreviewed", "semanticReviewStatus": "unreviewed"}
                     for chapter in CHAPTERS],
        "pages": pages,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--render", metavar="PAGES", help="Render all, or a list such as 7-15,644-647,698-699")
    parser.add_argument("--render-only", action="store_true")
    parser.add_argument("--dpi", type=int, default=120)
    args = parser.parse_args()
    if args.render_only and not args.render:
        parser.error("--render-only requires --render")
    if not 72 <= args.dpi <= 600:
        parser.error("--dpi must be between 72 and 600")
    if not args.render_only:
        inventory = extract()
        path = BOOK / "source-inventory.json"
        path.write_text(json.dumps(inventory, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        counts = Counter(caption["kind"] for page in inventory["pages"] for caption in page["captionCandidates"])
        print(json.dumps({"output": path.relative_to(ROOT).as_posix(), "pages": len(inventory["pages"]),
                          "headingCandidates": sum(len(page["headingCandidates"]) for page in inventory["pages"]),
                          "equationCandidates": sum(len(page["equationCandidates"]) for page in inventory["pages"]),
                          "captionCandidates": counts, "semanticReview": "NOT PERFORMED"}, ensure_ascii=False), flush=True)
    if args.render:
        render_pages(parse_pages(args.render), args.dpi)


if __name__ == "__main__":
    main()
