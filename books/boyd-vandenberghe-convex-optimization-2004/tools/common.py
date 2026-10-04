"""Book-local paths and ranges checked against the supplied PDF's original pages."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BOOK_ID = "boyd-vandenberghe-convex-optimization-2004"
BOOK = ROOT / "books" / BOOK_ID
TMP = ROOT / "tmp" / "convex"
PDF_NAME = "Convex Optimization – Boyd and Vandenberghe.pdf"
PDF = ROOT / PDF_NAME


@dataclass(frozen=True)
class Chapter:
    id: str
    first: int
    last: int
    english_title: str
    source_name: str
    guide_required: bool = False


# Ranges include intervening blank pages, which remain explicit in the source
# ledger but do not create artificial reading content. PDF page != printed page.
# The PDF bookmarks for Appendices and References are one page early.
CHAPTERS = [
    Chapter("frontmatter", 1, 6, "Title, publication information, dedication", "frontmatter.md"),
    Chapter("contents", 7, 10, "Contents", "contents.md"),
    Chapter("preface", 11, 14, "Preface", "preface.md"),
    Chapter("01", 15, 32, "Introduction", "chapter-01.md", True),
    Chapter("part-I", 33, 34, "Part I: Theory", "part-I.md"),
    Chapter("02", 35, 80, "Convex sets", "chapter-02.md", True),
    Chapter("03", 81, 140, "Convex functions", "chapter-03.md", True),
    Chapter("04", 141, 228, "Convex optimization problems", "chapter-04.md", True),
    Chapter("05", 229, 302, "Duality", "chapter-05.md", True),
    Chapter("part-II", 303, 304, "Part II: Applications", "part-II.md"),
    Chapter("06", 305, 364, "Approximation and fitting", "chapter-06.md", True),
    Chapter("07", 365, 410, "Statistical estimation", "chapter-07.md", True),
    Chapter("08", 411, 468, "Geometric problems", "chapter-08.md", True),
    Chapter("part-III", 469, 470, "Part III: Algorithms", "part-III.md"),
    Chapter("09", 471, 534, "Unconstrained minimization", "chapter-09.md", True),
    Chapter("10", 535, 574, "Equality constrained minimization", "chapter-10.md", True),
    Chapter("11", 575, 644, "Interior-point methods", "chapter-11.md", True),
    Chapter("appendices", 645, 646, "Appendices", "appendices.md"),
    Chapter("A", 647, 666, "Mathematical background", "chapter-A.md", True),
    Chapter("B", 667, 674, "Problems involving two quadratic functions", "chapter-B.md", True),
    Chapter("C", 675, 698, "Numerical linear algebra background", "chapter-C.md", True),
    Chapter("references", 699, 710, "References", "references.md"),
    Chapter("notation", 711, 714, "Notation", "notation.md"),
]
CHAPTER_BY_ID = {chapter.id: chapter for chapter in CHAPTERS}


def chapter_for_page(page: int) -> Chapter:
    return next(chapter for chapter in CHAPTERS if chapter.first <= page <= chapter.last)


def parse_pages(value: str, *, maximum: int = 714) -> list[int]:
    if value == "all":
        return list(range(1, maximum + 1))
    pages: set[int] = set()
    for part in value.split(","):
        if "-" in part:
            first, last = map(int, part.split("-", 1))
            if first > last:
                raise ValueError(f"Descending page range: {part}")
            pages.update(range(first, last + 1))
        else:
            pages.add(int(part))
    if not pages or min(pages) < 1 or max(pages) > maximum:
        raise ValueError(f"PDF pages must be between 1 and {maximum}")
    return sorted(pages)
