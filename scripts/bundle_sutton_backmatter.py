"""Build Sutton/Barto reference, index, and series-book reader data.

The page Markdown files are the editorial source. This script preserves their
physical-page order and never registers or approves content on its own.
"""

from __future__ import annotations

import argparse
import html
import json
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BOOK = ROOT / "books" / "sutton-barto-reinforcement-learning-2e"
BACK = BOOK / "backmatter"
BOOK_ID = BOOK.name
PAGE_OFFSET = 22
INDEX_ITEM = re.compile(r"^( *)(- )(.+)$")
INLINE = re.compile(r"\*\*([^*]+)\*\*|\*([^*]+)\*|\$([^$]+)\$|(?<![\w(])(\d+(?:[–-]\d+)?)(?![\w)])")


def pages(directory: str, first: int, last: int) -> list[tuple[int, str]]:
    results = []
    for physical in range(first, last + 1):
        path = BACK / directory / f"page-{physical}.md"
        if not path.is_file():
            raise ValueError(f"Missing source page: {path}")
        source = path.read_text(encoding="utf-8").strip()
        if not source:
            raise ValueError(f"Empty source page: {path}")
        results.append((physical, source))
    return results


def block(kind: str, page: int, sequence: int, **fields: object) -> dict:
    return {"kind": kind, "page": page, "id": f"p{page}-b{sequence:03d}", **fields}


