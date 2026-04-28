# Workbench CLI Specification

## Status

This is the current product contract for `products/workbench-cli`. The CLI is cloud-first: top-level workflow and resource commands target hosted Workbench projects, while local-only execution is explicitly under `workbench dev`.

## Public Model

Durable resources live in Workbench Web:

- `project`: one hosted Workbench project.
- `spec`: the project YAML contract for power users and agents.
- `candidate`: a hosted file snapshot Workbench can inspect, improve, compare, and pull.
- `cases`: uploaded evaluation examples or fixtures.
- `environment`: a built-in or user-defined Docker/OCI runtime selected by exact image ref.
- `run`: a hosted `eval`, `improve`, or `compare` workflow.

Local source directories contain `workbench.yaml`, `candidate/`, `cases/`, and an optional `.workbench/link.json`. The link file records the hosted project id and API base URL. Local source state is disposable; hosted project state is durable.

## Configuration

The CLI resolves the API base URL from `WORKBENCH_API_URL`, then the linked project URL, then the login config written by `workbench login --base-url URL`, then `https://v2.workbench.ai`.

`workbench login` uses the Workbench web portal OAuth device flow. Manual pasted bearer tokens are not part of the product contract.

## Commands

Supported commands:

```bash
workbench <command> [options]
workbench launch --name NAME [--description TEXT] [--dir DIR] [--dry-run] [--json]
workbench link PROJECT_ID [--dir DIR] [--dry-run] [--json]
workbench sync [--dir DIR] [--project ID] [--dry-run] [--json]
workbench eval [--dir DIR] [--project ID] [--candidate ID] [--samples N] [--no-sync] [--watch] [--dry-run] [--json]
workbench improve [--dir DIR] [--project ID] [--budget N] [--samples N] [--no-sync] [--watch] [--dry-run] [--json]
workbench compare [--dir DIR] [--project ID] [--candidate ID] [--samples N] [--no-sync] [--watch] [--dry-run] [--json]
workbench watch [RUN_ID] [--dir DIR] [--project ID] [--interval-ms N] [--timeout-ms N] [--json]
workbench pull CANDIDATE_ID --out DIR [--dir DIR] [--project ID] [--dry-run] [--json]
workbench init [DIR] --artifact skill|pipeline|command --name NAME [--agent codex|claude|pi] [--from PATH] [--example] [--json]
workbench check [--dir DIR] [--json]
workbench unlink [--dir DIR] [--dry-run] [--json]
workbench status [--dir DIR] [--project ID] [--json]
workbench open [RUN_ID|CANDIDATE_ID] [--dir DIR] [--project ID] [--json]
workbench projects list [--json]
workbench projects show [PROJECT_ID] [--dir DIR] [--project ID] [--json]
workbench envs list [--dir DIR] [--project ID] [--json]
workbench envs create --name NAME --dockerfile PATH|- [--dir DIR] [--project ID] [--cpu N] [--memory-gb N] [--disk-gb N] [--timeout-minutes N] [--network off|on] [--dry-run] [--json]
workbench runs list [--dir DIR] [--project ID] [--json]
workbench runs show [RUN_ID] [--dir DIR] [--project ID] [--json]
workbench candidates list [--dir DIR] [--project ID] [--json]
workbench candidates files CANDIDATE_ID [--dir DIR] [--project ID] [--json]
workbench candidates preview CANDIDATE_ID --path PATH [--dir DIR] [--project ID] [--output PATH|-] [--json]
workbench candidates pull CANDIDATE_ID --out DIR [--dir DIR] [--project ID] [--dry-run] [--json]
workbench logs [RUN_ID] [--dir DIR] [--project ID] [--json]
workbench dev eval [--dir DIR] [--candidate ID] [--samples N] [--json]
workbench dev improve [--dir DIR] [--budget N] [--samples N] [--json]
workbench dev compare [--dir DIR] [--candidate ID] [--samples N] [--json]
workbench dev checkpoint [--dir DIR] [--json]
workbench dev restore [--dir DIR] [--candidate ID] [--dry-run] [--yes] [--json]
workbench dev candidates [--dir DIR] [--json]
workbench dev files [--dir DIR] [--candidate ID] [--json]
workbench dev preview [--dir DIR] [--candidate ID] --path PATH [--output PATH|-] [--json]
workbench dev comparisons [--dir DIR] [--json]
workbench login [--base-url URL] [--no-open] [--json]
workbench logout [--json]
workbench whoami [--json]
workbench --help
workbench --version
```

