"""Bundle the verified introduction to Part III of Sutton and Barto."""

import json
import re
from pathlib import Path


root = Path(__file__).resolve().parents[1]
book = root / "books" / "sutton-barto-reinforcement-learning-2e"
source = (book / "parts" / "part-03.md").read_text(encoding="utf-8")
source = re.sub(r"<!--.*?-->", "", source, flags=re.S)
chunks = [chunk.strip() for chunk in re.split(r"\n\s*\n", source) if chunk.strip()]
if len(chunks) != 2 or not chunks[0].startswith("# "):
    raise SystemExit("Expected the Part III heading and one source paragraph")

blocks = [
    {"id": "p339-t01", "kind": "heading", "level": 1, "text": chunks[0][2:], "page": 339},
    {"id": "p339-t02", "kind": "paragraph", "text": chunks[1], "page": 339},
]
chapter = {
    "bookId": book.name,
    "title": "第三部分 深入探讨",
    "toc": [{"number": "III", "title": "深入探讨", "block": blocks[0]["id"]}],
    "blocks": blocks,
}
output = book / "chapter-III.json"
output.write_text(json.dumps(chapter, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
print(f"Wrote {output}: {len(blocks)} blocks")