def save(stem: str, title: str, toc: list[dict], blocks: list[dict]) -> None:
    if not blocks or not toc:
        raise ValueError(f"Empty backmatter: {stem}")
    output = BOOK / f"chapter-{stem}.json"
    output.write_text(json.dumps({"bookId": BOOK_ID, "title": title, "toc": toc, "blocks": blocks},
                                 ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(f"Wrote {output}: {len(blocks)} blocks, {len(toc)} TOC entries")


def references() -> None:
    blocks = []
    count = 0
    for physical, source in pages("references", 503, 540):
        printed = physical - PAGE_OFFSET
        for sequence, paragraph in enumerate(re.split(r"\n\s*\n", source), 1):
            paragraph = " ".join(paragraph.strip().splitlines())
            if physical == 503 and sequence == 1:
                if paragraph != "# 参考文献":
                    raise ValueError("Reference title differs from source convention")
                blocks.append(block("heading", printed, sequence, level=1, text="参考文献"))
            else:
                if not paragraph or paragraph.startswith("#"):
                    raise ValueError(f"Malformed reference entry on physical page {physical}")
                blocks.append(block("reference-entry", printed, sequence, text=paragraph))
                count += 1
    if count != 782:
        raise ValueError(f"Expected 782 reviewed references, found {count}")
    save("REF", "参考文献", [{"number": "", "title": "参考文献", "block": blocks[0]["id"], "level": 1}], blocks)


def page_map() -> dict[int, str]:
    mapping: dict[int, str] = {}
    for stem in ["01", "I", *[f"{n:02d}" for n in range(2, 9)], "II",
                 *[f"{n:02d}" for n in range(9, 14)], "III",
                 *[f"{n:02d}" for n in range(14, 18)]]:
        data = json.loads((BOOK / f"chapter-{stem}.json").read_text(encoding="utf-8"))
        for item in data["blocks"]:
            number = item.get("page")
            if isinstance(number, int):
                previous = mapping.setdefault(number, stem)
                if previous != stem:
                    raise ValueError(f"Printed page {number} belongs to both {previous} and {stem}")
    return mapping


def math_map(sources: list[str]) -> dict[str, str]:
    tex = list(dict.fromkeys(re.findall(r"\$([^$]+)\$", "\n".join(sources))))
    if not tex:
        return {}
    process = subprocess.run(["node", str(ROOT / "scripts" / "tex_to_mathml.js")],
                             input=json.dumps([{"tex": value, "display": False} for value in tex]),
                             text=True, encoding="utf-8", capture_output=True, check=True)
    rendered = json.loads(process.stdout)
    if len(rendered) != len(tex):
        raise ValueError("Index MathML conversion count mismatch")
    return dict(zip(tex, rendered, strict=True))


def index_html(value: str, mapping: dict[int, str], math: dict[str, str], missing: set[int]) -> str:
    def page_link(label: str) -> str:
        start = int(re.match(r"\d+", label).group())
        chapter = mapping.get(start)
        if chapter is None:
            missing.add(start)
            return html.escape(label)
        href = f"?book={BOOK_ID}&amp;chapter={chapter}&amp;page={start}"
        return f'<a href="{href}" title="跳转至原书第 {start} 页">{html.escape(label)}</a>'

    chunks = []
    cursor = 0
    first_comma = value.find(",")
    for match in INLINE.finditer(value):
        chunks.append(html.escape(value[cursor:match.start()]))
        strong, emph, tex, numeric = match.groups()
        if strong is not None:
            inner = page_link(strong) if strong[0].isdigit() and match.start() > first_comma else html.escape(strong)
            chunks.append(f"<strong>{inner}</strong>")
        elif emph is not None:
            inner = page_link(emph) if emph[0].isdigit() and match.start() > first_comma else html.escape(emph)
            chunks.append(f"<em>{inner}</em>")
        elif tex is not None:
            chunks.append(math[tex])
        elif numeric is not None:
            chunks.append(page_link(numeric) if match.start() > first_comma >= 0 else html.escape(numeric))
        cursor = match.end()
    chunks.append(html.escape(value[cursor:]))
    return "".join(chunks)


def index() -> None:
    sources = pages("index", 541, 546)
    mapping = page_map()
    math = math_map([source for _, source in sources])
    missing: set[int] = set()
    blocks = []
    entries = 0
    for physical, source in sources:
        printed = physical - PAGE_OFFSET
        sequence = 0
        for line in source.splitlines():
            if not line.strip():
                continue
            sequence += 1
            if line == "# 索引":
                blocks.append(block("heading", printed, sequence, level=1, text="索引"))
            elif line.startswith("> "):
                blocks.append(block("paragraph", printed, sequence, text=line[2:]))
            else:
                item = INDEX_ITEM.fullmatch(line)
                if item is None:
                    raise ValueError(f"Malformed index line on physical page {physical}: {line}")
                depth = len(item[1]) // 2
                if depth > 2 or len(item[1]) % 2:
                    raise ValueError(f"Unexpected index indentation: {line}")
                content = index_html(item[3], mapping, math, missing)
                html_line = f'<p class="index-entry sutton-index-level-{depth}">{content}</p>'
                blocks.append(block("rich", printed, sequence, html=html_line))
                entries += 1
    if entries != 529:
        raise ValueError(f"Expected 529 reviewed index entries, found {entries}")
    if missing:
        raise ValueError(f"Index references lack translated pages: {sorted(missing)}")
    save("IDX", "索引", [{"number": "", "title": "索引", "block": blocks[0]["id"], "level": 1}], blocks)


def series() -> None:
    blocks = []
    titles = 0
    for physical, source in pages("series", 547, 548):
        printed = physical - PAGE_OFFSET
        for sequence, paragraph in enumerate(re.split(r"\n\s*\n", source), 1):
            paragraph = " ".join(paragraph.strip().splitlines())
            if paragraph.startswith("# "):
                blocks.append(block("heading", printed, sequence, level=1, text=paragraph[2:]))
            elif paragraph.startswith("系列主编："):
                blocks.append(block("paragraph", printed, sequence, text=paragraph))
            else:
                segments: list[str | dict] = []
                cursor = 0
                for match in re.finditer(r"\*([^*]+)\*", paragraph):
                    if match.start() > cursor:
                        segments.append(paragraph[cursor:match.start()])
                    segments.append({"em": True, "text": match[1]})
                    cursor = match.end()
                if not segments or cursor >= len(paragraph):
                    raise ValueError(f"Series title or credit missing on physical page {physical}")
                segments.append(paragraph[cursor:])
                plain = "".join(part if isinstance(part, str) else part["text"] for part in segments)
                blocks.append(block("catalog-entry", printed, sequence, text=plain, segments=segments))
                titles += 1
    if titles != 24:
        raise ValueError(f"Expected 24 reviewed series titles, found {titles}")
    save("SERIES", "自适应计算与机器学习系列书目",
         [{"number": "", "title": "系列书目", "block": blocks[0]["id"], "level": 1}], blocks)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("section", choices=("references", "index", "series", "all"))
    selected = parser.parse_args().section
    tasks = {"references": references, "index": index, "series": series}
    for name, build in tasks.items():
        if selected in (name, "all"):
            build()


if __name__ == "__main__":
    main()
