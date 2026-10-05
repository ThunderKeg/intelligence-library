"""Build reviewed MacKay chapter, figure, table, formula, and exercise links."""

from __future__ import annotations

import json
from pathlib import Path
import re


BOOK = Path(__file__).resolve().parents[1]
ROOT = BOOK.parents[1]
BOOK_ID = BOOK.name
OUTPUT = BOOK / "reference-index.json"
KINDS = ("chapter", "part", "section", "figure", "table", "algorithm",
         "formula", "exercise", "example")
NUMBER = r"(?:[A-C]|\d+)\.\d+(?:\.\d+)?"
NUMBERED = re.compile(rf"^\(?({NUMBER})\)?$")
SECTION = re.compile(rf"^{NUMBER}$")
LABELS = {
    "figure": re.compile(rf"^图\s*({NUMBER})(?![\d.])"),
    "table": re.compile(rf"^表\s*({NUMBER})(?![\d.])"),
    "algorithm": re.compile(rf"^算法\s*({NUMBER})(?![\d.])"),
    "exercise": re.compile(rf"^[▷▶*＊∗]?\s*习题\s*({NUMBER})(?![\d.])"),
    "example": re.compile(rf"^(?:示例|例)\s*({NUMBER})(?![\d.])"),
}
ALGORITHM_TITLE = re.compile(rf"^算法\s*({NUMBER})(?![\d.])\u3000")


def registered_chapters() -> list[tuple[str, Path]]:
    source = (ROOT / "books.js").read_text(encoding="utf-8")
    marker = f'id: "{BOOK_ID}"'
    if source.count(marker) != 1:
        raise ValueError("MacKay registration missing or duplicated")
    section = source.split(marker, 1)[1].split('\n  {\n    id: "', 1)[0]
    routes = re.findall(r'\{ id: "([^"]+)",[^\n]*content: "([^"]+)" \}', section)
    if len(routes) != 81 or len({chapter_id for chapter_id, _ in routes}) != 81:
        raise ValueError(f"Expected 81 distinct MacKay reading units, got {len(routes)}")
    result = []
    for chapter_id, relative in routes:
        if relative != f"books/{BOOK_ID}/chapter-{chapter_id}.json":
            raise ValueError(f"Unexpected registered path: {relative}")
        result.append((chapter_id, ROOT / relative))
    return result


