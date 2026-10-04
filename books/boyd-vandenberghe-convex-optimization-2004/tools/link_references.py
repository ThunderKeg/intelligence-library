"""Link actual, built reference targets in this book's own chapter JSON.

The shared reader does not traverse rich blocks when adding reference links.
This book-local pass preserves every visible character and every MathML node;
only verified targets among the explicitly selected units become links.
"""

from __future__ import annotations

import argparse
from copy import deepcopy
import json
import re
from urllib.parse import urlencode

from bs4 import BeautifulSoup, Comment, NavigableString

from common import BOOK, BOOK_ID, CHAPTERS, CHAPTER_BY_ID


NUMBER = r"(?:[A-C]|\d+)\.\d+(?:\.\d+)?"
REFERENCE_KEY = r"[^\W\d_][\w+\-]*"
RULES = (
    ("chapter", re.compile(r"第\s*(\d+)\s*章")),
    ("chapter", re.compile(r"附录\s*([A-C])(?![A-Za-z\d.])")),
    ("part", re.compile(r"第([一二三])部分")),
    ("section", re.compile(rf"(?:第\s*)?({NUMBER})\s*(?:小)?节")),
    ("section", re.compile(rf"§\s*({NUMBER})(?![\d.])")),
    ("figure", re.compile(rf"图\s*({NUMBER})(?![\d.])")),
    ("table", re.compile(rf"表\s*({NUMBER})(?![\d.])")),
    ("example", re.compile(rf"(?:示例|例)\s*({NUMBER})(?![\d.])")),
    ("exercise", re.compile(rf"习题\s*({NUMBER})(?![\d.])")),
    ("algorithm", re.compile(rf"算法\s*({NUMBER})(?![\d.])")),
    ("formula", re.compile(rf"(?:公式|式)?\s*[（(]\s*({NUMBER})\s*[）)]")),
)


def strip_generated(document: dict) -> dict:
    result = deepcopy(document)
    for block in result["blocks"]:
        if "data-convex-reference" not in block.get("html", ""):
            continue
        soup = BeautifulSoup(block["html"], "html.parser")
        for anchor in soup.select("a[data-convex-reference]"):
            anchor.unwrap()
        block["html"] = str(soup)
    return result


def collect_targets(documents: list[dict]) -> dict:
    targets: dict[str, dict[str, tuple[str, str]]] = {}

    def add(kind, key, chapter, block):
        previous = targets.setdefault(kind, {}).setdefault(key, (chapter, block))
        if previous != (chapter, block):
            raise ValueError(f"Duplicate {kind} target {key}: {previous}, {(chapter, block)}")

    for document in documents:
        chapter = document["chapterId"]
        first = document["blocks"][0]["id"]
        in_exercises = False
        if chapter.isdigit():
            add("chapter", str(int(chapter)), chapter, first)
        elif chapter in "ABC" and len(chapter) == 1:
            add("chapter", chapter, chapter, first)
        elif chapter in {"part-I": "一", "part-II": "二", "part-III": "三"}:
            add("part", {"part-I": "一", "part-II": "二", "part-III": "三"}[chapter], chapter, first)
        for block in document["blocks"]:
            identifier = block["id"]
            if block["kind"] == "heading":
                if block.get("level", 2) <= 2:
                    in_exercises = block["text"].strip() == "习题"
                match = re.match(rf"^({NUMBER})\s", block["text"])
                if match:
                    add("section", match[1], chapter, identifier)
                for kind, label in (("exercise", "习题"), ("example", "(?:示例|例)"), ("algorithm", "算法")):
                    match = re.match(rf"^{label}\s*({NUMBER})(?![\d.])", block["text"])
                    if match:
                        add(kind, match[1], chapter, identifier)
            if "html" not in block:
                continue
            soup = BeautifulSoup(block["html"], "html.parser")
            for equation in soup.select(".book-formula[id^='eq-']"):
                add("formula", equation["id"][3:].replace("-", "."), chapter, identifier)
            for figure in soup.find_all("figure"):
                number = figure.get("data-figure")
                if not number:
                    match = re.match(rf"图\s*({NUMBER})(?![\d.])", figure.find("figcaption").get_text(" ", strip=True)) if figure.find("figcaption") else None
                    number = match[1] if match else None
                if number:
                    add("figure", number, chapter, identifier)
            for node in soup.select("div.example, div.exercise, div.algorithm, p, caption"):
                if node.find_parent(["figure", "table"]):
                    continue
                text = node.get_text(" ", strip=True)
                # The original exercises start with a bold number, without an
                # added 'exercise' label. Restrict bare-number targets to this
                # section, so section 2.1 and exercise 2.1 stay distinct.
                first_child = next((child for child in node.children
                                    if str(child).strip()), None)
                if (in_exercises and getattr(first_child, "name", None) == "strong"
                        and (match := re.match(rf"^({NUMBER})(?![\d.])", first_child.get_text(" ", strip=True)))):
                    add("exercise", match[1], chapter, identifier)
                for kind, label in (("example", "(?:示例|例)"), ("exercise", "习题"), ("algorithm", "算法"), ("table", "表")):
                    # A prose paragraph can start with a reference, e.g.
                    # '习题 4.31 和 4.58 将给出具体例子。'. Only a styled
                    # title/caption or an explicit semantic container defines
                    # a target; ordinary leading references do not.
                    if node.name == "p" and getattr(first_child, "name", None) != "strong":
                        continue
                    match = re.match(rf"^{label}\s*({NUMBER})(?![\d.])", text)
                    if match:
                        add(kind, match[1], chapter, identifier)
                # Bibliography labels can contain inline typography, e.g.
                # [ABB<sup>+</sup>99]. Joining with spaces splits the key.
                if chapter == "references" and (match := re.match(
                        rf"^\[({REFERENCE_KEY})\]", node.get_text("", strip=True))):
                    add("reference", match[1], chapter, identifier)
    return targets


