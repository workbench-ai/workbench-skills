# DOCX Artifact Recipe

Use this recipe for Word documents, contracts, reports, memos, and redlines.

## Extract

Good DOCX evidence includes:

- headings and section order
- paragraph text
- tables, row counts, column counts, and key cell values
- headers, footers, footnotes, and comments when relevant
- style names for required elements
- rendered page images for layout-sensitive checks

Use a DOCX parser for structure and an Office renderer for visual checks. If the runtime needs LibreOffice to render pages, use `docker://workbench/workbench-libreoffice-python:envv_libreoffice_python` or create a custom environment with the required tools.

## Score

Avoid byte-for-byte DOCX comparisons. DOCX files contain ids, timestamps, relationship ordering, and compression differences that often change even when the document is acceptable.

Score the document by combining:

- required text and headings
- required tables and values
- forbidden placeholder text
- approximate style or section checks
- optional rendered page similarity for layout-sensitive work

## Case Layout

```text
cases/
  board-memo/
    input/source.docx
    expected/golden.docx
    expected/evidence.json
    rubric.md
```

`evidence.json` should contain the extracted headings, required table checks, and any visual tolerances that matter.