def build_index() -> dict:
    targets: dict[str, dict[str, dict[str, str]]] = {kind: {} for kind in KINDS}
    ranks: dict[str, dict[str, int]] = {kind: {} for kind in KINDS}
    known_ids: dict[str, set[str]] = {}

    def add(kind: str, number: str, chapter: str, block: str, rank: int = 1) -> None:
        candidate = {"chapter": chapter, "block": block}
        previous = targets[kind].get(number)
        if previous is None or rank > ranks[kind].get(number, 0):
            targets[kind][number] = candidate
            ranks[kind][number] = rank
        elif previous != candidate and rank == ranks[kind][number]:
            raise ValueError(f"Ambiguous {kind} {number}: {previous} vs {candidate}")

    for chapter_id, path in registered_chapters():
        chapter = json.loads(path.read_text(encoding="utf-8"))
        if chapter.get("bookId") != BOOK_ID or not chapter.get("blocks"):
            raise ValueError(f"Invalid registered chapter: {path}")
        known_ids[chapter_id] = set()
        first = chapter["toc"][0]["block"]
        if chapter_id.isdigit() and int(chapter_id) in range(1, 51):
            add("chapter", str(int(chapter_id)), chapter_id, first)
        if chapter_id in {"A", "B", "C"}:
            add("chapter", chapter_id, chapter_id, first)
        if chapter_id in {"I", "II", "III", "IV", "V", "VI", "VII"}:
            chinese = {"I": "一", "II": "二", "III": "三", "IV": "四",
                       "V": "五", "VI": "六", "VII": "七"}[chapter_id]
            add("part", chinese, chapter_id, first)
        for entry in chapter["toc"]:
            if SECTION.fullmatch(entry["number"]):
                add("section", entry["number"], chapter_id, entry["block"])

        def visit(blocks: list[dict]) -> None:
            for index, block in enumerate(blocks):
                block_id = block["id"]
                if block_id in known_ids[chapter_id]:
                    raise ValueError(f"Duplicate block id: {chapter_id} {block_id}")
                known_ids[chapter_id].add(block_id)
                kind = block["kind"]
                text = block.get("text", "")
                caption = block.get("caption", "")
                label = block.get("label", "")
                if kind == "formula":
                    match = NUMBERED.fullmatch(block.get("number", ""))
                    if match:
                        add("formula", match[1], chapter_id, block_id)
                if kind == "exercise":
                    match = LABELS["exercise"].match(label or text)
                    if match:
                        add("exercise", match[1], chapter_id, block_id)
                if kind in ("heading", "paragraph"):
                    match = LABELS["example"].match(text)
                    if match:
                        continuation = text[match.end():].lstrip().startswith(("（续）", "(续)"))
                        add("example", match[1], chapter_id, block_id,
                            rank=3 if kind == "heading" else 1 if continuation else 2)
                if kind in ("figure", "table") and caption:
                    for target_kind in ("figure", "table", "algorithm"):
                        match = LABELS[target_kind].match(caption)
                        if match:
                            add(target_kind, match[1], chapter_id, block_id, rank=3)
                if kind in ("figure", "table"):
                    previous = blocks[index - 1] if index else None
                    if previous and previous["kind"] == "paragraph":
                        match = LABELS[kind].match(previous.get("text", ""))
                        if match:
                            add(kind, match[1], chapter_id, block_id, rank=2)
                if kind == "caption":
                    for target_kind in ("figure", "table", "algorithm"):
                        match = LABELS[target_kind].match(text)
                        if not match:
                            continue
                        previous = blocks[index - 1] if index else None
                        use_previous = previous and previous["kind"] == target_kind
                        if target_kind == "algorithm" and previous:
                            use_previous = previous["kind"] in ("box", "code", "table")
                        target_block = previous["id"] if use_previous else block_id
                        add(target_kind, match[1], chapter_id, target_block,
                            rank=2 if use_previous else 1)
                if kind == "paragraph":
                    match = ALGORITHM_TITLE.match(text)
                    if match:
                        previous = blocks[index - 1] if index else None
                        use_previous = previous and previous["kind"] in ("box", "code")
                        target_block = previous["id"] if use_previous else block_id
                        add("algorithm", match[1], chapter_id, target_block,
                            rank=3 if use_previous else 2)
                    for target_kind in ("figure", "table", "algorithm"):
                        match = LABELS[target_kind].match(text)
                        if not match:
                            continue
                        previous = blocks[index - 1] if index else None
                        if previous and previous["kind"] == target_kind:
                            add(target_kind, match[1], chapter_id, previous["id"], rank=2)
                if kind == "box":
                    visit(block.get("blocks", []))

        visit(chapter["blocks"])

    # The printed text calls Figure 4.10 a table and Algorithm 30.1 a figure.
    # Both aliases point to their existing, independently reviewed source objects.
    for alias_kind, alias_number, source_kind, source_number in (
            ("table", "4.10", "figure", "4.10"),
            ("figure", "30.1", "algorithm", "30.1")):
        target = targets[source_kind][source_number]
        add(alias_kind, alias_number, target["chapter"], target["block"], rank=3)
    # This printed "figure" is an algorithm paragraph, so retain the jump only.
    targets["figure"]["30.1"]["preview"] = False
    # The caption for Figure 47.2 follows its image and three translated
    # panel notes; the link should land at the image itself.
    add("figure", "47.2", "47", "p570-b001", rank=4)

    for kind, entries in targets.items():
        for number, target in entries.items():
            if target["block"] not in known_ids[target["chapter"]]:
                raise ValueError(f"Missing {kind} {number}: {target}")
    return {"bookId": BOOK_ID,
            "targets": {kind: dict(sorted(entries.items()))
                        for kind, entries in targets.items()}}


def main() -> None:
    index = build_index()
    OUTPUT.write_text(json.dumps(index, ensure_ascii=False, indent=2) + "\n",
                      encoding="utf-8")
    print(json.dumps({kind: len(entries) for kind, entries in index["targets"].items()},
                     ensure_ascii=False))


if __name__ == "__main__":
    main()
