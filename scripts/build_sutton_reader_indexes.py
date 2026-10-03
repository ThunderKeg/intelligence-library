"""Build Sutton/Barto navigation targets and the complete offline image list."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BOOK_ID = "sutton-barto-reinforcement-learning-2e"
BOOK = ROOT / "books" / BOOK_ID
CHAPTERS = (
    "00", "01", "I", "02", "03", "04", "05", "06", "07", "08", "II",
    "09", "10", "11", "12", "13", "III", "14", "15", "16", "17",
    "REF", "IDX", "SERIES",
)
NUMBER = r"\d+\.\d+"
SECTION = re.compile(rf"{NUMBER}(?:\.\d+)?\Z")
FIGURE = re.compile(rf"^图\s*({NUMBER})(?![\d.])")
TABLE = re.compile(rf"^表\s*({NUMBER})(?![\d.])")
EXERCISE = re.compile(rf"^[∗＊*]?习题\s*({NUMBER})(?![\d.])")
EXAMPLE = re.compile(rf"^(?:示例|例)\s*({NUMBER})(?=[：:\s])(.*)")


def write_json(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> None:
    registered = {path.stem.removeprefix("chapter-") for path in BOOK.glob("chapter-*.json")}
    if registered != set(CHAPTERS):
        raise ValueError(f"Unexpected chapter set: {sorted(registered ^ set(CHAPTERS))}")

    targets: dict[str, dict[str, dict[str, str]]] = {
        kind: {} for kind in ("chapter", "part", "section", "figure", "table", "formula", "exercise", "example")
    }
    example_ranks: dict[str, int] = {}
    assets: set[str] = set()
    block_ids: dict[str, set[str]] = {}

    def add(kind: str, number: str, chapter: str, block: str) -> None:
        entry = {"chapter": chapter, "block": block}
        previous = targets[kind].setdefault(number, entry)
        if previous != entry:
            raise ValueError(f"Duplicate {kind} {number}: {previous} and {entry}")

    for chapter in CHAPTERS:
        data = json.loads((BOOK / f"chapter-{chapter}.json").read_text(encoding="utf-8"))
        if data.get("bookId") != BOOK_ID or not data.get("blocks"):
            raise ValueError(f"Invalid chapter data: {chapter}")
        if chapter.isdigit() and int(chapter) > 0:
            add("chapter", str(int(chapter)), chapter, data["toc"][0]["block"])
        elif chapter in {"I": "一", "II": "二", "III": "三"}:
            add("part", {"I": "一", "II": "二", "III": "三"}[chapter], chapter, data["toc"][0]["block"])
        for entry in data["toc"]:
            if SECTION.fullmatch(entry["number"]):
                add("section", entry["number"], chapter, entry["block"])

        ids = block_ids.setdefault(chapter, set())

        def visit(blocks: list[dict]) -> None:
            for index, block in enumerate(blocks):
                if block["id"] in ids:
                    raise ValueError(f"Duplicate block ID: {chapter} {block['id']}")
                ids.add(block["id"])
                if block["kind"] == "box":
                    visit(block["blocks"])
                    continue
                kind = block["kind"]
                block_id = block["id"]
                text = block.get("text", "")
                if kind == "figure":
                    src = block["src"]
                    if not re.fullmatch(r"assets/[\w./-]+\.(?:png|jpe?g|webp|gif|svg)", src, re.I) or ".." in Path(src).parts:
                        raise ValueError(f"Invalid image path: {chapter} {src}")
                    asset = f"books/{BOOK_ID}/{src}"
                    if not (ROOT / asset).is_file():
                        raise FileNotFoundError(asset)
                    assets.add(asset)
                    match = FIGURE.match(block.get("caption", ""))
                    if match:
                        add("figure", match[1], chapter, block_id)
                elif kind == "formula" and re.fullmatch(NUMBER, block.get("number", "")):
                    add("formula", block["number"], chapter, block_id)
                elif kind == "exercise":
                    match = EXERCISE.match(block.get("label", ""))
                    if match:
                        add("exercise", match[1], chapter, block_id)
                elif kind == "table":
                    match = TABLE.match(block.get("caption", ""))
                    if match:
                        add("table", match[1], chapter, block_id)
                elif kind == "paragraph":
                    match = TABLE.match(text)
                    if match and index and blocks[index - 1]["kind"] == "table":
                        add("table", match[1], chapter, blocks[index - 1]["id"])

                if kind in {"heading", "paragraph"}:
                    match = EXAMPLE.match(text)
                    if match:
                        number = match[1]
                        rank = 3 if kind == "heading" else 2 if match[2].startswith(("：", ":")) else 1
                        if rank > example_ranks.get(number, 0):
                            targets["example"][number] = {"chapter": chapter, "block": block_id}
                            example_ranks[number] = rank

        visit(data["blocks"])

    for kind, entries in targets.items():
        for number, target in entries.items():
            if target["block"] not in block_ids[target["chapter"]]:
                raise ValueError(f"Missing {kind} target {number}: {target}")

    listed_assets = {f"books/{BOOK_ID}/assets/{path.name}" for path in (BOOK / "assets").iterdir() if path.is_file()}
    if assets != listed_assets:
        raise ValueError(f"Unmatched image files: {sorted(assets ^ listed_assets)}")
    ordered_assets = sorted(assets)
    digest = hashlib.sha256()
    total_bytes = 0
    for asset in ordered_assets:
        contents = (ROOT / asset).read_bytes()
        digest.update(asset.encode("utf-8"))
        digest.update(hashlib.sha256(contents).digest())
        total_bytes += len(contents)

    write_json(BOOK / "reference-index.json", {"bookId": BOOK_ID, "targets": targets})
    write_json(BOOK / "offline-images.json", {
        "bookId": BOOK_ID,
        "version": digest.hexdigest()[:20],
        "totalBytes": total_bytes,
        "assets": ordered_assets,
    })
    print("Reference targets:", ", ".join(f"{kind}={len(items)}" for kind, items in targets.items()))
    print(f"Offline images: {len(assets)}, {total_bytes} bytes, version {digest.hexdigest()[:20]}")


if __name__ == "__main__":
    main()
