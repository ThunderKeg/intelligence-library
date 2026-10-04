"""Build the page-checked, unpublished MacKay index reader draft.

The nine Markdown sources follow the three printed columns in their original
order.  Printed Arabic page numbers link to the first reading block on the
corresponding physical PDF page (printed page + 12).  The three Roman front
matter references retain their printed labels.
"""

from __future__ import annotations

import html
import json
import re
import subprocess
from dataclasses import dataclass, field
from pathlib import Path

import markdown
from bs4 import BeautifulSoup


BOOK = Path(__file__).resolve().parents[1]
ROOT = BOOK.parents[1]
SOURCE = BOOK / "translation" / "index"
OUTPUT = BOOK / "chapter-IDX.draft.json"
BOOK_ID = "mackay-information-theory-2003"
PAGES = range(632, 641)
BULLET = re.compile(r"^( *)(- )(.+)$")
COLUMN = re.compile(r"^<!-- (左|中|右)栏(?:续 (.*?))? -->$")
MATH = re.compile(r"\$([^$]+)\$")
TARGET = re.compile(r"([^、及或和→]+?)（[^）]*）")
PAGE_REF = re.compile(r"(?P<strong>\*\*)?(?P<first>\d+|xii|xi|v)(?(strong)\*\*)(?:[–-](?P<last>\d+))?$", re.I)
CHAPTER_ROW = re.compile(
    r'\{\s*id:\s*"([\w-]+)"[^{}]*?content:\s*"'
    r'(books/mackay-information-theory-2003/chapter-[\w-]+\.json)"\s*\}'
)
ALIASES = {
    "source code (for data compression)": "source code",
    "linear code": "linear block code",
    "profile": "profile, of random graph",
    "Gaussian": "Gaussian distribution",
    "Lempel–Ziv": "Lempel–Ziv coding",
    "wife-beaters": "wife-beater",
    "Student-t": "Student-t distribution",
}


@dataclass
class Entry:
    pdf_page: int
    line: int
    column: str
    depth: int
    term: str
    body: str
    has_colon: bool
    anchor: str
    parent: str = ""
    block_id: str = ""
    targets: list[str] = field(default_factory=list)


@dataclass
class Group:
    pdf_page: int
    column: str
    entries: list[Entry]
    continuation: str = ""
    block_id: str = ""


def normalized(term: str) -> str:
    """Use the original English spelling, ignoring Markdown visual markup."""
    if term.endswith("）") and "（" in term:
        term = term.rsplit("（", 1)[0]
    term = re.sub(r"[`*$]", "", term)
    term = re.sub(r"\\(?:mathrm|mathbf|mathit)\{([^{}]+)\}", r"\1", term)
    term = re.sub(r"\s+", " ", term).strip()
    return ALIASES.get(term, term)


