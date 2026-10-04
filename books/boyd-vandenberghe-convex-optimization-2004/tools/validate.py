"""Read-only source/output consistency checks; never a semantic review result."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from build import compile_chapter
from common import BOOK, CHAPTERS, CHAPTER_BY_ID
from link_references import strip_generated


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("chapters", nargs="*", help="Assigned chapter IDs; default: all required book units")
    parser.add_argument("--partial", action="store_true", help="Report structural gaps in a work-in-progress source")
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    unknown = [value for value in args.chapters if value not in CHAPTER_BY_ID]
    if unknown:
        parser.error(f"Unknown chapter IDs: {unknown}")
    selected = [CHAPTER_BY_ID[value] for value in args.chapters] if args.chapters else CHAPTERS
    reports = []
    failed = False
    for chapter in selected:
        source = BOOK / "translation" / chapter.source_name
        output = BOOK / f"chapter-{chapter.id}.json"
        report = {"chapterId": chapter.id, "sourceExists": source.is_file(), "outputExists": output.is_file(),
                  "semanticReview": "NOT PERFORMED"}
        if not source.is_file() or not output.is_file():
            failed = True
            report["structuralIssues"] = ["Missing source or generated reader JSON"]
        else:
            try:
                expected, details = compile_chapter(chapter, partial=args.partial)
                actual = json.loads(output.read_text(encoding="utf-8"))
                report.update(details)
                source_matches = strip_generated(actual) == expected
                report["generatedOutputMatchesSource"] = source_matches
                report["structuralIssues"] = ([] if source_matches else ["Generated reader JSON differs from the current Markdown build"])
                for key in ["equationCandidatesNotTagged", "taggedNumbersNotInCandidates", "figureCandidatesNotPresent"]:
                    if report[key]:
                        report["structuralIssues"].append(f"Resolve original-PDF candidate difference: {key}")
                if report["sourceCoverage"]["missingPdfPages"] or report["sourceCoverage"]["emptyNonblankPdfPages"]:
                    report["structuralIssues"].append("Missing page markers or empty nonblank pages")
                failed |= bool(report["structuralIssues"])
            except (ValueError, FileNotFoundError) as error:
                failed = True
                report["structuralIssues"] = [str(error)]
        reports.append(report)
        print(json.dumps({"chapter": chapter.id, "structuralIssues": report["structuralIssues"],
                          "semanticReview": "NOT PERFORMED"}, ensure_ascii=False), flush=True)
    result = {"scope": "Source/output structure and extracted-candidate comparisons only",
              "limitation": "No conclusion about translation completeness, meaning, formula correctness, image content, or visual quality.",
              "chapters": reports}
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    raise SystemExit(1 if failed else 0)


if __name__ == "__main__":
    main()
