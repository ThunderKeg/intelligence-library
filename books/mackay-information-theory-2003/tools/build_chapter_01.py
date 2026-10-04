"""Compile the checked, page-aligned MacKay chapter 1 drafts for the reader.

This only writes a draft JSON.  Registration in books.js follows independent
review of the translation and browser layout.
"""

import json
import re
import subprocess
from pathlib import Path
from xml.etree import ElementTree

import markdown
from bs4 import BeautifulSoup, Comment, Tag
from PIL import Image


BOOK = Path(__file__).resolve().parents[1]
ROOT = BOOK.parents[1]
SOURCE = BOOK / "translation" / "chapter-01"
OUTPUT = BOOK / "chapter-01.draft.json"
PDF_PAGES = range(15, 34)
DISPLAY = re.compile(r"(?<!\\)\$\$(.+?)(?<!\\)\$\$", re.DOTALL)
INLINE = re.compile(r"(?<!\\)\$(?!\$)(.+?)(?<!\\)\$", re.DOTALL)
MATH_TOKEN = re.compile(r"MACKAYMATH\d{6}")
FOOTNOTE_REF = re.compile(r"\[\^(\d+)-(\d+)\]")
INLINE_TOKEN = re.compile(r"MACKAYMATH\d{6}|\[\^\d+-\d+\]")
FOOTNOTE_DEF = re.compile(r"^\[\^(\d+)-(\d+)\]:\s*(.*)$", re.DOTALL)
NUMBER = re.compile(r"\\tag\{([^{}]+)\}")
NUMBERED_HEADING = re.compile(r"^(1(?:\.\d+)*)\s+(.+)$")
IMAGE = re.compile(r"^\.\./\.\./assets/chapter-01/([\w.-]+\.(?:png|jpg|svg|webp))$")


def protect_math(source: str):
    expressions = {}

    def replace(match, display):
        token = f"MACKAYMATH{len(expressions):06d}"
        expressions[token] = (match.group(1).strip(), display)
        return token

    source = DISPLAY.sub(lambda match: replace(match, True), source)
    source = INLINE.sub(lambda match: replace(match, False), source)
    return source, expressions


def plain(value: str, expressions: dict) -> str:
    value = MATH_TOKEN.sub(
        lambda match: ("$$" if expressions[match.group()][1] else "$")
        + expressions[match.group()][0]
        + ("$$" if expressions[match.group()][1] else "$"),
        value,
    )
    return FOOTNOTE_REF.sub(lambda match: match.group(2), value)


def segments(value: str, expressions: dict):
    pieces = []
    last = 0
    for match in INLINE_TOKEN.finditer(value):
        if match.start() > last:
            pieces.append(value[last : match.start()])
        if match.group().startswith("MACKAYMATH"):
            tex, display = expressions[match.group()]
            if display:
                raise ValueError("Display formula inside paragraph")
            pieces.append({"tex": tex, "text": tex})
        else:
            footnote = FOOTNOTE_REF.fullmatch(match.group())
            pieces.append({"footnote": True,
                           "href": f"#read-fn-{footnote.group(1)}-{footnote.group(2)}",
                           "text": footnote.group(2)})
        last = match.end()
    if last < len(value):
        pieces.append(value[last:])
    return pieces


def formatted_segments(nodes, expressions: dict):
    """Keep Markdown emphasis, code, and links alongside protected mathematics."""
    pieces = []

    def visit(node, emphasis=None):
        if isinstance(node, Comment):
            return
        if isinstance(node, str):
            for piece in segments(str(node), expressions):
                if isinstance(piece, str) and emphasis and piece:
                    pieces.append({emphasis: True, "text": piece})
                else:
                    pieces.append(piece)
            return
        if not isinstance(node, Tag):
            return
        if node.name == "br":
            if not str(node.next_sibling or "").startswith("\n"):
                pieces.append("\n")
        elif node.name == "code":
            pieces.append({"code": True, "text": node.get_text()})
        elif node.name == "a" and node.get("href"):
            pieces.append({"href": node["href"], "text": plain(node.get_text(), expressions)})
        else:
            next_emphasis = "strong" if node.name in ("strong", "b") else (
                "em" if node.name in ("em", "i") else emphasis
            )
            for child in node.contents:
                visit(child, next_emphasis)

    for node in nodes:
        visit(node)
    while pieces:
        first = pieces[0]
        if isinstance(first, str):
            trimmed = first.lstrip()
            if trimmed:
                pieces[0] = trimmed
                break
        elif "text" in first and "tex" not in first:
            trimmed = first["text"].lstrip()
            if trimmed:
                pieces[0] = {**first, "text": trimmed}
                break
        else:
            break
        pieces.pop(0)
    while pieces:
        last = pieces[-1]
        if isinstance(last, str):
            trimmed = last.rstrip()
            if trimmed:
                pieces[-1] = trimmed
                break
        elif "text" in last and "tex" not in last:
            trimmed = last["text"].rstrip()
            if trimmed:
                pieces[-1] = {**last, "text": trimmed}
                break
        else:
            break
        pieces.pop()
    return pieces