Bare `workbench` prints help and exits `0`. Unknown commands print a usage error and exit `2`. Mutating hosted commands that support `--dry-run` do not contact the API or write link/output files. Destructive local restore requires either `--dry-run` or `--yes`.

## Hosted Workflows

`workbench sync` validates the local source, applies `workbench.yaml`, uploads `candidate/`, and uploads `cases/` to the linked or specified hosted project.

`workbench eval` creates a hosted run with `workflow: "eval"`. It evaluates the requested candidate, the active hosted candidate, or the uploaded candidate snapshot if no candidate exists. It queues current-variant runner and grader executions and does not propose changes.

`workbench improve` creates a hosted run with `workflow: "improve"`. It queues proposer executions up to `--budget`, then runner and grader executions for each proposed candidate, and updates hosted candidate history by greedy selection.

`workbench compare` creates a hosted run with `workflow: "compare"`. It evaluates the requested or active candidate across `current` plus configured `evaluation.variants` and writes a comparison record.

All workflows freeze the current spec revision, base candidate files, and case files onto the run input. `evaluation.cases.include` filters the frozen case surface when present. Runner phases never receive `WORKBENCH_REWARD_FILE`; only command grader phases can write reward output.

## Local Development

`workbench dev improve`, `workbench dev eval`, and `workbench dev compare` run against a local source directory without hosted API calls. They use `--dir`, share the same `workbench.yaml` contract, and store local history under `.workbench/`. The legacy `--workspace` flag is rejected.

## Spec Authoring Contract

The hosted API stores the spec as YAML source. The canonical authoring guide lives under [`docs/evals/`](docs/evals/):

- [`docs/evals/spec-syntax.md`](docs/evals/spec-syntax.md) owns the YAML shape.
- [`docs/evals/runner-contract.md`](docs/evals/runner-contract.md) owns staged runtime directories, environment variables, and `WORKBENCH_REWARD_FILE`.
- [`docs/evals/from-existing-workflow.md`](docs/evals/from-existing-workflow.md) owns the workflow-wrapping path.
- [`docs/evals/from-artifacts.md`](docs/evals/from-artifacts.md) owns artifact-first eval creation from `.docx`, `.xlsx`, `.pdf`, `.pptx`, and similar files.

The validator accepts the version-6 YAML shape: `version: 6`, `name`, `candidate.kind`, `candidate.root`, `candidate.entry`, `candidate.editable`, `optimization.goal`, generic `optimization.proposer.use` plus optional `with`, `optimization.selection`, `evaluation.task`, `evaluation.cases.root`, `evaluation.runner`, and required `evaluation.grader`. `candidate.kind` is `skill`, `pipeline`, or `command`. `evaluation.runner.use` may be `skill`, `pipeline`, or `command`; command adapters require `evaluation.environment.use: oci` and `evaluation.environment.with.image`, while skill and pipeline runners are agent/template backed. Executable blocks use the same `use` plus `with` adapter envelope. Provider auth and harness config are resolved by sandbox adapters, not stored in public YAML. Top-level `goal`, `eval`, `runtime`, `runner`, `strategy`, and `variants` are rejected.

## Runtime Environments

The runtime environment model is OCI-image-first for command adapters. Built-in environments provide common bases such as Python, Node, and LibreOffice plus Python, and each built-in environment is backed by a Dockerfile under `products/workbench-cli/environments/`. Power users may define custom Dockerfile environments through `workbench envs create` or Workbench Web. Custom Dockerfiles compile down to exact image refs before a command-backed run can start. Command-backed specs must declare `evaluation.environment.with.image`, `evaluation.runner.with.run`, and `evaluation.grader`; skill and pipeline runners do not require an OCI environment unless a command proposer, runner, grader, or variant is present.
