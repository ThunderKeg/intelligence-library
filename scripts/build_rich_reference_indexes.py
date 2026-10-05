"""Build exact figure and equation preview targets for rich-HTML books.

Usage: python scripts/build_rich_reference_indexes.py [--check]
"""

import argparse
import json
import re
from pathlib import Path

from bs4 import BeautifulSoup


ROOT = Path(__file__).resolve().parents[1]
BOOKS = {
    "shannon-mathematical-theory-1948": {"figure": "figure[id^='fig-']"},
    "boyd-vandenberghe-convex-optimization-2004": {
        "figure": "figure[id^='fig-']",
        "formula": ".book-formula[id^='eq-']",
    },
}


def build(book_id, selectors):
    book_dir = ROOT / "books" / book_id
    targets = {kind: {} for kind in selectors}
    for path in sorted(book_dir.glob("chapter-*.json")):
        chapter = json.loads(path.read_text(encoding="utf-8"))
        if chapter.get("bookId") != book_id or not chapter.get("chapterId"):
            raise ValueError(f"Invalid chapter: {path}")
        for block in chapter["blocks"]:
            if block.get("kind") != "rich" or not block.get("html"):
                continue
            soup = BeautifulSoup(block["html"], "html.parser")
            for kind, selector in selectors.items():
                prefix = "fig-" if kind == "figure" else "eq-"
                for element in soup.select(selector):
                    element_id = element["id"]
                    number = element_id.removeprefix(prefix).replace("-", ".")
                    valid = re.fullmatch(r"\d+" if book_id.startswith("shannon-") else r"(?:[A-C]|\d+)(?:\.\d+)+", number)
                    if not valid:
                        if kind == "figure":
                            continue  # Exercise artwork has a fig- ID but no figure number.
                        raise ValueError(f"Invalid {kind} ID: {element_id}")
                    if kind == "figure" and element.get("data-figure") and element["data-figure"] != number:
                        raise ValueError(f"Figure number mismatch: {element_id}")
                    target = {"chapter": chapter["chapterId"], "block": block["id"], "element": element_id}
                    previous = targets[kind].setdefault(number, target)
                    if previous != target:
                        raise ValueError(f"Duplicate {kind} {number}: {previous}, {target}")
    if not targets["figure"] or ("formula" in selectors and not targets["formula"]):
        raise ValueError(f"No preview targets found for {book_id}")
    return {"bookId": book_id, "targets": {kind: dict(sorted(entries.items())) for kind, entries in targets.items()}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Verify indexes without writing")
    args = parser.parse_args()
    for book_id, selectors in BOOKS.items():
        index = build(book_id, selectors)
        path = ROOT / "books" / book_id / "reference-index.json"
        content = json.dumps(index, ensure_ascii=False, indent=2) + "\n"
        if args.check:
            if path.read_text(encoding="utf-8") != content:
                raise ValueError(f"Outdated index: {path}")
        else:
            path.write_text(content, encoding="utf-8")
        print(book_id, {kind: len(entries) for kind, entries in index["targets"].items()})


if __name__ == "__main__":
    main()