def read_sources() -> list[Group]:
    groups: list[Group] = []
    heading_seen = False
    for pdf_page in PAGES:
        path = SOURCE / f"pdf-{pdf_page}.md"
        if not path.is_file():
            raise FileNotFoundError(path)
        text = path.read_text(encoding="utf-8")
        column = ""
        continuation = ""
        current: Group | None = None
        ordinal = 0
        for line_no, line in enumerate(text.splitlines(), 1):
            line = line.rstrip()
            if not line:
                continue
            if line == "# 索引（Index）" and pdf_page == 632 and not heading_seen:
                heading_seen = True
                continue
            match = COLUMN.fullmatch(line)
            if match:
                column, continuation = match.groups()
                continuation = continuation or ""
                if continuation and current is not None:
                    parent = current.continuation or current.entries[0].term
                    if normalized(continuation) != normalized(parent):
                        raise ValueError(f"Wrong same-page column continuation {path.name}:{line_no}")
                    # The prior headword's group already receives these children.
                    continuation = ""
                continue
            if line.startswith("<!--") and line.endswith("-->"):
                continue
            match = BULLET.fullmatch(line)
            if not match or not column:
                raise ValueError(f"Unexpected index line {path.name}:{line_no}: {line}")
            indent, _, content = match.groups()
            if len(indent) not in (0, 2, 4):
                raise ValueError(f"Invalid index depth {path.name}:{line_no}")
            depth = len(indent) // 2
            term, sep, body = content.partition("：")
            if not term.strip():
                raise ValueError(f"Empty index term {path.name}:{line_no}")
            ordinal += 1
            entry = Entry(pdf_page, line_no, column, depth, term, body, bool(sep),
                          f"idx-p{pdf_page}-e{ordinal:03d}")
            if depth == 0:
                current = Group(pdf_page, column, [], continuation)
                groups.append(current)
                continuation = ""
            elif current is None:
                if not continuation:
                    raise ValueError(f"Orphan subentry {path.name}:{line_no}")
                current = Group(pdf_page, column, [], continuation)
                groups.append(current)
                continuation = ""
            if current is None:
                raise AssertionError("Unreachable empty group")
            current.entries.append(entry)
        if not column:
            raise ValueError(f"No original columns recorded in {path.name}")
    if not heading_seen:
        raise ValueError("Missing printed Index heading")
    if normalized(groups[0].entries[0].term) != "Γ":
        raise ValueError("First printed index term changed")
    if normalized(groups[-1].entries[-1].term) != "Zipf, George K.":
        raise ValueError("Last printed index term changed")
    return groups


def assign_ids(groups: list[Group]) -> tuple[dict[str, Entry], dict[tuple[str, str], Entry]]:
    main: dict[str, Entry] = {}
    child: dict[tuple[str, str], Entry] = {}
    group_count: dict[int, int] = {632: 1}
    previous_parent = ""
    for group in groups:
        page = group.pdf_page
        group_count[page] = group_count.get(page, 0) + 1
        group.block_id = f"p{page}-b{group_count[page]:03d}"
        parent = normalized(group.continuation) if group.continuation else previous_parent
        for entry in group.entries:
            entry.block_id = group.block_id
            key = normalized(entry.term)
            if entry.depth == 0:
                parent = key
                if key in main:
                    raise ValueError(f"Duplicate main index term: {key}")
                main[key] = entry
            elif entry.depth == 1:
                if not parent:
                    raise ValueError(f"Subentry lacks parent: {entry.anchor}")
                entry.parent = parent
                child[(parent, key)] = entry
            else:
                if not parent:
                    raise ValueError(f"Third-level index entry lacks parent: {entry.anchor}")
                entry.parent = parent
            previous_parent = parent
    return main, child


def reading_targets() -> dict[int, tuple[str, str]]:
    source = (ROOT / "books.js").read_text(encoding="utf-8")
    marker = f'id: "{BOOK_ID}"'
    if source.count(marker) != 1:
        raise ValueError("Cannot locate unique MacKay book in books.js")
    section = source.split(marker, 1)[1].split('\n  {\n    id: "', 1)[0]
    chapters = CHAPTER_ROW.findall(section)
    if not chapters:
        raise ValueError("No formally registered MacKay chapters found")
    mapping: dict[int, tuple[str, str]] = {}
    for chapter_id, relative in chapters:
        path = ROOT / relative
        if not path.is_file():
            raise FileNotFoundError(path)
        chapter = json.loads(path.read_text(encoding="utf-8"))
        if chapter.get("bookId") != BOOK_ID:
            raise ValueError(f"Wrong book in {relative}")
        for block in chapter.get("blocks", []):
            page = block.get("pdfPage")
            if isinstance(page, int) and page not in mapping:
                mapping[page] = (chapter_id, block["id"])
            elif isinstance(page, int) and mapping[page][0] != chapter_id:
                raise ValueError(f"Physical PDF {page} appears in two registered units")
    return mapping


