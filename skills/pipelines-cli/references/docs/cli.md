# Pipelines CLI

The `pipelines` binary is the lightweight direct runner for standalone `PipelineSpec` files. It is published by the `@workbench-ai/pipeline-cli` package. Use it when you have a YAML or JSON pipeline document and want to validate or execute it once without creating durable Flow workflow or execution state.

`pipelines` is local-only. It does not use `flow start`, does not target `--server`, does not write `.flow/workflows`, and does not create `.flow/executions`. The only persisted changes are the side effects produced by the run itself, such as files written by hooks or stages.

## Commands

Validate a pipeline file:

```bash
pipelines validate --file pipeline.yaml --repo . --json
pipelines validate --file pipeline.yaml --schema-only --json
cat pipeline.yaml | pipelines validate --stdin --repo .
```

Run a pipeline once:

```bash
pipelines run --file pipeline.yaml --repo . --dry-run
pipelines run --file pipeline.yaml --repo . --json
pipelines run --file pipeline.yaml --repo . --mode project --input reviewer_feedback=ready
pipelines run --file pipeline.yaml --repo . --mode project --payload-json '{"reviewer_feedback":"ready"}'
printf '{"reviewer_feedback":"ready"}' | pipelines run --file pipeline.yaml --repo . --payload-file - --json
```

Use exactly one spec source:

- `--file PATH` for YAML or `.json` files
- `--stdin` for YAML or JSON piped on stdin

`validate --schema-only` checks only the document structure. Normal `validate`, `run --dry-run`, and `run` also resolve the target git worktree, load local extensions, and check harness readiness, secrets, and runtime capabilities.

## Workspace Modes

`--mode scratch` is the default. It copies the target repo into a disposable workspace and reports that path as `workspace_path`; this is the safer default because the source repo is not mutated.

`--mode project` runs directly against the target repo workspace. Use it when the pipeline is intentionally supposed to write files into that repo.

Default validation and runs require the target path to be a git worktree, but the repo does not need `flow init`, a running Flow runtime, or an existing commit.

## JSON Output

`pipelines run --json` includes:

- `status`
- `terminal_reason`
- `workspace_path`
- `final_output`
- `trace`
- `harness_events`

For multistage runs, use `trace.summaries[]` for concise per-stage status. Stageful first-party harness pipelines can use stage `hooks.after` checks to make file or output expectations explicit; see [`examples/pipelines/codex-multistage-files.yaml`](examples/pipelines/codex-multistage-files.yaml).