def without_prefix(pieces, length: int):
    """Remove an exercise label while retaining formatting in its body."""
    result = []
    for piece in pieces:
        visible = piece if isinstance(piece, str) else piece.get("text", "")
        if length >= len(visible):
            length -= len(visible)
            continue
        if length:
            if not isinstance(piece, str) and "tex" in piece:
                raise ValueError("Exercise label ends inside a formula")
            piece = visible[length:] if isinstance(piece, str) else {**piece, "text": visible[length:]}
            length = 0
        result.append(piece)
    if length:
        raise ValueError("Exercise label exceeds its paragraph")
    if result:
        first = result[0]
        if isinstance(first, str):
            result[0] = first.lstrip()
        elif "text" in first:
            result[0] = {**first, "text": first["text"].lstrip()}
    return result


def text_of(node: Tag) -> str:
    return node.get_text("", strip=False).strip()


def table_rows(table: Tag, expressions: dict):
    rows = []
    for row in table.find_all("tr"):
        cells = []
        for cell in row.find_all(["th", "td"], recursive=False):
            value = text_of(cell)
            cells.append({"text": plain(value, expressions),
                          "segments": formatted_segments([cell], expressions),
                          "header": cell.name == "th"})
        rows.append(cells)
    return rows


def list_items(node: Tag, expressions: dict):
    items = []
    for li in node.find_all("li", recursive=False):
        nested = li.find(["ul", "ol"], recursive=False)
        value = "".join(str(part) if isinstance(part, str) else part.get_text()
                        for part in li.contents if part is not nested).strip()
        item = {"text": plain(value, expressions),
                "segments": formatted_segments([part for part in li.contents if part is not nested], expressions)}
        if nested:
            item["children"] = list_items(nested, expressions)
            item["ordered"] = nested.name == "ol"
        items.append(item)
    return items


def image_path(source: str) -> str:
    match = IMAGE.fullmatch(source)
    if not match:
        raise ValueError(f"Unexpected figure path: {source}")
    path = BOOK / "assets" / "chapter-01" / match.group(1)
    if not path.is_file():
        raise ValueError(f"Missing figure: {path}")
    return f"assets/chapter-01/{match.group(1)}"


def image_dimensions(source: str) -> tuple[int, int]:
    path = BOOK / source
    if path.suffix.lower() == ".svg":
        root = ElementTree.parse(path).getroot()
        return int(root.attrib["width"]), int(root.attrib["height"])
    with Image.open(path) as image:
        return image.size


