"""Build this book's image cache manifest from all 23 reader documents."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from common import BOOK, BOOK_ID, CHAPTERS, ROOT


def build_manifest() -> tuple[dict, list[dict]]:
    paths = set()
    for chapter in CHAPTERS:
        document = json.loads((BOOK / f"chapter-{chapter.id}.json").read_text(encoding="utf-8"))
        if document["bookId"] != BOOK_ID or document["chapterId"] != chapter.id:
            raise ValueError(f"Wrong document identity: {chapter.id}")
        paths.update(document["images"])
    records = []
    for asset in sorted(paths):
        path = (ROOT / asset).resolve()
        if (not asset.startswith(f"books/{BOOK_ID}/assets/") or ".." in asset
                or not path.is_relative_to((BOOK / "assets").resolve())
                or path.suffix.lower() not in {".png", ".jpg", ".jpeg", ".webp", ".gif", ".svg"}):
            raise ValueError(f"Invalid book image: {asset}")
        data = path.read_bytes()
        records.append({"path": asset, "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()})
    fingerprint = json.dumps(records, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    return {"bookId": BOOK_ID, "version": hashlib.sha256(fingerprint).hexdigest()[:20],
            "totalBytes": sum(item["bytes"] for item in records),
            "assets": [item["path"] for item in records]}, records


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Check without replacing the manifest")
    parser.add_argument("--report", type=Path, help="Optional asset hashes for an audit record")
    args = parser.parse_args()
    manifest, evidence = build_manifest()
    output = BOOK / "offline-images.json"
    if args.check:
        if json.loads(output.read_text(encoding="utf-8")) != manifest:
            raise SystemExit("Offline image manifest needs rebuilding")
    else:
        output.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps({"manifest": manifest, "evidence": evidence},
                                         ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"images": len(evidence), "totalBytes": manifest["totalBytes"],
                      "version": manifest["version"], "checkOnly": args.check}))