def linked_documents(documents: list[dict]) -> tuple[list[dict], dict]:
    clean = [strip_generated(document) for document in documents]
    targets = collect_targets(clean)
    results = deepcopy(clean)
    counts = {}
    for document, original in zip(results, clean):
        chapter = document["chapterId"]
        count = 0
        for block, original_block in zip(document["blocks"], original["blocks"]):
            if "html" not in block or block["kind"] in {"heading", "intro"}:
                continue
            soup = BeautifulSoup(block["html"], "html.parser")
            for node in list(soup.find_all(string=True)):
                if isinstance(node, Comment) or node.find_parent(["a", "math", "code", "pre", "script", "style"]):
                    continue
                candidates = []
                groups = list(re.finditer(r"\[[^\[\]\n]+\]", str(node)))
                citation_groups = []
                for group in groups:
                    first_key = re.match(rf"\[({REFERENCE_KEY})(?=\s*[,;，；\]])", group.group())
                    if first_key and any(char.isdigit() for char in first_key[1]):
                        citation_groups.append(group)
                # Part/chapter numbers in a bibliography title describe that
                # cited work, never this book (e.g. WSMP Part I and Part II).
                for kind, pattern in (() if chapter == "references" else RULES):
                    for match in pattern.finditer(str(node)):
                        # In [BTN01, §4.3], section 4.3 belongs to the cited
                        # work, not this book. The same applies to a Chinese
                        # chapter/section detail inside a citation group.
                        if any(group.start() <= match.start() < group.end()
                               for group in citation_groups):
                            continue
                        destination = targets.get(kind, {}).get(match[1])
                        if destination and destination != (chapter, block["id"]):
                            candidates.append((match.start(), match.end(), destination, kind))
                # Citation groups can contain several keys, accented author
                # initials, and page/volume details. Link only keys that exist
                # in the built bibliography, preserving all other characters.
                for group in groups:
                    for key in re.finditer(REFERENCE_KEY, group.group()):
                        destination = targets.get("reference", {}).get(key.group())
                        if destination and destination != (chapter, block["id"]):
                            candidates.append((group.start() + key.start(), group.start() + key.end(),
                                               destination, "reference"))
                if chapter == "contents" and node.find_parent("td"):
                    text = str(node)
                    match = re.match(rf"^({NUMBER})\s", text)
                    if match and (destination := targets.get("section", {}).get(match[1])):
                        candidates.append((0, len(text), destination, "section"))
                    elif (match := re.match(r"^([A-C]|\d+)\s", text)):
                        if destination := targets.get("chapter", {}).get(match[1]):
                            candidates.append((0, len(text), destination, "chapter"))
                if not candidates:
                    continue
                offset = 0
                for start, end, destination, kind in sorted(candidates, key=lambda item: (item[0], -item[1])):
                    if start < offset:
                        continue
                    if start > offset:
                        node.insert_before(NavigableString(str(node)[offset:start]))
                    target_chapter, target_block = destination
                    href = f"#read-{target_block}" if target_chapter == chapter else (
                        "?" + urlencode({"book": BOOK_ID, "chapter": target_chapter}) + f"#read-{target_block}")
                    anchor = soup.new_tag("a", href=href, attrs={"class": "reading-reference", "data-convex-reference": kind})
                    anchor.string = str(node)[start:end]
                    node.insert_before(anchor)
                    offset = end
                    count += 1
                if offset < len(str(node)):
                    node.insert_before(NavigableString(str(node)[offset:]))
                node.extract()
            block["html"] = str(soup)
            before = BeautifulSoup(original_block["html"], "html.parser")
            assert soup.get_text() == before.get_text(), (chapter, block["id"], "visible text changed")
            assert [str(x) for x in soup.find_all("math")] == [str(x) for x in before.find_all("math")]
        counts[chapter] = count
    return results, counts


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("chapters", nargs="*", help="Explicit completed/stable JSON units; default: existing outputs in book order")
    parser.add_argument("--check", action="store_true", help="Verify current generated links; do not write")
    args = parser.parse_args()
    selected = args.chapters or [chapter.id for chapter in CHAPTERS if (BOOK / f"chapter-{chapter.id}.json").exists()]
    if not selected or any(chapter not in CHAPTER_BY_ID for chapter in selected):
        parser.error("Select existing book units")
    paths = [BOOK / f"chapter-{chapter}.json" for chapter in selected]
    originals = [json.loads(path.read_text(encoding="utf-8")) for path in paths]
    documents, counts = linked_documents(originals)
    for path, old, document in zip(paths, originals, documents):
        if args.check:
            if old != document:
                raise SystemExit(f"Reference pass needs rebuilding: {path.name}")
        else:
            path.write_text(json.dumps(document, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")
    print(json.dumps({"linkedReferences": counts, "visibleTextAndMathPreserved": True}, ensure_ascii=False))


if __name__ == "__main__":
    main()
