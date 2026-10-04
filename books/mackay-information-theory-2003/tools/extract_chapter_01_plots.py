"""Render only the numbered plots from the local source PDF at 216 dpi."""

from pathlib import Path

import fitz


BOOK = Path(__file__).resolve().parents[3] / "Information Theory, Inference, and Learning Algorithms.pdf"
ASSETS = Path(__file__).resolve().parents[1] / "assets" / "chapter-01"
PLOTS = {
    # PDF physical page number, PDF coordinate rectangle (points).
    "figure-1-18.png": (26, (64, 112, 395, 292)),
    "figure-1-19.png": (27, (64, 112, 395, 292)),
}

with fitz.open(BOOK) as document:
    for filename, (pdf_page, rectangle) in PLOTS.items():
        page = document[pdf_page - 1]
        image = page.get_pixmap(matrix=fitz.Matrix(3, 3), clip=fitz.Rect(rectangle), alpha=False)
        image.save(ASSETS / filename)
