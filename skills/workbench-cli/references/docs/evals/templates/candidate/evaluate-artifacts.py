import json
import os
import re
import sys
from pathlib import Path


def read_required_text(path: Path) -> tuple[str, str | None]:
    if not path.exists():
        return "", f"Missing required file: {path}"
    text = path.read_text(encoding="utf-8", errors="replace").strip()
    if not text:
        return "", f"Required file is empty: {path}"
    return text, None


def read_optional_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def words(text: str) -> set[str]:
    return {match.group(0).lower() for match in re.finditer(r"[A-Za-z0-9_]+", text)}


def score_text_overlap(actual: str, expected: str) -> float:
    expected_words = words(expected)
    if not expected_words:
        return 0.0
    actual_words = words(actual)
    return len(expected_words & actual_words) / len(expected_words)


candidate_dir = Path(os.environ["WORKBENCH_CANDIDATE_DIR"])
cases_dir = Path(os.environ["WORKBENCH_CASES_DIR"])
output_dir = Path(os.environ["WORKBENCH_OUTPUT_DIR"])
output_dir.mkdir(parents=True, exist_ok=True)
mode = sys.argv[1] if len(sys.argv) > 1 else "--run-only"

case_dirs = sorted(path for path in cases_dir.iterdir() if path.is_dir()) if cases_dir.exists() else []
case_results = []
issues = []
fatal_issues = []

if not case_dirs:
    issue = f"No case folders found under {cases_dir}"
    issues.append(issue)
    fatal_issues.append(issue)

for case_dir in case_dirs:
    expected_text, expected_issue = read_required_text(case_dir / "expected" / "text.txt")
    actual_text = read_optional_text(candidate_dir / "outputs" / f"{case_dir.name}.txt")
    if not actual_text:
        actual_text = read_optional_text(candidate_dir / "output.txt")

    case_issues = []
    if expected_issue:
        case_issues.append(expected_issue)
        fatal_issues.append(expected_issue)
    if not actual_text.strip():
        case_issues.append(
            f"No candidate output found for {case_dir.name}; expected outputs/{case_dir.name}.txt or output.txt"
        )

    case_score = 0.0 if case_issues else score_text_overlap(actual_text, expected_text)
    case_results.append({
        "id": case_dir.name,
        "score": round(case_score, 3),
        "expectedTextWords": len(words(expected_text)),
        "actualTextWords": len(words(actual_text)),
        "issues": case_issues,
    })
    issues.extend(case_issues)

score = sum(item["score"] for item in case_results) / len(case_results) if case_results else 0.0
summary_lines = [
    "# Artifact eval summary",
    "",
    f"Cases: {len(case_results)}",
    f"Score: {score:.3f}",
    f"Issues: {len(issues)}",
]
for item in case_results:
    summary_lines.append(f"- {item['id']}: {item['score']:.3f}")
    for issue in item["issues"]:
        summary_lines.append(f"  - {issue}")
(candidate_dir / "eval-summary.md").write_text("\n".join(summary_lines) + "\n", encoding="utf-8")

payload = {
    "score": round(score, 3),
    "summary": f"Scored {len(case_results)} artifact case(s) with {len(issues)} issue(s).",
    "fileChanges": ["eval-summary.md"],
    "cases": [
        {
            "id": item["id"],
            "label": item["id"],
            "status": "passed" if item["score"] >= 0.8 else "failed",
            "metrics": {"score": item["score"]},
            "feedback": {"issues": item["issues"]},
        }
        for item in case_results
    ],
    "feedback": {
        "caseResults": case_results,
        "issues": issues,
        "note": "Replace this text-overlap smoke evaluator with artifact-specific extraction before using it as a real benchmark.",
    },
}

if mode == "--run-only":
    (output_dir / "runner-evidence.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
elif mode == "--grade-only":
    Path(os.environ["WORKBENCH_REWARD_FILE"]).write_text(json.dumps(payload, indent=2), encoding="utf-8")
else:
    raise SystemExit("Expected --run-only or --grade-only")

if fatal_issues:
    raise SystemExit(1)
