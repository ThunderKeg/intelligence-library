"""Bundle the page-checked chapter 2 translation without losing source structure."""

import json
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BOOK = ROOT / "books" / "sutton-barto-reinforcement-learning-2e"
SOURCE = BOOK / "translation" / "chapter-02"
OUTPUT = BOOK / "chapter-02.json"
HEADING = re.compile(r"^(#{1,3})\s+(.+)$")
IMAGE = re.compile(r"^!\[([^]]*)\]\((assets/[\w./-]+)\)$")
FORMULA = re.compile(r"^公式(?:（(2\.\d+)）)?：(.+)$", re.S)
EXERCISE = re.compile(r"^\*\*(习题\s+2\.\d+[^*]*?)\*\*(.*)$", re.S)
BIBLIO = re.compile(r"^\*\*(2\.[\d–-]+)\*\*\s*(.+)$", re.S)
EMPHASIS = re.compile(r"\*([A-Za-z]+)\*")

# Exact, reviewed equation displays. The source transcription remains in `text`
# for accessibility and comparison against the PDF.
FORMULA_TEX = {
    "2.1": r"Q_t(a)\doteq\frac{\text{在 }t\text{ 前选择 }a\text{ 所得奖励总和}}{\text{在 }t\text{ 前选择 }a\text{ 的次数}}=\frac{\sum_{i=1}^{t-1}R_i\,\mathbb{1}_{A_i=a}}{\sum_{i=1}^{t-1}\mathbb{1}_{A_i=a}}",
    "2.2": r"A_t\doteq\operatorname*{arg\,max}_a Q_t(a)",
    "2.3": r"=Q_n+\frac{1}{n}(R_n-Q_n)",
    "2.4": r"\text{NewEstimate}\leftarrow\text{OldEstimate}+\text{StepSize}[\text{Target}-\text{OldEstimate}]",
    "2.5": r"Q_{n+1}\doteq Q_n+\alpha(R_n-Q_n)",
    "2.6": r"=(1-\alpha)^nQ_1+\sum_{i=1}^{n}\alpha(1-\alpha)^{n-i}R_i",
    "2.7": r"\sum_{n=1}^{\infty}\alpha_n(a)=\infty,\qquad \sum_{n=1}^{\infty}\alpha_n^2(a)<\infty",
    "2.8": r"\beta_n\doteq\frac{\alpha}{\bar o_n}",
    "2.9": r"\bar o_n\doteq\bar o_{n-1}+\alpha(1-\bar o_{n-1}),\ n>0,\quad \bar o_0\doteq0",
    "2.10": r"A_t\doteq\operatorname*{arg\,max}_a\left[Q_t(a)+c\sqrt{\frac{\ln t}{N_t(a)}}\right]",
    "2.11": r"\Pr\{A_t=a\}\doteq\frac{e^{H_t(a)}}{\sum_{b=1}^{k}e^{H_t(b)}}\doteq\pi_t(a)",
    "2.12": r"\begin{aligned}H_{t+1}(A_t)&\doteq H_t(A_t)+\alpha(R_t-\bar R_t)[1-\pi_t(A_t)]\\ H_{t+1}(a)&\doteq H_t(a)-\alpha(R_t-\bar R_t)\pi_t(a),\quad a\ne A_t\end{aligned}",
    "2.13": r"H_{t+1}(a)\doteq H_t(a)+\alpha\frac{\partial\mathbb E[R_t]}{\partial H_t(a)}",
}


def inline(text: str) -> tuple[str, list | None]:
    """Translate simple source Markdown italics to safe reader segments."""
    segments = []
    position = 0
    for match in EMPHASIS.finditer(text):
        if match.start() > position:
            segments.append(text[position:match.start()])
        segments.append({"em": True, "text": match[1]})
        position = match.end()
    if not segments:
        return text, None
    if position < len(text):
        segments.append(text[position:])
    return EMPHASIS.sub(lambda match: match[1], text), segments


