"""Render Bishop chapter 1 PDF pages for the bilingual facsimile reader."""

import sys
from pathlib import Path

import fitz
from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
PDF = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "Christopher M. Bishop, Hugh Bishop - Deep Learning_ Foundations and Concepts-Springer (2024).pdf"
OUTPUT = ROOT / "books" / "bishop-deep-learning-2024" / "pages"
OUTPUT.mkdir(parents=True, exist_ok=True)

with fitz.open(PDF) as document:
    for book_page in range(1, 23):
        pdf_index = book_page + 19
        page = document[pdf_index]
        pixmap = page.get_pixmap(matrix=fitz.Matrix(2, 2), colorspace=fitz.csRGB, alpha=False)
        image = Image.frombytes("RGB", (pixmap.width, pixmap.height), pixmap.samples)
        image.save(OUTPUT / f"page-{book_page:02d}.webp", "WEBP", quality=86, method=6)
        print(f"page {book_page:02d} -> {pixmap.width}x{pixmap.height}")
