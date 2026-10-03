"""Compare compiled Bishop chapters with page-level labels in the supplied PDF.

This is a locator check, not a substitute for reading each original page.
"""

import argparse
import json
import re
from collections import Counter
from pathlib import Path

import fitz

from build_bishop_chapters import BOOK, PDF, chapter_ranges


def original_labels(document: fitz.Document, number: int | str, start: int, end: int) -> dict[str, set[str]]:
    labels = {"figures": set(), "tables": set(), "algorithms": set(), "formulas": set()}
    patterns = {
        "figures": re.compile(rf"^Figure\s+({number}\.\d+)\b"),
        "tables": re.compile(rf"^Table\s+({number}\.\d+)\b"),
        "algorithms": re.compile(rf"^Algorithm\s+({number}\.\d+)\b"),
        "formulas": re.compile(rf"\(({number}\.\d+)\)$"),
    }
    for page in range(start, end + 1):
        for raw_line in document[page - 1].get_text().splitlines():
            line = raw_line.strip()
            for key, pattern in patterns.items():
                match = pattern.search(line) if key == "formulas" else pattern.match(line)
                if match:
                    labels[key].add(match.group(1))
    return labels


def compiled_labels(chapter: dict, number: int | str) -> dict[str, set[str]]:
    result = {"figures": set(), "tables": set(), "algorithms": set(), "formulas": set()}
    for block in chapter["blocks"]:
        if block["kind"] == "figure":
            match = re.search(rf"(?:图|Figure)\s*({number}\.\d+)\b", block.get("caption", ""))
            if match:
                result["figures"].add(match.group(1))
        elif block["kind"] == "table":
            match = re.search(rf"(?:表|Table)\s*({number}\.\d+)\b", block.get("caption", ""))
            if match:
                result["tables"].add(match.group(1))
        elif block["kind"] == "formula":
            match = re.fullmatch(rf"\(({number}\.\d+)\)", block.get("number", ""))
            if match:
                result["formulas"].add(match.group(1))
        if block["kind"] == "paragraph":
            match = re.match(rf"^(?:算法|Algorithm)\s*({number}\.\d+)\b", block.get("text", ""))
            if match:
                result["algorithms"].add(match.group(1))
    return result


def audit(number: int | str, document: fitz.Document, page_range: tuple[int, int]) -> bool:
    path = BOOK / (f"chapter-{number:02d}.json" if isinstance(number, int)
                   else f"appendix-{number.lower()}.json" if number in {"A", "B", "C"}
                   else f"{number}.json")
    if not path.exists():
        print(f"Chapter {number}: no compiled JSON")
        return False
    chapter = json.loads(path.read_text(encoding="utf-8"))
    expected = original_labels(document, number, *page_range)
    actual = compiled_labels(chapter, number)
    page_counts = Counter(block["pdfPage"] for block in chapter["blocks"])
    problems = []
    for kind in expected:
        missing = sorted(expected[kind] - actual[kind], key=lambda value: int(value.split(".")[1]))
        extra = sorted(actual[kind] - expected[kind], key=lambda value: int(value.split(".")[1]))
        if missing:
            problems.append(f"{kind} detected in PDF but absent from JSON: {', '.join(missing)}")
        if extra:
            problems.append(f"{kind} in JSON but not detected in PDF text: {', '.join(extra)}")
    empty_pages = [page for page in range(page_range[0], page_range[1] + 1) if not page_counts[page]]
    if empty_pages:
        problems.append(f"PDF pages with no compiled blocks: {empty_pages}")
    bad_math = [block["id"] for block in chapter["blocks"] if block["kind"] == "formula" and not block.get("mathml")]
    if bad_math:
        problems.append(f"Formula blocks lacking MathML: {', '.join(bad_math)}")
    print(f"Chapter {number}: PDF {page_range[0]}–{page_range[1]}, {len(chapter['blocks'])} blocks, "
          f"{len(chapter['images'])} image files")
    for kind in expected:
        print(f"  {kind}: PDF labels {len(expected[kind])}, JSON labels {len(actual[kind])}")
    for problem in problems:
        print(f"  REVIEW: {problem}")
    return not problems


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--chapter", action="append", help="chapter/unit (repeatable); default: all compiled")
    args = parser.parse_args()
    ranges: dict[int | str, tuple[int, int]] = {
        **chapter_ranges(), "A": (618, 624), "B": (625, 627), "C": (628, 631),
        "frontmatter": (1, 4), "contents": (11, 20),
        "bibliography": (632, 647), "index": (648, 656),
    }
    numbers = (
        [int(value) if value.isdigit() else value.upper() if value.upper() in {"A", "B", "C"}
         else value.lower() for value in args.chapter]
        if args.chapter else
        [number for number in ranges if (
            BOOK / (f"chapter-{number:02d}.json" if isinstance(number, int)
                    else f"appendix-{number.lower()}.json" if number in {"A", "B", "C"}
                    else f"{number}.json")).exists()]
    )
    with fitz.open(PDF) as document:
        passed = all([audit(number, document, ranges[number]) for number in numbers])
    raise SystemExit(0 if passed else 1)


if __name__ == "__main__":
    main()
