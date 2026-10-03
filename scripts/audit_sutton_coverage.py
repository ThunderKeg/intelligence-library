"""Check the PDF's 548 physical pages against Sutton/Barto source and reader data."""

import csv
import hashlib
import json
import re
import subprocess
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BOOK = ROOT / "books" / "sutton-barto-reinforcement-learning-2e"
PDF = ROOT / "Reinforcement_ Learning_An_Introduction.pdf"
EXPECTED_SHA256 = "2DD0D71D9EE883FBEB99F9B888C65AC3255FAE2512203D11B18E838BEFFFE9A6"
CHAPTERS = {2: (25, 46), 3: (47, 72), 4: (73, 90), 5: (91, 118), 6: (119, 140),
            7: (141, 158), 8: (159, 194), 9: (197, 242), 10: (243, 256),
            11: (257, 286), 12: (287, 320), 13: (321, 338), 14: (341, 376),
            15: (377, 420), 16: (421, 458), 17: (459, 480)}


def reader_blocks(inventory: dict[int, Counter] | None = None) -> Counter:
    counts: Counter = Counter()
    for data_path in BOOK.glob("chapter-*.json"):
        chapter = data_path.stem.removeprefix("chapter-")
        data = json.loads(data_path.read_text(encoding="utf-8"))
        assert data["bookId"] == BOOK.name

        def visit(items: list[dict]) -> None:
            for item in items:
                if item["kind"] == "box":
                    if inventory is not None and item.get("algorithm"):
                        physical = item["page"] if chapter == "00" else item["page"] + 22
                        inventory.setdefault(physical, Counter())["algorithm_boxes"] += 1
                    visit(item["blocks"])
                    continue
                number = item.get("page")
                if not isinstance(number, int):
                    raise ValueError(f"No page for {chapter}: {item.get('id')}")
                physical = number if chapter == "00" else number + 22
                if not 1 <= physical <= 548:
                    raise ValueError(f"Block out of source range: {chapter} {item.get('id')}")
                counts[physical] += 1
                if inventory is not None:
                    kinds = inventory.setdefault(physical, Counter())
                    kinds[item["kind"]] += 1
                    if item["kind"] == "figure":
                        kinds["figure_annotations"] += len(item.get("annotations", []))
                if item["kind"] in ("figure", "image"):
                    asset = BOOK / item["src"]
                    if not asset.is_file():
                        raise ValueError(f"Missing figure: {asset}")

        visit(data["blocks"])
    return counts


def manifest() -> list[dict]:
    rows = []

    def add(physical: int, source: str, section: str, review: str) -> None:
        path = BOOK / source
        if not path.is_file() or (not path.read_text(encoding="utf-8").strip() and physical != 6):
            raise ValueError(f"Missing or empty source page: {path}")
        rows.append({"pdf_physical_page": physical,
                     "book_page": "front matter" if physical <= 22 else str(physical - 22),
                     "section": section, "source": source, "review": review})

    for physical in range(1, 23):
        add(physical, f"frontmatter/page-{physical:02d}.md", "front matter", "REVIEW-FRONTMATTER.md")
    for printed in range(1, 23):
        add(printed + 22, f"translation/page-{printed:02d}.md", "chapter 1", "REVIEW-CH1.md")
    for printed in (23, 24):
        add(printed + 22, "parts/part-01.md", "part I", "REVIEW-CH2.md")
    for chapter, (first, last) in CHAPTERS.items():
        if chapter == 9:
            for printed in (195, 196):
                add(printed + 22, "parts/part-02.md", "part II", "REVIEW-PART2.md")
        if chapter == 14:
            for printed in (339, 340):
                add(printed + 22, "parts/part-03.md", "part III", "REVIEW-CH14.md")
        for printed in range(first, last + 1):
            add(printed + 22, f"translation/chapter-{chapter:02d}/page-{printed:02d}.md",
                f"chapter {chapter}", f"REVIEW-CH{chapter}.md")
    for physical in range(503, 541):
        review = "REVIEW-REFS-503-527.md" if physical <= 527 else "REVIEW-REFS-528-540.md"
        add(physical, f"backmatter/references/page-{physical}.md", "references", review)
    for physical in range(541, 547):
        add(physical, f"backmatter/index/page-{physical}.md", "index", "REVIEW-INDEX.md")
    for physical in range(547, 549):
        add(physical, f"backmatter/series/page-{physical}.md", "series bibliography", "REVIEW-SERIES.md")
    numbers = [row["pdf_physical_page"] for row in rows]
    if len(rows) != 548 or sorted(numbers) != list(range(1, 549)):
        raise ValueError("PDF physical-page manifest has a gap or duplicate")
    return rows


def main() -> None:
    digest = hashlib.sha256(PDF.read_bytes()).hexdigest().upper()
    if digest != EXPECTED_SHA256:
        raise ValueError(f"Source PDF changed: {digest}")
    info = subprocess.run(["pdfinfo", str(PDF)], capture_output=True, text=True,
                          encoding="utf-8", errors="replace", check=True).stdout
    match = re.search(r"(?m)^Pages:\s+(\d+)$", info)
    if not match or int(match[1]) != 548:
        raise ValueError("Expected a 548-page PDF")
    inventory: dict[int, Counter] = {}
    counts = reader_blocks(inventory)
    rows = manifest()
    for row in rows:
        physical = row["pdf_physical_page"]
        kinds = inventory.get(physical, Counter())
        row["reader_blocks"] = counts[physical]
        row["figures"] = kinds["figure"]
        row["figure_annotations"] = kinds["figure_annotations"]
        row["tables"] = kinds["table"]
        row["formulas"] = kinds["formula"]
        row["code_blocks"] = kinds["code"]
        row["algorithm_boxes"] = kinds["algorithm_boxes"]
        row["exercises"] = kinds["exercise"]
        row["footnotes"] = kinds["footnote"]
        row["lists"] = kinds["list"]
    zeros = [row["pdf_physical_page"] for row in rows if row["reader_blocks"] == 0]
    # These pages are documented as blank, or their continuation is merged
    # into the preceding paragraph or source box.
    expected_zeros = {6, 46, 68, 94, 140, 216, 218, 362, 442, 480}
    if set(zeros) != expected_zeros:
        raise ValueError(f"Unexpected reader-empty physical pages: {zeros}")
    output = BOOK / "PAGE-AUDIT.csv"
    with output.open("w", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    print(f"PASS: PDF SHA-256 and 548-page count; {len(rows)} source-page mappings; "
          f"{sum(counts.values())} reader blocks; {len(zeros)} documented reader-empty pages")
    print(f"Wrote {output}")


if __name__ == "__main__":
    main()
