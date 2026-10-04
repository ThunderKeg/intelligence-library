"""Check complete MacKay reader coverage, references, and local image assets."""

from __future__ import annotations

import argparse
from collections import Counter
from html.parser import HTMLParser
import json
from pathlib import Path
import re
from urllib.parse import parse_qs, urlsplit


BOOK = Path(__file__).resolve().parents[1]
ROOT = BOOK.parents[1]
BOOK_ID = BOOK.name
MANIFEST = json.loads((BOOK / "offline-images.json").read_text(encoding="utf-8"))
PARSER = argparse.ArgumentParser(description=__doc__)
PARSER.add_argument("--include-index-draft", action="store_true",
                    help="Audit all 640 pages before the index is formally registered")
PARSER.add_argument("--list-unreferenced", action="store_true",
                    help="List image files not directly referenced by chapter JSON")
ARGS = PARSER.parse_args()


class Links(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.anchors: set[str] = set()
        self.hrefs: list[str] = []
        self.srcs: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if values.get("id"):
            self.anchors.add(values["id"])
        if values.get("href"):
            self.hrefs.append(values["href"])
        if values.get("src"):
            self.srcs.append(values["src"])


def walk(value: object):
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from walk(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk(child)


source = (ROOT / "books.js").read_text(encoding="utf-8")
marker = f'id: "{BOOK_ID}"'
assert source.count(marker) == 1, "MacKay registration missing or duplicated"
section = source.split(marker, 1)[1].split('\n  {\n    id: "', 1)[0]
routes = re.findall(r'\{ id: "([^"]+)",[^\n]*content: "([^"]+)" \}', section)
assert routes and len(routes) == len({item[0] for item in routes})
assert all(path == f"books/{BOOK_ID}/chapter-{chapter_id}.json"
           for chapter_id, path in routes)
assert f'referenceIndex: "books/{BOOK_ID}/reference-index.json"' in section
if ARGS.include_index_draft:
    assert "IDX" not in {chapter_id for chapter_id, _ in routes}
    routes.append(("IDX", f"books/{BOOK_ID}/chapter-IDX.draft.json"))

pages = Counter()
anchors: dict[str, set[str]] = {}
hrefs: list[tuple[str, str]] = []
images: set[str] = set()
blocks_total = 0
toc_total = 0
all_block_ids: set[str] = set()
reference_blocks: dict[str, set[str]] = {}

for chapter_id, relative in routes:
    path = ROOT / relative
    chapter = json.loads(path.read_text(encoding="utf-8"))
    assert chapter["bookId"] == BOOK_ID, relative
    start, end = chapter["sourcePdfPages"]
    assert 1 <= start <= end <= 640, (chapter_id, start, end)
    blocks = chapter["blocks"]
    reference_blocks[chapter_id] = {
        item["id"] for item in walk(blocks) if "kind" in item and "id" in item}
    ids = [block["id"] for block in blocks]
    assert len(ids) == len(set(ids)), f"duplicate block id: {chapter_id}"
    assert not (set(ids) & all_block_ids), f"cross-chapter block id collision: {chapter_id}"
    all_block_ids.update(ids)
    assert blocks and blocks[0]["pdfPage"] == start and blocks[-1]["pdfPage"] == end
    assert [block["pdfPage"] for block in blocks] == sorted(
        block["pdfPage"] for block in blocks), f"out-of-order blocks: {chapter_id}"
    assert set(range(start, end + 1)) == {
        block["pdfPage"] for block in blocks}, f"page without block: {chapter_id}"
    for page in range(start, end + 1):
        pages[page] += 1

    local_anchors = {f"read-{block_id}" for block_id in ids}
    for item in chapter["toc"]:
        assert item["block"] in ids, (chapter_id, item)
    toc_total += len(chapter["toc"])
    blocks_total += len(blocks)
    parser = Links()
    for item in walk(blocks):
        if isinstance(item.get("html"), str):
            parser.feed(item["html"])
        for value in item.values():
            if isinstance(value, str) and value.startswith("assets/"):
                images.add(f"books/{BOOK_ID}/{value}")
    local_anchors.update(parser.anchors)
    anchors[chapter_id] = local_anchors
    hrefs.extend((chapter_id, href) for href in parser.hrefs)
    for src in parser.srcs:
        if src.startswith("assets/"):
            images.add(f"books/{BOOK_ID}/{src}")
        elif src.startswith(f"books/{BOOK_ID}/assets/"):
            images.add(src)

assert sorted(pages) == list(range(1, 641)), "PDF page coverage has gaps"
assert all(count == 1 for count in pages.values()), "PDF pages overlap"

reference_index = json.loads((BOOK / "reference-index.json").read_text(encoding="utf-8"))
assert reference_index["bookId"] == BOOK_ID
reference_targets = reference_index["targets"]
for kind, entries in reference_targets.items():
    for number, target in entries.items():
        assert target["chapter"] in reference_blocks, (kind, number, target)
        assert target["block"] in reference_blocks[target["chapter"]], (
            kind, number, target)
assert "16.5" not in reference_targets["formula"]
assert reference_targets["table"]["4.10"] == reference_targets["figure"]["4.10"]
assert reference_targets["figure"]["30.1"] == reference_targets["algorithm"]["30.1"]

reference_mentions = 0
unresolved_mentions: set[tuple[str, str, str, str]] = set()
number = r"(?:[A-C]|\d+)\.\d+(?:\.\d+)?"
mention_patterns = {
    kind: re.compile(rf"{prefix}\s*({number})(?![\d.])")
    for kind, prefix in (("figure", "图"), ("table", "表"),
                         ("algorithm", "算法"), ("exercise", "习题"))
}
mention_patterns["formula"] = re.compile(
    rf"(?:式|公式)\s*[（(]\s*({number})\s*[）)]")
for chapter_id, relative in routes:
    if chapter_id not in {"A", "B", "C"} and not (
            chapter_id.isdigit() and 1 <= int(chapter_id) <= 50):
        continue
    chapter = json.loads((ROOT / relative).read_text(encoding="utf-8"))
    for item in walk(chapter["blocks"]):
        if "kind" not in item:
            continue
        source_text = item.get("text", "") + " " + item.get("caption", "")
        for kind, pattern in mention_patterns.items():
            for match in pattern.finditer(source_text):
                reference_mentions += 1
                if match[1] not in reference_targets[kind]:
                    unresolved_mentions.add((kind, match[1], chapter_id,
                                             item.get("id", "")))
# The printed Chapter 43 text cites equation (16.5), but Chapter 16 has no
# equation (16.5); keeping it unlinked preserves the original discrepancy.
assert unresolved_mentions == {("formula", "16.5", "43", "p535-b017")}, (
    "Unexpected unresolved printed cross-references", sorted(unresolved_mentions))

internal_links = 0
for origin, href in hrefs:
    url = urlsplit(href)
    if not href.startswith(("?", "#")):
        continue
    query = parse_qs(url.query)
    if url.query and query.get("book") != [BOOK_ID]:
        continue
    target = query.get("chapter", [origin])[0]
    assert target in anchors, (origin, href, "unknown chapter")
    if url.fragment:
        assert url.fragment in anchors[target], (origin, href, "unknown anchor")
    internal_links += 1

manifest_assets = set(MANIFEST["assets"])
assert MANIFEST["bookId"] == BOOK_ID
assert len(manifest_assets) == len(MANIFEST["assets"])
assert images <= manifest_assets, sorted(images - manifest_assets)
assert all((ROOT / path).is_file() for path in manifest_assets)
assert MANIFEST["totalBytes"] == sum((ROOT / path).stat().st_size
                                      for path in manifest_assets)

print(json.dumps({"chapters": len(routes), "pages": len(pages),
                  "blocks": blocks_total, "toc": toc_total,
                  "internalLinks": internal_links,
                  "referenceTargets": sum(len(entries) for entries in reference_targets.values()),
                  "numberedMentions": reference_mentions,
                  "referencedImages": len(images),
                  "manifestImages": len(manifest_assets)},
                 ensure_ascii=False))
if ARGS.list_unreferenced:
    for path in sorted(manifest_assets - images):
        print(path)
