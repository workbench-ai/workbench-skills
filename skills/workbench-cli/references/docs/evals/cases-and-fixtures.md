# Cases And Fixtures

Cases are uploaded by `workbench sync`. They are frozen onto each run and staged under `WORKBENCH_CASES_DIR` for every evaluation job. A case can be a single file or a folder with inputs, expected outputs, rubrics, and extracted evidence.

## Recommended Layout

```text
cases/
  case-001/
    input/
      source.docx
    expected/
      golden.docx
      evidence.json
    rubric.md
  case-002/
    input/
    expected/
      text.txt
    rubric.md
```

Use stable, descriptive case folder names when possible:

```text
cases/
  monthly-board-deck/
  debt-schedule-workbook/
  redline-contract/
```

## What Belongs In Cases

Cases should contain evidence the candidate should not edit:

- source artifacts supplied to the workflow
- golden outputs
- extracted text or structural JSON
- scoring rubrics
- small fixture data
- expected values and tolerances

Do not put mutable prompts, templates, or scripts in cases when Workbench should improve them. Put those files under the candidate root instead.

Every smoke case should contain at least one non-empty expected signal, such as `expected/text.txt` or `expected/evidence.json`. Empty expected folders are placeholders only; they should not be treated as passing cases.

The hosted CLI uploads binary artifacts as base64 snapshots automatically, so cases may contain real `.docx`, `.xlsx`, `.pdf`, or `.pptx` files alongside extracted text and JSON evidence.

## Evidence Files

For artifact-heavy evals, prefer explicit evidence files:

```json
{
  "requiredHeadings": ["Executive Summary", "Risks", "Recommendation"],
  "tables": [
    { "name": "Revenue Bridge", "minRows": 4, "minColumns": 3 }
  ],
  "visualChecks": [
    { "page": 1, "description": "Logo appears in the header." }
  ]
}
```

Evidence files should be generated from goldens when practical, then reviewed and checked in with the cases. This makes scoring explainable and avoids brittle byte-for-byte comparisons.

## Case Count

Start with one or two smoke cases. Add broader case coverage after the runner is stable. A small case set that catches the most important failure modes is better than a large set that is slow, flaky, or hard to explain.
