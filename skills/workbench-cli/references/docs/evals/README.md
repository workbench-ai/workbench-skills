# Workbench Eval Authoring

This directory is the canonical guide for creating hosted Workbench evaluations. Use it when a user wants a new `workbench.yaml`, wants to score a candidate with an existing workflow, or wants to build an evaluation from artifacts such as `.docx`, `.xlsx`, `.pdf`, or `.pptx` files.

Workbench eval authoring has two normal starting points:

- Existing workflow: start with [from-existing-workflow.md](from-existing-workflow.md) when the user already has a script, test command, benchmark harness, or manual scoring process.
- Artifact-first: start with [from-artifacts.md](from-artifacts.md) when the user has examples, goldens, reports, workbooks, decks, PDFs, or other opaque files and needs an agent to derive stable scoring signals.

Before writing a spec, read:

- [spec-syntax.md](spec-syntax.md) for the local/hosted YAML shape.
- [runner-contract.md](runner-contract.md) for staged directories, archive access, phase order, and the `WORKBENCH_REWARD_FILE` boundary.
- [cases-and-fixtures.md](cases-and-fixtures.md) for case directory layout and artifact evidence.
- [run-and-inspect.md](run-and-inspect.md) for the hosted CLI loop.

Artifact-specific guidance lives under [artifact-recipes/](artifact-recipes/):

- [docx.md](artifact-recipes/docx.md)
- [xlsx.md](artifact-recipes/xlsx.md)
- [pdf.md](artifact-recipes/pdf.md)
- [pptx.md](artifact-recipes/pptx.md)

Templates live under [templates/](templates/). Copy the whole project-shaped starter into a project and adapt names, commands, `evaluation.environment.with.image`, and scoring logic before applying the spec.

The authoring goal is not to make a perfect evaluator on the first pass. First make a small deterministic smoke evaluator that proves Workbench can stage the candidate, read the cases, run runner and grader phases, write a finite numeric score, and produce an inspectable candidate. Then tighten extraction, scoring, and case coverage.
