"""Bundle the first part introduction after checking its source pages."""

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BOOK = ROOT / "books" / "sutton-barto-reinforcement-learning-2e"
source = (BOOK / "parts" / "part-01.md").read_text(encoding="utf-8")
chunks = [value.strip() for value in re.split(r"\n\s*\n", source) if value.strip()]
blocks = []
for index, value in enumerate(chunks, 1):
    if value.startswith("<!--"):
        continue
    blocks.append({
        "id": f"p23-t{index:02d}",
        "kind": "heading" if value.startswith("# ") else "paragraph",
        "text": value.removeprefix("# "),
        "level": 1 if value.startswith("# ") else None,
        "page": 23,
    })
if len(blocks) != 5:
    raise SystemExit(f"Expected heading and four paragraphs, got {len(blocks)} blocks")
for block in blocks:
    if block["level"] is None:
        del block["level"]
chapter = {
    "bookId": "sutton-barto-reinforcement-learning-2e",
    "title": "第一部分 表格型求解方法",
    "toc": [{"number": "I", "title": "表格型求解方法", "block": blocks[0]["id"]}],
    "blocks": blocks,
}
output = BOOK / "chapter-I.json"
output.write_text(json.dumps(chapter, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
print(f"Wrote {output}: {len(blocks)} blocks")