blocks = []
counts = {}
for page in range(25, 47):
    path = SOURCE / f"page-{page:02d}.md"
    if not path.exists():
        raise SystemExit(f"Missing translated page: {path}")
    source = path.read_text(encoding="utf-8").strip()
    if page == 46:
        if "为空白页" not in source:
            raise SystemExit("Source page 46 should be confirmed blank")
        continue
    if not source:
        raise SystemExit(f"Empty translated page {page}")
    for chunk in [part.strip() for part in re.split(r"\n\s*\n", source) if part.strip()]:
        heading = HEADING.fullmatch(chunk)
        image = IMAGE.fullmatch(chunk)
        formula = FORMULA.fullmatch(chunk)
        exercise = EXERCISE.fullmatch(chunk)
        biblio = BIBLIO.fullmatch(chunk)
        if heading:
            value, segments = inline(heading[2])
            block = {"kind": "heading", "text": value, "level": len(heading[1])}
        elif chunk.startswith("> 导读："):
            value, segments = inline(chunk[2:].replace("\n", " "))
            block = {"kind": "intro", "text": value}
        elif image:
            block = {"kind": "figure", "alt": image[1], "src": image[2], "wide": True}
            segments = None
        elif re.match(r"^图 2\.\d+：", chunk):
            if not blocks or blocks[-1]["kind"] != "figure":
                raise SystemExit(f"Figure caption without adjacent image on page {page}")
            value, segments = inline(chunk)
            blocks[-1]["caption"] = value
            if segments:
                blocks[-1]["captionSegments"] = segments
            continue
        elif chunk.startswith("图内文字译注："):
            if not blocks or blocks[-1]["kind"] != "figure":
                raise SystemExit(f"Figure annotation without adjacent image on page {page}")
            blocks[-1]["annotations"] = [item.strip() for item in chunk.removeprefix("图内文字译注：").split("；") if item.strip()]
            continue
        elif formula:
            value, segments = inline(formula[2].strip().rstrip("。"))
            block = {"kind": "formula", "text": value}
            if formula[1]:
                block["number"] = formula[1]
        elif chunk.startswith("```text\n") and chunk.endswith("\n```"):
            block = {"kind": "code", "language": "text", "text": chunk[8:-4]}
            segments = None
        elif exercise:
            value, segments = inline(exercise[2].replace("\n", " ").strip())
            block = {"kind": "exercise", "label": exercise[1], "text": value}
        elif biblio:
            value, segments = inline(biblio[2].replace("\n", " "))
            block = {"kind": "bibliographical-note", "label": biblio[1], "text": value}
        elif chunk.startswith("脚注 "):
            label, value = chunk.split("：", 1)
            value, segments = inline(value.strip())
            block = {"kind": "footnote", "label": label, "text": value}
        elif chunk.startswith("**") and chunk.endswith("**"):
            block = {"kind": "heading", "text": chunk.strip("*"), "level": 3}
            segments = None
        else:
            value, segments = inline(chunk.replace("\n", " "))
            block = {"kind": "paragraph", "text": value}
        counts[page] = counts.get(page, 0) + 1
        block["id"] = f"p{page:02d}-t{counts[page]:02d}"
        block["page"] = page
        if segments and block["kind"] in {"paragraph", "intro", "exercise", "bibliographical-note", "footnote"}:
            block["segments"] = segments
        blocks.append(block)

# The original visually separates this three-page derivation in a shaded box.
box_start = next(index for index, block in enumerate(blocks) if block["kind"] == "heading" and block["text"] == "赌博机梯度算法作为随机梯度上升")
box_end = max(index for index, block in enumerate(blocks) if block["page"] == 40)
if blocks[box_start]["page"] != 38 or blocks[box_end]["page"] != 40:
    raise SystemExit("Gradient derivation box should span source pages 38–40")
boxed = {"kind": "box", "id": "p38-gradient-box", "page": 38, "blocks": blocks[box_start:box_end + 1]}
blocks[box_start:box_end + 1] = [boxed]

all_blocks = [nested for block in blocks for nested in (block["blocks"] if block["kind"] == "box" else [block])]
heading_blocks = [block for block in all_blocks if block["kind"] == "heading"]
toc = []
for number in ["2", *(f"2.{index}" for index in range(1, 11))]:
    prefix = "第 2 章 " if number == "2" else number + " "
    matches = [block for block in heading_blocks if block["text"].startswith(prefix)]
    if len(matches) != 1:
        raise SystemExit(f"Expected one heading {number}, got {len(matches)}")
    toc.append({"number": number, "title": matches[0]["text"].removeprefix(prefix), "block": matches[0]["id"]})

def require(kind: str, expected: int) -> None:
    actual = sum(block["kind"] == kind for block in all_blocks)
    if actual != expected:
        raise SystemExit(f"Expected {expected} {kind} blocks, got {actual}")


require("figure", 6)
require("exercise", 11)
require("code", 1)
require("footnote", 1)
if sorted((block["number"] for block in all_blocks if block["kind"] == "formula" and "number" in block), key=lambda item: int(item.split(".")[1])) != [f"2.{index}" for index in range(1, 14)]:
    raise SystemExit("Chapter 2 numbered equations should be 2.1–2.13")

numbered = [block for block in all_blocks if block["kind"] == "formula" and "number" in block]
converted = subprocess.run(
    ["node", str(ROOT / "scripts" / "tex_to_mathml.js")],
    input=json.dumps([{"tex": FORMULA_TEX[block["number"]], "display": True} for block in numbered]),
    text=True,
    encoding="utf-8",
    capture_output=True,
    check=True,
)
for block, mathml in zip(numbered, json.loads(converted.stdout), strict=True):
    block["mathml"] = mathml

chapter = {"bookId": "sutton-barto-reinforcement-learning-2e", "title": "第 2 章 多臂赌博机", "toc": toc, "blocks": blocks, "emptySourcePages": [46]}
OUTPUT.write_text(json.dumps(chapter, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
print(f"Wrote {OUTPUT}: {len(all_blocks)} source blocks, {len(toc)} TOC entries")
