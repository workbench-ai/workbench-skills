---
name: workbench-cli
description: >-
  Use this skill whenever the user wants to configure, create evaluations for,
  run, inspect, compare, improve, or export Workbench projects with the
  `workbench` CLI, including evals based on existing workflows or artifacts such
  as DOCX, XLSX, PDF, and PPTX files.
---

# Workbench CLI

Use the `workbench` CLI as the cloud-first Workbench interface. Normal commands target hosted projects; local execution is development mode under `workbench dev`.

The user-facing resources are:

- source directory: local `workbench.yaml`, `candidate/`, `cases/`, and optional `.workbench/link.json`
- project: the hosted Workbench project
- artifact: a candidate `skill`, `pipeline`, or `command`
- environment: the exact Docker/OCI runtime selected by `evaluation.environment.with.image` for command adapters
- run: hosted `eval`, `improve`, or `compare`
- candidate: hosted output snapshot that can be inspected, previewed, and pulled

## CLI Availability

Before using hosted project commands, verify that the `workbench` binary is available:

```bash
workbench --version
```

If the command is missing, install the published CLI from GitHub Packages:

```bash
npm config set @workbench-ai:registry https://npm.pkg.github.com
npm install -g @workbench-ai/workbench-cli
workbench --version
```

If npm reports a GitHub Packages auth or registry error, tell the user that npm needs `@workbench-ai` GitHub Packages access with a token that can read packages, then stop cleanly instead of falling back to a local monorepo build.

## Working Rules

- Use `workbench init --artifact skill|pipeline|command --name NAME`, `workbench launch --name NAME`, and `workbench sync` to create and connect a local source directory to a hosted project.
- Use `workbench eval`, `workbench improve`, and `workbench compare` for hosted workflows. Add `--watch` when the user wants to wait for completion.
- Use `workbench dev improve`, `workbench dev eval`, and `workbench dev compare` only when the user explicitly wants local development without hosted API calls.
- Use `workbench check` to validate local `workbench.yaml`.
- Use `workbench envs list` and `workbench envs create --project ID --name NAME --dockerfile PATH|-` for runtime environments.
- Use `workbench candidates list`, `workbench candidates files`, `workbench candidates preview`, and `workbench candidates pull` for hosted inspection and retrieval.
- Use `workbench dev candidates`, `workbench dev files`, `workbench dev preview`, and `workbench dev restore --dry-run|--yes` for local development history.
- Prefer `--json` when another tool or agent needs structured output.
- Use `--dir DIR` to target a source directory. Do not use `--workspace`.

## Common Hosted Flow

```bash
workbench init --artifact skill --name my-eval --agent codex
workbench launch --name my-eval
workbench sync
workbench eval --samples 1 --watch
workbench improve --budget 2 --samples 1 --watch
workbench compare --samples 1 --watch
workbench candidates list
workbench pull <candidate-id> --out ./best-candidate
```

Use `workbench link PROJECT_ID` when a hosted project already exists. Use `--project ID` for one-off commands without writing `.workbench/link.json`.

## Evaluation Creation

When the user wants to create a Workbench eval, first read [references/docs/evals/README.md](references/docs/evals/README.md). In the authored repo tree, the same content lives under `docs/evals/`.

- Use [references/docs/evals/spec-syntax.md](references/docs/evals/spec-syntax.md) before writing or editing `workbench.yaml`.
- Use [references/docs/evals/runner-contract.md](references/docs/evals/runner-contract.md) before writing runner/grader commands or the `WORKBENCH_REWARD_FILE` reward output.
- Use [references/docs/evals/from-existing-workflow.md](references/docs/evals/from-existing-workflow.md) when the user already has a benchmark, test suite, script, or manual scoring workflow.
- Use [references/docs/evals/from-artifacts.md](references/docs/evals/from-artifacts.md) when the user has documents, spreadsheets, PDFs, decks, goldens, examples, or other opaque artifacts and needs a deterministic evaluator.
- For artifact-first evals, load only the matching recipe from `references/docs/evals/artifact-recipes/`: `docx.md`, `xlsx.md`, `pdf.md`, or `pptx.md`.

Do not treat `skills/workbench-cli/evals/` as user project eval examples. That directory is the skill-ergonomics catalog for testing this skill.

## Local References

- Read [references/docs/cli.md](references/docs/cli.md) for the canonical CLI guide. In the authored repo tree, the same content lives under `docs/cli.md`.
- Read [references/SPEC.md](references/SPEC.md) when you need the command and spec contract.
- Read [references/docs/evals/](references/docs/evals/) when you need to create or explain Workbench eval specs, runner commands, cases, or artifact-first evaluation recipes.
