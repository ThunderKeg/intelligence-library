"""Build Bishop reference targets and the complete offline image manifest."""

import hashlib
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BOOK_ID = "bishop-deep-learning-2024"
BOOK = ROOT / "books" / BOOK_ID
UNITS = ["frontmatter", "chapter-00", "contents"] + [
    f"chapter-{number:02d}" for number in range(1, 21)
] + [f"appendix-{letter}" for letter in "abc"] + ["bibliography", "index"]
NUMBER = r"(?:[A-C]|\d+)\.\d+"
HEADING_NUMBER = re.compile(rf"^(({NUMBER})(?:\.\d+)?)\s")
FIGURE_LABEL = re.compile(rf"^图\s*({NUMBER})(?!\d)")
TABLE_LABEL = re.compile(rf"^表\s*({NUMBER})(?!\d)")
ALGORITHM_LABEL = re.compile(rf"^算法\s*({NUMBER})(?!\d)")
FORMULA_LABEL = re.compile(rf"^\(({NUMBER})\)$")


def write_json(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> None:
    targets: dict[str, dict[str, dict[str, str]]] = {
        kind: {} for kind in ("chapter", "section", "figure", "table", "formula", "algorithm")
    }
    assets: list[str] = []
    seen_assets: set[str] = set()

    def add(kind: str, number: str, chapter: str, block: str) -> None:
        entry = {"chapter": chapter, "block": block}
        previous = targets[kind].setdefault(number, entry)
        if previous != entry:
            raise ValueError(f"Duplicate {kind} {number}: {previous} and {entry}")

    for unit in UNITS:
        chapter = unit.removeprefix("chapter-") if unit.startswith("chapter-") else (
            unit[-1].upper() if unit.startswith("appendix-") else unit
        )
        data = json.loads((BOOK / f"{unit}.json").read_text(encoding="utf-8"))
        if data.get("bookId") != BOOK_ID:
            raise ValueError(f"Unexpected bookId in {unit}")
        blocks = data["blocks"]
        if unit.startswith("chapter-") and unit != "chapter-00":
            add("chapter", str(int(chapter)), chapter, blocks[0]["id"])
        elif unit.startswith("appendix-"):
            add("chapter", chapter, chapter, blocks[0]["id"])

        for index, block in enumerate(blocks):
            kind = block["kind"]
            block_id = block["id"]
            if kind == "heading":
                match = HEADING_NUMBER.match(block.get("text", ""))
                if match:
                    add("section", match.group(1), chapter, block_id)
            elif kind == "figure":
                caption = block.get("caption", "")
                match = FIGURE_LABEL.match(caption)
                if match:
                    add("figure", match.group(1), chapter, block_id)
                match = ALGORITHM_LABEL.match(caption)
                if match:
                    add("algorithm", match.group(1), chapter, block_id)
            elif kind == "table":
                match = TABLE_LABEL.match(block.get("caption", ""))
                if match:
                    add("table", match.group(1), chapter, block_id)
            elif kind == "formula":
                match = FORMULA_LABEL.match(block.get("number", ""))
                if match:
                    add("formula", match.group(1), chapter, block_id)
            elif kind == "code" and index:
                previous = blocks[index - 1]
                match = ALGORITHM_LABEL.match(previous.get("text", ""))
                if match and match.group(1) not in targets["algorithm"]:
                    add("algorithm", match.group(1), chapter, previous["id"])

        for asset in data.get("images", []):
            if not asset.startswith(f"books/{BOOK_ID}/assets/") or ".." in Path(asset).parts:
                raise ValueError(f"Invalid image path: {asset}")
            if not (ROOT / asset).is_file():
                raise FileNotFoundError(asset)
            if asset not in seen_assets:
                seen_assets.add(asset)
                assets.append(asset)

    digest = hashlib.sha256()
    total_bytes = 0
    for asset in assets:
        contents = (ROOT / asset).read_bytes()
        digest.update(asset.encode("utf-8"))
        digest.update(hashlib.sha256(contents).digest())
        total_bytes += len(contents)

    write_json(BOOK / "reference-index.json", {"bookId": BOOK_ID, "targets": targets})
    write_json(BOOK / "offline-images.json", {
        "bookId": BOOK_ID,
        "version": digest.hexdigest()[:20],
        "totalBytes": total_bytes,
        "assets": assets,
    })
    print(f"Reference targets: {', '.join(f'{kind}={len(items)}' for kind, items in targets.items())}")
    print(f"Offline images: {len(assets)}, {total_bytes} bytes, version {digest.hexdigest()[:20]}")


if __name__ == "__main__":
    main()