def compile_page(page: int, *, source: Path | None = None, image_resolver=None,
                 chapter_start: int = 15, chapter_number: int = 1):
    source = source or SOURCE / f"pdf-{page:03d}.md"
    image_resolver = image_resolver or image_path
    if not source.is_file():
        raise FileNotFoundError(source)
    raw = source.read_text(encoding="utf-8")
    if re.search(r"\b(?:TODO|TBD)\b|此处略|待补", raw, re.IGNORECASE):
        raise ValueError(f"Unfinished placeholder in {source}")
    protected, expressions = protect_math(raw)
    footnotes = []
    content_lines = []
    for line in protected.splitlines():
        note = FOOTNOTE_DEF.match(line)
        if note:
            footnotes.append((note.group(1), note.group(2), note.group(3)))
        else:
            content_lines.append(line)
    protected = "\n".join(content_lines)
    html = markdown.markdown(protected, extensions=["tables", "fenced_code", "sane_lists"], output_format="html5")
    soup = BeautifulSoup(html, "html.parser")
    nodes = []
    for node in soup.contents:
        if not isinstance(node, Tag):
            continue
        paragraphs = node.find_all("p", recursive=False) if node.name == "blockquote" else []
        if len(paragraphs) > 1:
            for paragraph in paragraphs:
                quote = soup.new_tag("blockquote")
                quote.append(paragraph.extract())
                nodes.append(quote)
        else:
            nodes.append(node)
    result = []
    index = 0
    while index < len(nodes):
        node = nodes[index]
        block = {"pdfPage": page, "page": page - chapter_start + 1}
        extra_caption = None
        if node.name in ("h1", "h2", "h3"):
            block.update(kind="heading", level=int(node.name[1]),
                         text=plain(text_of(node), expressions),
                         segments=formatted_segments([node], expressions))
        elif node.name == "blockquote":
            value = text_of(node)
            block.update(kind="intro" if value.startswith(("本章导读", "编者导读")) else "quote",
                         text=plain(value, expressions), segments=formatted_segments([node], expressions))
        elif node.name == "table":
            block.update(kind="table", rows=table_rows(node, expressions))
            if index + 1 < len(nodes) and nodes[index + 1].name == "p" and text_of(nodes[index + 1]).startswith((f"表 {chapter_number}.", f"算法 {chapter_number}.")):
                caption = text_of(nodes[index + 1])
                if caption.startswith("算法 1.16"):
                    block["notation"] = True
                extra_caption = {
                    "pdfPage": page, "page": page - chapter_start + 1,
                    "kind": "caption", "text": plain(caption, expressions),
                    "segments": formatted_segments([nodes[index + 1]], expressions),
                }
                index += 1
        elif node.name in ("ol", "ul"):
            block.update(kind="list", ordered=node.name == "ol", items=list_items(node, expressions))
        elif node.name == "pre":
            code = node.find("code")
            block.update(kind="code", text=code.get_text() if code else node.get_text())
        elif node.name == "p":
            value = text_of(node)
            if value in expressions and expressions[value][1]:
                tex = expressions[value][0]
                number = NUMBER.search(tex)
                block.update(kind="formula", tex=NUMBER.sub("", tex).strip(),
                             number=f"({number.group(1)})" if number else "",
                             text=plain(value, expressions))
            elif node.find("img") and len(node.find_all("img")) == 1 and not value:
                image = node.find("img")
                exercise = text_of(nodes[index + 1]) if index + 1 < len(nodes) and nodes[index + 1].name == "p" else ""
                label = re.match(rf"^(习题\s*{chapter_number}\.\d+)[。.]?(.*)$", exercise, re.DOTALL)
                icon_source = image.get("src", "")
                if icon_source.endswith(("exercise-rat.png", "exercise-icon.png")) and label:
                    body = label.group(2).strip()
                    icon_path = ("assets/shared/exercise-rat.png" if icon_source.endswith("exercise-rat.png")
                                 else image_resolver(icon_source))
                    block.update(kind="exercise", recommendedIcon=icon_path,
                                 label=label.group(1), text=plain(body, expressions),
                                 segments=without_prefix(
                                     formatted_segments([nodes[index + 1]], expressions), label.start(2)))
                    index += 1
                else:
                    figure_source = image_resolver(image.get("src", ""))
                    width, height = image_dimensions(figure_source)
                    block.update(kind="figure", src=figure_source, width=width, height=height,
                                 alt=image.get("alt", ""))
                    next_text = text_of(nodes[index + 1]) if index + 1 < len(nodes) and nodes[index + 1].name == "p" else ""
                    if next_text.startswith(f"图 {chapter_number}.") or (
                        figure_source.endswith("exercise-2-28-tree.png")
                        and next_text.startswith("习题 2.28 的分支示意")
                    ):
                        caption = text_of(nodes[index + 1])
                        block["caption"] = plain(caption, expressions)
                        block["captionSegments"] = formatted_segments([nodes[index + 1]], expressions)
                        index += 1
            else:
                rat = node.find("img")
                if rat:
                    icon_source = rat.get("src", "")
                    if not icon_source.endswith(("exercise-rat.png", "exercise-icon.png")):
                        raise ValueError(f"Unexpected inline image in {source}: {rat}")
                    rat.decompose()
                    value = text_of(node)
                    block["recommendedIcon"] = ("assets/shared/exercise-rat.png"
                                                if icon_source.endswith("exercise-rat.png")
                                                else image_resolver(icon_source))
                label = re.match(rf"^(▷\s*)?(习题\s*{chapter_number}\.\d+)[。.]?(.*)$", value, re.DOTALL)
                if label and not label.group(3).lstrip().startswith("的"):
                    body = label.group(3).strip()
                    mark = "▷ " if label.group(1) else ""
                    block.update(kind="exercise", label=mark + label.group(2),
                                 text=plain(body, expressions),
                                 segments=without_prefix(formatted_segments([node], expressions),
                                                         label.start(3)))
                else:
                    block.update(kind="paragraph", text=plain(value, expressions),
                                 segments=formatted_segments([node], expressions))
        else:
            raise ValueError(f"Unsupported {node.name} in {source}")
        block["id"] = f"p{page:03d}-b{len(result) + 1:03d}"
        result.append(block)
        if extra_caption:
            extra_caption["id"] = f"p{page:03d}-b{len(result) + 1:03d}"
            result.append(extra_caption)
        index += 1
    for chapter_id, note_number, body in footnotes:
        note_html = markdown.markdown(body, extensions=["tables", "fenced_code", "sane_lists"], output_format="html5")
        note_soup = BeautifulSoup(note_html, "html.parser")
        note_nodes = [node for node in note_soup.contents if isinstance(node, Tag)]
        if len(note_nodes) != 1 or note_nodes[0].name != "p":
            raise ValueError(f"Unsupported footnote {chapter_id}-{note_number} in {source}")
        note_node = note_nodes[0]
        result.append({
            "id": f"fn-{chapter_id}-{note_number}", "kind": "footnote",
            "pdfPage": page, "page": page - chapter_start + 1,
            "label": note_number,
            "text": plain(text_of(note_node), expressions),
            "segments": formatted_segments([note_node], expressions),
        })
    return result


