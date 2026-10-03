"""Create a page-level locator for figures, tables, algorithms, and equation labels."""

from pathlib import Path
import re

import fitz


ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / "Christopher M. Bishop, Hugh Bishop - Deep Learning_ Foundations and Concepts-Springer (2024).pdf"
OUTPUT = ROOT / "books/bishop-deep-learning-2024/SOURCE_INVENTORY.md"
PATTERNS = {
    "图": re.compile(r"^Figure\s+((?:\d+|[A-C])\.\d+)\b"),
    "表": re.compile(r"^Table\s+((?:\d+|[A-C])\.\d+)\b"),
    "算法": re.compile(r"^Algorithm\s+((?:\d+|[A-C])\.\d+)\b"),
    "公式": re.compile(r"\(((?:\d+|[A-C])\.\d+)\)$"),
}


def main() -> None:
    with fitz.open(PDF) as document:
        starts = [(int(match.group(1)), title, page) for level, title, page in document.get_toc()
                  if level == 1 and (match := re.match(r"^(\d+)\s", title))]
        ranges = [
            (number, title, start, starts[index + 1][2] - 1 if index + 1 < len(starts) else 617)
            for index, (number, title, start) in enumerate(starts)
        ]
        ranges.extend([
            ("A", "Appendix A. Linear Algebra", 618, 624),
            ("B", "Appendix B. Calculus of Variations", 625, 627),
            ("C", "Appendix C. Lagrange Multipliers", 628, 631),
        ])
        lines = [
            "# Bishop 原书逐页定位索引",
            "",
            "此索引由 PDF 文本层自动提取，只用于定位；图、表、公式和算法是否齐全，必须逐页目视核对。",
            "页码为 PDF 物理页。原书中没有编号的章节开篇图、图内文字、脚注和代码仍须人工核对。",
            "",
        ]
        for number, title, start, end in ranges:
            lines.extend([f"## {title}（PDF 第 {start}–{end} 页）", "", "| PDF 页 | 图 | 表 | 算法 | 公式编号 |", "| ---: | --- | --- | --- | --- |"])
            for page_number in range(start, end + 1):
                matches = {name: [] for name in PATTERNS}
                for raw_line in document[page_number - 1].get_text().splitlines():
                    line = raw_line.strip()
                    for name, pattern in PATTERNS.items():
                        match = pattern.search(line) if name == "公式" else pattern.match(line)
                        if match and match.group(1).startswith(f"{number}.") and match.group(1) not in matches[name]:
                            matches[name].append(match.group(1))
                cells = [", ".join(matches[name]) or "—" for name in ("图", "表", "算法", "公式")]
                lines.append(f"| {page_number} | {' | '.join(cells)} |")
            lines.append("")
    OUTPUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {OUTPUT}")


if __name__ == "__main__":
    main()
