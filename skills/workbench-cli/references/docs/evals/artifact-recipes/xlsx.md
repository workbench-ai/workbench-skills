# XLSX Artifact Recipe

Use this recipe for Excel workbooks, models, calculators, schedules, and exported tables.

## Extract

Good XLSX evidence includes:

- workbook sheet names and order
- named ranges
- formulas by cell or range
- cached values after recalculation when available
- key input, output, and check cells
- table dimensions and headers
- formatting only when it is part of the task

For financial models, include explicit tie-out checks such as balance sheet balance, cash flow linkage, debt schedule totals, and sign conventions.

## Score

Avoid comparing raw workbook bytes. Score by workbook semantics:

- required sheets exist
- required formulas exist and reference the expected ranges
- important outputs are within tolerance
- check cells pass
- no required formulas were hardcoded
- protected or non-editable areas were preserved when relevant

Use `better: higher` with a normalized `score`, or `better: lower` if the primary metric is an error count.

## Case Layout

```text
cases/
  debt-schedule/
    input/source.xlsx
    expected/golden.xlsx
    expected/checks.json
    rubric.md
```

`checks.json` should name the cells, ranges, formulas, and tolerances that matter. Keep it small enough for agents to inspect and explain.
