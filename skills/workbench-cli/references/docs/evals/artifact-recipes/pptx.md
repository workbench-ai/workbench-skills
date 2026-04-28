# PPTX Artifact Recipe

Use this recipe for PowerPoint decks, investor presentations, board decks, and slide templates.

## Extract

Good PPTX evidence includes:

- slide count
- slide titles and speaker notes
- text boxes and bullet structure
- table and chart presence
- image and shape counts for key slides
- theme or layout names when relevant
- rendered slide images for layout-sensitive checks

Use a presentation parser for structure and LibreOffice or another renderer for slide images when visual layout matters.

## Score

Avoid comparing PPTX bytes. Score by:

- required slides exist and appear in the expected order
- required titles and key messages are present
- prohibited placeholder text is absent
- charts, tables, and images appear where required
- rendered slides stay within visual tolerance
- speaker notes or hidden metadata match requirements when relevant

## Case Layout

```text
cases/
  board-deck/
    input/outline.md
    expected/golden.pptx
    expected/evidence.json
    rubric.md
```

For generation tasks, put the source outline or data under `input/` and the expected deck or extracted slide evidence under `expected/`.