def compile_math(blocks: list[dict]):
    targets = []
    payload = []
    for block in blocks:
        if block["kind"] == "formula":
            targets.append(block)
            payload.append({"tex": block["tex"], "display": True})
        for field in ("segments", "captionSegments"):
            for segment in block.get(field, []):
                if isinstance(segment, dict) and "tex" in segment:
                    targets.append(segment)
                    payload.append({"tex": segment["tex"], "display": False})
        for item in block.get("items", []):
            for segment in item.get("segments", []):
                if isinstance(segment, dict) and "tex" in segment:
                    targets.append(segment)
                    payload.append({"tex": segment["tex"], "display": False})
        for row in block.get("rows", []):
            for cell in row:
                for segment in cell["segments"]:
                    if isinstance(segment, dict) and "tex" in segment:
                        targets.append(segment)
                        payload.append({"tex": segment["tex"], "display": False})
    if not payload:
        return
    run = subprocess.run(["node", str(ROOT / "scripts" / "tex_to_mathml.js")],
                         input=json.dumps(payload, ensure_ascii=False), text=True,
                         encoding="utf-8", capture_output=True, check=False)
    if run.returncode:
        raise ValueError("KaTeX conversion failed:\n" + "\n".join(run.stderr.strip().splitlines()[-16:]))
    mathml = json.loads(run.stdout)
    if len(mathml) != len(targets):
        raise ValueError("MathML expression count mismatch")
    for target, markup in zip(targets, mathml):
        target["mathml"] = markup


def main():
    blocks = [block for page in PDF_PAGES for block in compile_page(page)]
    for block in blocks:
        if block["kind"] == "figure" and block["width"] >= 560:
            block["wide"] = True
    if not blocks or blocks[0]["kind"] != "heading":
        raise ValueError("Chapter heading missing")
    toc = []
    for block in blocks:
        if block["kind"] != "heading":
            continue
        match = NUMBERED_HEADING.match(block["text"])
        if block["level"] == 1:
            toc.append({"number": "1", "title": "信息论导论", "block": block["id"]})
        elif match and block["level"] == 2:
            toc.append({"number": match.group(1), "title": match.group(2), "block": block["id"]})
    if [entry["number"] for entry in toc] != ["1", "1.1", "1.2", "1.3", "1.4", "1.5", "1.6"]:
        raise ValueError(f"Unexpected chapter sections: {toc}")
    compile_math(blocks)
    chapter = {"schemaVersion": 2, "bookId": "mackay-information-theory-2003",
               "title": blocks[0]["text"], "sourcePdfPages": [15, 33],
               "toc": toc, "blocks": blocks}
    OUTPUT.write_text(json.dumps(chapter, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(f"Wrote {OUTPUT}: {len(blocks)} blocks, {len(toc)} sections")


if __name__ == "__main__":
    main()
