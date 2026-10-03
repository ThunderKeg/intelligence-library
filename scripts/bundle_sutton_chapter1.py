"""Bundle the page-checked Chinese translation of Sutton and Barto, chapter 1."""

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BOOK = ROOT / "books" / "sutton-barto-reinforcement-learning-2e"
TRANSLATION = BOOK / "translation"
OUTPUT = BOOK / "chapter-01.json"
IMAGE = re.compile(r"^!\[([^]]*)\]\((assets/[\w./-]+)\)$")
HEADING = re.compile(r"^(#{1,3})\s+(.+)$")
EXERCISE = re.compile(r"^\*\*(习题\s+1\.\d+：[^*]+)\*\*\s*(.+)$", re.S)
BIBLIO_NOTE = re.compile(r"^\*\*(1\.\d+)\*\*\s*(.+)$", re.S)

UPDATE_MATHML = (
    '<math xmlns="http://www.w3.org/1998/Math/MathML" display="block">'
    '<mrow><mi>V</mi><mo>(</mo><msub><mi>S</mi><mi>t</mi></msub><mo>)</mo>'
    '<mo>←</mo><mi>V</mi><mo>(</mo><msub><mi>S</mi><mi>t</mi></msub><mo>)</mo>'
    '<mo>+</mo><mi>α</mi><mo>[</mo>'
    '<mi>V</mi><mo>(</mo><msub><mi>S</mi><mrow><mi>t</mi><mo>+</mo><mn>1</mn></mrow></msub><mo>)</mo>'
    '<mo>−</mo><mi>V</mi><mo>(</mo><msub><mi>S</mi><mi>t</mi></msub><mo>)</mo>'
    '<mo>]</mo></mrow></math>'
)


def chunks(path: Path) -> list[str]:
    if not path.exists():
        raise SystemExit(f"Missing translated page: {path}")
    result = re.split(r"\n\s*\n", path.read_text(encoding="utf-8").strip())
    if not result or not result[0].strip():
        raise SystemExit(f"Empty translated page: {path}")
    return [chunk.strip() for chunk in result]


blocks: list[dict] = []
counts = {}
for page in range(1, 23):
    for chunk in chunks(TRANSLATION / f"page-{page:02d}.md"):
        heading = HEADING.fullmatch(chunk)
        image = IMAGE.fullmatch(chunk)
        exercise = EXERCISE.fullmatch(chunk)
        biblio_note = BIBLIO_NOTE.fullmatch(chunk)
        if heading:
            block = {"kind": "heading", "text": heading[2], "level": len(heading[1])}
        elif chunk.startswith("> 导读："):
            block = {"kind": "intro", "text": chunk[2:]}
        elif chunk.startswith("> "):
            block = {"kind": "quote", "text": chunk[2:].replace("\n", " ")}
        elif exercise:
            block = {"kind": "exercise", "label": exercise[1], "text": exercise[2].replace("\n", " ")}
        elif biblio_note:
            block = {"kind": "bibliographical-note", "label": biblio_note[1], "text": biblio_note[2].replace("\n", " ")}
        elif image:
            block = {"kind": "figure", "alt": image[1], "src": image[2]}
        elif chunk.startswith("图 1.1："):
            if not blocks or blocks[-1]["kind"] != "figure":
                raise SystemExit("Figure 1.1 caption must follow its image")
            blocks[-1]["caption"] = chunk
            continue
        elif chunk.startswith("图内文字译注："):
            if not blocks or blocks[-1]["kind"] != "figure":
                raise SystemExit("Figure annotations must follow a figure")
            blocks[-1]["annotations"] = [part.strip() for part in chunk.removeprefix("图内文字译注：").split("；") if part.strip()]
            continue
        elif chunk.startswith("公式："):
            expression = chunk.removeprefix("公式：").strip().rstrip("。")
            if expression != "V(Sₜ) ← V(Sₜ) + α[V(Sₜ₊₁) − V(Sₜ)]":
                raise SystemExit(f"Unreviewed formula on page {page}: {expression}")
            block = {"kind": "formula", "text": expression, "mathml": UPDATE_MATHML}
        elif chunk.startswith("- "):
            item = chunk[2:].replace("\n", " ")
            if blocks and blocks[-1]["kind"] == "list":
                blocks[-1]["items"].append(item)
                continue
            block = {"kind": "list", "items": [item], "ordered": False}
        else:
            block = {"kind": "paragraph", "text": chunk.replace("**", "").replace("\n", " ")}
        counts[page] = counts.get(page, 0) + 1
        block["id"] = f"p{page:02d}-t{counts[page]:02d}"
        block["page"] = page
        blocks.append(block)

headings = [block for block in blocks if block["kind"] == "heading"]
toc = []
for number in ["1", *(f"1.{i}" for i in range(1, 8))]:
    prefix = "第 1 章 " if number == "1" else number + " "
    found = [block for block in headings if block["text"].startswith(prefix)]
    if len(found) != 1:
        raise SystemExit(f"Expected one heading for {number}, got {len(found)}")
    heading = found[0]
    toc.append({"number": number, "title": heading["text"].removeprefix(prefix), "block": heading["id"]})

if sum(1 for block in blocks if block["kind"] == "figure") != 2:
    raise SystemExit("Chapter 1 must have the board and Figure 1.1")
if sum(1 for block in blocks if block["kind"] == "formula") != 1:
    raise SystemExit("Chapter 1 must have the temporal-difference update formula")

chapter = {"bookId": "sutton-barto-reinforcement-learning-2e", "title": "第 1 章 绪论", "toc": toc, "blocks": blocks}
OUTPUT.write_text(json.dumps(chapter, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
print(f"Wrote {OUTPUT}: 22 translated pages, {len(blocks)} blocks, {len(toc)} TOC entries")