def convert_math(groups: list[Group]) -> dict[str, str]:
    expressions = sorted({tex for group in groups for entry in group.entries
                          for value in (entry.term, entry.body)
                          for tex in MATH.findall(value)})
    if not expressions:
        return {}
    payload = [{"tex": tex, "display": False} for tex in expressions]
    run = subprocess.run(["node", str(ROOT / "scripts" / "tex_to_mathml.js")],
                         input=json.dumps(payload), text=True, capture_output=True, check=True)
    results = json.loads(run.stdout)
    if len(results) != len(expressions) or any("merror" in item for item in results):
        raise ValueError("MathML conversion incomplete")
    return dict(zip(expressions, results))


def inline(source: str, mathml: dict[str, str]) -> str:
    tokens: dict[str, str] = {}

    def preserve(match: re.Match[str]) -> str:
        tex = match.group(1)
        token = f"MACKAYINDEXMATH{len(tokens):06d}"
        tokens[token] = f'<span class="inline-math">{mathml[tex]}</span>'
        return token

    protected = MATH.sub(preserve, source)
    markup = markdown.markdown(protected, output_format="html5")
    if not (markup.startswith("<p>") and markup.endswith("</p>")):
        raise ValueError(f"Unexpected inline Markdown: {source}")
    markup = markup[3:-4]
    for token, rendered in tokens.items():
        markup = markup.replace(token, rendered)
    return markup


def page_link(label: str, mapping: dict[int, tuple[str, str]]) -> str:
    match = PAGE_REF.fullmatch(label)
    if not match:
        raise ValueError(f"Unrecognized printed page reference: {label}")
    first = match.group("first")
    physical = {"v": 5, "xi": 11, "xii": 12}.get(first.lower())
    if physical is None:
        number = int(first)
        if not 1 <= number <= 612:
            raise ValueError(f"Printed page outside translated book: {label}")
        physical = number + 12
    if physical not in mapping:
        raise ValueError(f"Printed page {label} has no registered reading block")
    chapter_id, block_id = mapping[physical]
    url = f"?book={BOOK_ID}&chapter={chapter_id}#read-{block_id}"
    visible = html.escape(first + ("–" + match.group("last") if match.group("last") else ""))
    if match.group("strong"):
        visible = f"<strong>{visible}</strong>"
    return (f'<a class="reading-reference" href="{html.escape(url, quote=True)}" '
            f'title="原书印刷页 {html.escape(label.strip("*"), quote=True)}">{visible}</a>')


def resolve_target(key: str, previous: str, main: dict[str, Entry],
                   child: dict[tuple[str, str], Entry]) -> Entry:
    key = normalized(key)
    if previous and (previous, key) in child:
        return child[(previous, key)]
    if ", " in key:
        parent, subterm = key.split(", ", 1)
        if (parent, subterm) in child:
            return child[(parent, subterm)]
    if key not in main:
        raise ValueError(f"Unresolved printed see target: {key}")
    return main[key]


def see_links(source: str, mathml: dict[str, str], main: dict[str, Entry],
              child: dict[tuple[str, str], Entry]) -> tuple[str, list[str]]:
    result: list[str] = []
    targets: list[str] = []
    previous = ""
    position = 0
    for match in TARGET.finditer(source):
        result.append(inline(source[position:match.start()], mathml) if match.start() > position else "")
        english = match.group(1).strip()
        item = resolve_target(english, previous, main, child)
        href = f"#read-{item.block_id}" if item.depth == 0 else f"#{item.anchor}"
        result.append(f'<a class="reading-reference" href="{href}">{inline(match.group(), mathml)}</a>')
        targets.append(item.anchor)
        previous = normalized(english)
        position = match.end()
    tail = source[position:]
    if tail:
        # The printed source-code cross-reference ends with bare Lempel–Ziv.
        if tail.strip(" 、及或和") == "Lempel–Ziv":
            item = resolve_target("Lempel–Ziv", previous, main, child)
            prefix = tail[:tail.index("Lempel–Ziv")]
            result.append(inline(prefix, mathml))
            result.append(f'<a class="reading-reference" href="#read-{item.block_id}">Lempel–Ziv</a>')
            targets.append(item.anchor)
        else:
            result.append(inline(tail, mathml))
    if not targets:
        raise ValueError(f"No see targets found in {source}")
    return "".join(result), targets


