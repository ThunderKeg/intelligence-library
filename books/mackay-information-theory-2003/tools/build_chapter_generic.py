"""Compile a page-aligned MacKay chapter for review without publishing it.

Use for later chapters that do not need special layout transforms. All source
pages must exist, and the full chapter validates its expected sections and
numbered equations before producing an ignored draft JSON.
"""

import argparse
import importlib.util
import json
import re
from pathlib import Path


BOOK = Path(__file__).resolve().parents[1]
PARSER = Path(__file__).with_name("build_chapter_01.py")
spec = importlib.util.spec_from_file_location("mackay_chapter_builder", PARSER)
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)


def main():
    cli = argparse.ArgumentParser()
    cli.add_argument("--chapter", type=int, required=True)
    cli.add_argument("--start", type=int, required=True, help="first physical PDF page")
    cli.add_argument("--end", type=int, required=True, help="last physical PDF page")
    cli.add_argument("--through", type=int, help="last translated page for partial preview")
    cli.add_argument("--title", required=True, help="reviewed Chinese chapter title")
    cli.add_argument("--sections", type=int, required=True, help="number of numbered top-level sections")
    cli.add_argument("--first-equation", type=int, default=1, help="first numbered equation on these body pages")
    cli.add_argument("--equations", type=int, required=True, help="last numbered equation in the chapter")
    args = cli.parse_args()
    through = args.through or args.end
    if not 1 <= args.chapter <= 50 or not 1 <= args.start <= through <= args.end <= 640 or not 1 <= args.first_equation <= args.equations:
        cli.error("invalid chapter number or physical PDF page range")
    chapter_dir = f"chapter-{args.chapter:02d}"
    image_match = re.compile(rf"^\.\./\.\./assets/{chapter_dir}/([\w.-]+\.(?:png|jpg|svg|webp))$")
    heading_match = re.compile(rf"^({args.chapter}(?:\.\d+)*)\s+(.+)$")

    def chapter_image(source: str) -> str:
        match = image_match.fullmatch(source)
        if not match:
            raise ValueError(f"Unexpected chapter {args.chapter} image path: {source}")
        path = BOOK / "assets" / chapter_dir / match.group(1)
        if not path.is_file():
            raise FileNotFoundError(path)
        return f"assets/{chapter_dir}/{match.group(1)}"

    blocks = [
        block
        for page in range(args.start, through + 1)
        for block in builder.compile_page(
            page,
            source=BOOK / "translation" / chapter_dir / f"pdf-{page:03d}.md",
            image_resolver=chapter_image,
            chapter_start=args.start,
            chapter_number=args.chapter,
        )
    ]
    if not blocks or blocks[0]["kind"] != "heading":
        raise ValueError(f"Chapter {args.chapter} heading missing")
    if not any(block["kind"] == "intro" for block in blocks):
        raise ValueError(f"Chapter {args.chapter} editor's introduction missing")
    for block in blocks:
        if block["kind"] == "figure" and block["width"] >= 560:
            block["wide"] = True
    toc = []
    for block in blocks:
        if block["kind"] != "heading":
            continue
        match = heading_match.match(block["text"])
        if block["level"] == 1:
            toc.append({"number": str(args.chapter), "title": args.title, "block": block["id"]})
        elif match and block["level"] == 2:
            toc.append({"number": match.group(1), "title": match.group(2), "block": block["id"]})
    if through == args.end and [entry["number"] for entry in toc] != (
        [str(args.chapter)] + [f"{args.chapter}.{n}" for n in range(1, args.sections + 1)]
    ):
        raise ValueError(f"Unexpected chapter {args.chapter} sections: {toc}")
    numbers = [block["number"] for block in blocks if block["kind"] == "formula" and block["number"]]
    if len(numbers) != len(set(numbers)):
        raise ValueError(f"Duplicate chapter {args.chapter} equation number")
    if through == args.end and numbers != [f"({args.chapter}.{n})" for n in range(args.first_equation, args.equations + 1)]:
        raise ValueError(f"Chapter {args.chapter} equations are missing or out of order: {numbers}")
    builder.compile_math(blocks)
    if args.chapter == 5 and through >= 111:
        algorithm_positions = [
            index for index, block in enumerate(blocks)
            if block["kind"] == "paragraph" and block["text"].startswith("算法 5.4")
        ]
        if len(algorithm_positions) != 1:
            raise ValueError("Algorithm 5.4 title missing or duplicated")
        index = algorithm_positions[0]
        title, steps = blocks[index : index + 2]
        if steps["kind"] != "list" or not steps["ordered"] or len(steps["items"]) != 2:
            raise ValueError("Algorithm 5.4 must contain its two ordered steps")
        blocks[index : index + 2] = [{
            "id": "box-5-4", "kind": "box", "pdfPage": 111,
            "page": 111 - args.start + 1, "outlined": True,
            "blocks": [title, steps],
        }]
    if args.chapter == 6:
        tables = [block for block in blocks if block["kind"] == "table"]
        if through == args.end and len(tables) != 4:
            raise ValueError(f"Chapter 6 requires four source tables, found {len(tables)}")
        for table in tables:
            table["codeTable"] = True
        if through >= 125:
            positions = [
                index for index, block in enumerate(blocks)
                if block["kind"] == "paragraph" and block["text"].startswith("算法 6.3　算术编码")
            ]
            if len(positions) != 1:
                raise ValueError("Algorithm 6.3 title missing or duplicated")
            index = positions[0]
            title, code = blocks[index : index + 2]
            if code["kind"] != "code":
                raise ValueError("Algorithm 6.3 code must follow its title")
            blocks[index : index + 2] = [{
                "id": "box-6-3", "kind": "box", "pdfPage": 125,
                "page": 125 - args.start + 1, "outlined": True,
                "blocks": [title, code],
            }]
    if args.chapter == 7:
        tables = [block for block in blocks if block["kind"] == "table"]
        if through == args.end and len(tables) != 5:
            raise ValueError(f"Chapter 7 requires five source tables, found {len(tables)}")
        for table in tables:
            table["codeTable"] = True
        if through >= 147:
            positions = [
                index for index, block in enumerate(blocks)
                if block["kind"] == "paragraph" and block["text"].startswith("算法 7.4　整数")
            ]
            if len(positions) != 1:
                raise ValueError("Algorithm 7.4 title missing or duplicated")
            index = positions[0]
            title, code = blocks[index : index + 2]
            if code["kind"] != "code":
                raise ValueError("Algorithm 7.4 code must follow its title")
            blocks[index : index + 2] = [{
                "id": "box-7-4", "kind": "box", "pdfPage": 147,
                "page": 147 - args.start + 1, "outlined": True,
                "blocks": [title, code],
            }]
    if args.chapter == 19 and through >= 286:
        positions = [index for index, block in enumerate(blocks) if block["pdfPage"] == 286]
        if len(positions) != 14 or positions != list(range(positions[0], positions[0] + 14)):
            raise ValueError("Box 19.2 must contain the 14 consecutive PDF 286 blocks")
        first, last = positions[0], positions[-1]
        contents = blocks[first : last + 1]
        if not contents[0]["text"].startswith("框 19.2") or [block["kind"] for block in contents].count("formula") != 6:
            raise ValueError("Box 19.2 title or six display formulas missing")
        blocks[first : last + 1] = [{
            "id": "box-19-2", "kind": "box", "pdfPage": 286,
            "page": 286 - args.start + 1, "outlined": True,
            "blocks": contents,
        }]
    if args.chapter == 26 and through >= 348:
        first = next(index for index, block in enumerate(blocks)
                     if block["id"] == "p348-b006")
        contents = blocks[first : first + 4]
        if [block["id"] for block in contents] != [f"p348-b{index:03d}" for index in range(6, 10)]:
            raise ValueError("Chapter 26 boxed sum-product rules are not consecutive")
        if [block["kind"] for block in contents] != ["paragraph", "formula", "paragraph", "formula"] or [
            block["number"] for block in contents if block["kind"] == "formula"
        ] != ["(26.11)", "(26.12)"]:
            raise ValueError("Chapter 26 boxed sum-product rules are incomplete")
        blocks[first : first + 4] = [{
            "id": "box-26-rules", "kind": "box", "pdfPage": 348,
            "page": 348 - args.start + 1, "outlined": True,
            "blocks": contents,
        }]
    chapter = {
        "schemaVersion": 2,
        "bookId": "mackay-information-theory-2003",
        "title": blocks[0]["text"],
        "sourcePdfPages": [args.start, through],
        "toc": toc,
        "blocks": blocks,
    }
    suffix = "draft" if through == args.end else "partial"
    output = BOOK / f"chapter-{args.chapter:02d}.{suffix}.json"
    output.write_text(json.dumps(chapter, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(f"Wrote {output}: {len(blocks)} blocks, {len(toc)} sections, {len(numbers)} numbered formulas")


if __name__ == "__main__":
    main()
