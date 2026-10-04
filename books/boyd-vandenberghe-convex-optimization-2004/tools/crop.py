"""Render one author-inspected source figure crop, with an auditable sidecar.

Coordinates are PDF points (top-left origin). The caller must inspect the original
page, choose the exact figure rectangle, and translate every English diagram label.
This command cannot establish whether a crop contains the complete figure.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import fitz

from common import BOOK, PDF, ROOT


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--page", type=int, required=True)
    parser.add_argument("--rect", type=float, nargs=4, metavar=("X0", "Y0", "X1", "Y1"), required=True)
    parser.add_argument("--output", type=Path, required=True, help="PNG under this book's assets/")
    parser.add_argument("--scale", type=float, default=3)
    args = parser.parse_args()
    target = args.output.resolve()
    if not target.is_relative_to((BOOK / "assets").resolve()) or target.suffix.lower() != ".png":
        parser.error("--output must be a .png under this book's assets/")
    if target.exists() or target.with_suffix(".source.json").exists():
        parser.error("Output already exists; coordinate with the owner before replacing it")
    if not 1 <= args.scale <= 6:
        parser.error("--scale must be between 1 and 6")
    with fitz.open(PDF) as document:
        if not 1 <= args.page <= len(document):
            parser.error("Source page out of range")
        page = document[args.page - 1]
        rect = fitz.Rect(args.rect)
        if rect.is_empty or not page.rect.contains(rect):
            parser.error("Invalid crop rectangle")
        if rect.get_area() >= .80 * page.rect.get_area() or (rect.width >= .90 * page.rect.width and rect.height >= .85 * page.rect.height):
            parser.error("Whole-page or nearly whole-page source images are prohibited")
        target.parent.mkdir(parents=True, exist_ok=True)
        page.get_pixmap(matrix=fitz.Matrix(args.scale, args.scale), clip=rect, alpha=False).save(target)
    provenance = {"sourcePdf": PDF.name, "pdfPage": args.page, "cropPoints": args.rect, "scale": args.scale,
                  "imageSha256": hashlib.sha256(target.read_bytes()).hexdigest(), "reviewStatus": "unreviewed"}
    target.with_suffix(".source.json").write_text(json.dumps(provenance, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(target.relative_to(ROOT).as_posix())
    print("The crop still requires independent original-page and label-translation review.")


if __name__ == "__main__":
    main()
