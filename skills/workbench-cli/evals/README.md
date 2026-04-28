# Workbench CLI Skill-Eval Catalog

This directory holds the product-local ergonomics catalog for the `workbench` CLI skill. It tests whether the skill drives the shared local/hosted CLI correctly and whether agents use the eval-authoring docs when creating project evaluations.

It is not the user-facing guide for creating Workbench project evaluations. Eval authoring guidance lives under `products/workbench-cli/docs/evals/` and is copied into installed skills as `references/docs/evals/`.

The evals intentionally cover the hosted deployment contract, local/hosted targeting rules, and eval-authoring entry points:

- configuring a hosted API target
- verifying or installing the published CLI package
- authoring evals from existing workflows
- authoring evals from `.docx`, `.xlsx`, `.pdf`, or `.pptx` artifacts
- creating a project and applying a spec
- creating project-specific Dockerfile environments
- syncing spec, candidate, and case snapshots
- starting and watching eval/improve/compare workflows
- inspecting, previewing, and exporting hosted candidates

They must not reward private `.workbench/` archive inspection or bundled `workbench ui` behavior. Local `workbench init`, `workbench check`, `workbench dev improve`, checkpoint, and restore are valid public CLI behavior, but this catalog remains focused on hosted deployment tasks and eval authoring.

Validate the catalog from `products/workbench-cli`:

```bash
pnpm cli-skill-evals:validate
```
