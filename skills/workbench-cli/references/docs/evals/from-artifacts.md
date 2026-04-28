# From Artifacts

Use this path when the user gives examples or goldens as artifacts such as `.docx`, `.xlsx`, `.pdf`, or `.pptx` files. The job is to turn opaque files into stable evaluation signals before writing `workbench.yaml`.

Artifact-first eval creation is a two-step process:

1. Extract comparable evidence from each artifact.
2. Score candidate artifacts against that evidence with a deterministic evaluator.

Do not ask the model to judge a binary file directly. Convert artifacts into text, structured JSON, rendered page images, formulas, tables, metadata, or other stable signals, then score those signals.

## Case Layout

Use one folder per case:

```text
cases/
  board-report-format/
    input/
      source.docx
    expected/
      golden.docx
    rubric.md
  forecast-workbook/
    input/
      draft.xlsx
    expected/
      golden.xlsx
    rubric.md
```

`input/` contains files the candidate workflow consumes. `expected/` contains goldens, reference outputs, or extracted evidence. `rubric.md` states what matters and what should not affect the score.

## Candidate Layout

Keep the mutable surface narrow:

```text
candidate/
  prompt.md
  output.txt
  template.docx
  build_report.py
  evaluate-artifacts.py
```

The starter template uses `output.txt` only as a smoke-test stand-in for a real generated artifact. Replace it with the real output path or generation script as soon as the evaluator proves it can stage cases and produce a finite score.

If Workbench should improve a source artifact, include that artifact in `candidate.editable`. If Workbench should improve a prompt or generation script, keep the artifact examples in `cases/` and include only the prompt or script under `candidate.editable`.

## Artifact Evidence

Create evidence that is stable across runs:

- Text: headings, paragraphs, slide titles, footnotes, cell labels, comments.
- Structure: table dimensions, sheet names, named ranges, formulas, section order, slide object counts.
- Rendered output: page images or slide images for visual checks.
- Metrics: balance checks, formula counts, missing values, pass/fail criteria, layout tolerances.

The evaluator can compute these signals live from artifacts, or case folders can include pre-extracted evidence such as `expected/evidence.json`. Pre-extracted evidence makes cases faster and easier to debug, but the extraction script should stay available so goldens can be regenerated deliberately.

## Scoring

Score the behavior the user cares about, not incidental byte equality. Office and PDF files often contain timestamps, ids, compression differences, or layout metadata that should not affect evaluation.

Good artifact scores combine multiple checks:

- Required content exists.
- Prohibited content is absent.
- Structure matches expected sections, sheets, slides, or tables.
- Numeric calculations tie out within tolerance.
- Rendered pages or slides stay within visual tolerances.
- The output opens successfully with the intended toolchain.

Keep artifact extraction in `evaluation.runner` and put scoring in the required `evaluation.grader`. Command graders write `WORKBENCH_REWARD_FILE` after reading runner evidence. The same reward boundary is described in [runner-contract.md](runner-contract.md).

## Recipes

Read only the recipe that matches the artifact type:

- Word documents: [artifact-recipes/docx.md](artifact-recipes/docx.md)
- Excel workbooks: [artifact-recipes/xlsx.md](artifact-recipes/xlsx.md)
- PDFs: [artifact-recipes/pdf.md](artifact-recipes/pdf.md)
- PowerPoint decks: [artifact-recipes/pptx.md](artifact-recipes/pptx.md)

If a case has multiple artifact types, use the dominant output artifact as the primary recipe and add secondary checks from the other recipes.
