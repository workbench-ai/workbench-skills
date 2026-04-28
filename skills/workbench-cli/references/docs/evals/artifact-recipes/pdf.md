# PDF Artifact Recipe

Use this recipe for rendered reports, filings, invoices, statements, and fixed-layout outputs.

## Extract

Good PDF evidence includes:

- page count
- extracted text by page
- tables when the task depends on tabular data
- rendered page images for layout and visual checks
- OCR text for scanned PDFs
- bounding boxes for fields that must appear in specific regions

Use text extraction for content checks and rendered images for layout checks. OCR should be a fallback for scanned PDFs, not the default for born-digital PDFs.

## Score

Avoid requiring exact PDF bytes. Score by:

- required text and labels
- page count and section order
- key field values
- table extraction results
- rendered visual similarity within tolerance
- absence of placeholders or blank pages

For invoices and statements, make numeric fields explicit in case evidence so the evaluator can compare values with currency and rounding tolerance.

## Case Layout

```text
cases/
  invoice-render/
    input/source.json
    expected/golden.pdf
    expected/evidence.json
    rubric.md
```

If the candidate produces a PDF, write any extracted text or render diagnostics into `WORKBENCH_CANDIDATE_DIR/eval-summary.md` for inspection.
