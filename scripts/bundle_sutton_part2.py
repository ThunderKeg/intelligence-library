"""Bundle the independently checked second-part introduction."""

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BOOK = ROOT / "books" / "sutton-barto-reinforcement-learning-2e"
source = (BOOK / "parts" / "part-02.md").read_text(encoding="utf-8")
chunks = [value.strip() for value in re.split(r"\n\s*\n", source) if value.strip() and not value.strip().startswith("<!--")]
if len(chunks) != 5 or not chunks[0].startswith("# "):
    raise SystemExit(f"Expected a heading and four source paragraphs, got {len(chunks)}")
blocks = []
for index, value in enumerate(chunks, 1):
    block = {"id": f"p195-t{index:02d}", "kind": "heading" if index == 1 else "paragraph", "text": value.removeprefix("# "), "page": 195}
    if index == 1:
        block["level"] = 1
    blocks.append(block)
chapter = {
    "bookId": BOOK.name,
    "title": "第二部分 近似求解方法",
    "toc": [{"number": "II", "title": "近似求解方法", "block": blocks[0]["id"]}],
    "blocks": blocks,
}
output = BOOK / "chapter-II.json"
output.write_text(json.dumps(chapter, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
print(f"Wrote {output}: {len(blocks)} blocks")
