"""Build the MacKay reader's image manifest from its staged book assets."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


BOOK = Path(__file__).resolve().parents[1]
BOOK_ID = "mackay-information-theory-2003"
ROOT = BOOK.parents[1]
OUTPUT = BOOK / "offline-images.json"
IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".svg"}


def build_manifest() -> dict:
    assets = sorted(path for path in (BOOK / "assets").rglob("*") if path.is_file())
    records = []
    for path in assets:
        if path.suffix.lower() not in IMAGE_SUFFIXES:
            raise ValueError(f"Unexpected non-image asset: {path}")
        relative = path.relative_to(ROOT).as_posix()
        if not relative.startswith(f"books/{BOOK_ID}/assets/") or ".." in relative:
            raise ValueError(f"Unsafe asset path: {relative}")
        data = path.read_bytes()
        records.append({"path": relative, "bytes": len(data),
                        "sha256": hashlib.sha256(data).hexdigest()})
    fingerprint = json.dumps(records, ensure_ascii=False,
                             separators=(",", ":")).encode("utf-8")
    return {"bookId": BOOK_ID,
            "version": hashlib.sha256(fingerprint).hexdigest()[:20],
            "totalBytes": sum(record["bytes"] for record in records),
            "assets": [record["path"] for record in records]}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true",
                        help="Verify the saved manifest without changing it")
    args = parser.parse_args()
    manifest = build_manifest()
    if args.check:
        if json.loads(OUTPUT.read_text(encoding="utf-8")) != manifest:
            raise SystemExit("Offline image manifest needs rebuilding")
    else:
        OUTPUT.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
                          encoding="utf-8")
    print(json.dumps({"images": len(manifest["assets"]),
                      "totalBytes": manifest["totalBytes"],
                      "version": manifest["version"], "checkOnly": args.check}))


if __name__ == "__main__":
    main()