def render_entry(entry: Entry, mathml: dict[str, str], mapping: dict[int, tuple[str, str]],
                 main: dict[str, Entry], child: dict[tuple[str, str], Entry]) -> str:
    body = entry.body
    if "见" in body:
        before, seen = body.split("见", 1)
        punctuation = before[-1] if before.endswith(("；", "，")) else ""
        before = before[:-1] if punctuation else before
    else:
        before, seen, punctuation = body, "", ""
    references = []
    if before:
        for item in before.split(", "):
            references.append(page_link(item, mapping))
    content = inline(entry.term, mathml) + ("：" if entry.has_colon else "")
    content += ", ".join(references)
    if seen:
        linked, entry.targets = see_links(seen.strip(), mathml, main, child)
        content += punctuation + "<em>见</em> " + linked
    elif punctuation:
        raise ValueError(f"Dangling see punctuation: {entry.anchor}")
    class_name = "index-entry" if entry.depth == 0 else "index-subentry"
    style = ' style="padding-left:3.2em"' if entry.depth == 2 else ""
    return f'<p id="{entry.anchor}" class="{class_name}"{style}>{content}</p>'


def main() -> None:
    groups = read_sources()
    main_terms, child_terms = assign_ids(groups)
    mathml = convert_math(groups)
    mapping = reading_targets()
    blocks = [{"pdfPage": 632, "page": 1, "kind": "heading", "level": 1,
               "text": "索引", "segments": ["索引"], "id": "p632-b001",
               "html": '<h1 style="text-align:center;border-top:3px solid currentColor;'
                       'padding-top:.45em;font-style:italic;font-weight:normal">索引</h1>'}]
    see_count = 0
    reference_count = 0
    for group in groups:
        content = "".join(render_entry(entry, mathml, mapping, main_terms, child_terms)
                          for entry in group.entries)
        for entry in group.entries:
            see_count += len(entry.targets)
            before = entry.body.split("见", 1)[0].rstrip("；，")
            reference_count += len(before.split(", ")) if before else 0
        block = {"pdfPage": group.pdf_page, "page": group.pdf_page - 631,
                 "kind": "rich", "id": group.block_id,
                 "text": BeautifulSoup(content, "html.parser").get_text(" ", strip=True),
                 "html": content,
                 "indexColumns": list(dict.fromkeys(entry.column for entry in group.entries)),
                 "indexEntryCount": len(group.entries)}
        if group.continuation:
            block["continuationOf"] = normalized(group.continuation)
        blocks.append(block)
    chapter = {"schemaVersion": 2, "bookId": BOOK_ID, "title": "索引",
               "sourcePdfPages": [632, 640],
               "toc": [{"number": "", "title": "索引", "block": "p632-b001"}],
               "blocks": blocks}
    if len({block["id"] for block in blocks}) != len(blocks):
        raise ValueError("Duplicate reading block ID")
    if [block["pdfPage"] for block in blocks] != sorted(block["pdfPage"] for block in blocks):
        raise ValueError("Index pages not in source order")
    if any("MACKAYINDEXMATH" in block.get("html", "") for block in blocks):
        raise ValueError("Unexpanded index math token")
    OUTPUT.write_text(json.dumps(chapter, ensure_ascii=False, separators=(",", ":")),
                      encoding="utf-8")
    print(f"Wrote {OUTPUT}: {len(blocks)} reading blocks, "
          f"{sum(len(group.entries) for group in groups)} source entries, "
          f"{reference_count} page references, {see_count} see links")


if __name__ == "__main__":
    main()
