# Workbench CLI

The `workbench` CLI is cloud-first. Normal commands target hosted Workbench projects; local execution is an explicit development mode under `workbench dev`.

The public model is intentionally small:

- project: one hosted Workbench project
- source directory: local `workbench.yaml`, `candidate/`, and `cases/`
- link: `.workbench/link.json`, which binds a source directory to a hosted project
- artifact: candidate `skill`, `pipeline`, or `command` under `candidate/`
- environment: exact Docker/OCI runtime selected by `evaluation.environment.with.image` for command adapters
- run: a hosted `eval`, `improve`, or `compare` workflow
- candidate: hosted file snapshot that can be inspected, previewed, and pulled

## Install

Node.js 18+ is required.

```bash
workbench --version
```

To install the published CLI from GitHub Packages:

```bash
npm config set @workbench-ai:registry https://npm.pkg.github.com
npm install -g @workbench-ai/workbench-cli
workbench --version
```

GitHub Packages may require npm auth for the `@workbench-ai` scope. A token with `read:packages` is enough for install.

## Commands

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

## Normal Hosted Flow

Create a local source directory, create a hosted project, and link them:

```bash
workbench init --artifact skill --name invoice-review --agent codex
workbench launch --name invoice-eval
workbench status
```

Push the local `workbench.yaml`, `candidate/`, and `cases/` to the linked project:

```bash
workbench sync
```

Run hosted workflows:

```bash
workbench eval --samples 1 --watch
workbench improve --budget 2 --samples 1 --watch
workbench compare --samples 1 --watch
```

Inspect and pull results:

```bash
workbench runs list
workbench candidates list
workbench candidates files <candidate-id>
workbench candidates preview <candidate-id> --path workbench-run-summary.md --output -
workbench pull <candidate-id> --out ./best-candidate
```

Use `--project ID` for one-off hosted targeting or `workbench link PROJECT_ID` to store the project in `.workbench/link.json`.

## Local Development Flow

Use `dev` when iterating without the hosted API:

```bash
workbench init --artifact command --name local-command-eval
workbench check
workbench dev improve --budget 1 --samples 1
workbench dev candidates
workbench dev improve --budget 1 --samples 1
```

Local development commands use `--dir DIR`, not `--workspace`.

## Environments

List built-in and project-specific runtimes:

```bash
workbench envs list
workbench envs list --project <project-id>
```

Create a custom Dockerfile environment:

```bash
workbench envs create --project <project-id> --name invoice-runtime --dockerfile ./Dockerfile --memory-gb 4 --disk-gb 10 --timeout-minutes 20 --network off --json
```

Use the returned ready version `imageRef` as `evaluation.environment.with.image`.

## Auth And API Target

Default login targets the hosted Workbench control plane:

```bash
workbench login
workbench whoami
```

For local Workbench Web development:

```bash
workbench login --base-url http://127.0.0.1:3000 --no-open
WORKBENCH_API_URL=http://127.0.0.1:3000 workbench projects list
```

The CLI resolves the API base URL from `WORKBENCH_API_URL`, then the linked project URL, then the login config, then `https://v2.workbench.ai`.

## Spec And Eval Authoring

Specs remain first-class for power users. The shared local/hosted validator accepts the version-6 adapter-envelope shape: `version: 6`, `name`, `candidate.kind`, `candidate.root`, `candidate.entry`, `candidate.editable`, `optimization.goal`, `optimization.proposer.use`, `optimization.selection.use`, `optimization.selection.metric`, `optimization.selection.direction`, `evaluation.task`, `evaluation.cases.root`, `evaluation.runner`, and required `evaluation.grader`. Command adapters additionally require `evaluation.environment.with.image`; skill and pipeline runners use `evaluation.runner.use: skill` or `evaluation.runner.use: pipeline` with an agent in `with.agent`.

Use [`evals/spec-syntax.md`](evals/spec-syntax.md) for the complete shared YAML shape and [`evals/runner-contract.md`](evals/runner-contract.md) for the proposer, runner, grader, archive, and reward contract. Use [`evals/from-existing-workflow.md`](evals/from-existing-workflow.md) when wrapping an existing benchmark or test command, and [`evals/from-artifacts.md`](evals/from-artifacts.md) when creating an eval from `.docx`, `.xlsx`, `.pdf`, `.pptx`, or similar artifacts.
