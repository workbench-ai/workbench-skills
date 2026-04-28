---
name: pipelines-cli
description: >-
  Use this skill whenever the user wants to validate, dry-run, or execute
  standalone pipeline YAML or JSON files with the `pipelines` CLI without
  Flow repo initialization, a persistent Flow runtime, durable execution ids,
  continuation state, rerun state, inspection state, or server targeting.
  Trigger for requests like "run this pipeline file", "validate this
  PipelineSpec", "execute pipeline yaml", "run a one-shot pipeline", or
  "use pipelines".
---

# Pipelines CLI

Use the `pipelines` CLI for direct local one-shot execution of standalone pipeline specs. This is not the Flow CLI: do not run `flow init`, do not start a Flow runtime, and do not translate standalone pipeline requests into `.flow/workflows`.

## CLI Availability

Verify the binary before using it:

```bash
pipelines --version
```

If the command is missing, install the published package from GitHub Packages:

```bash
npm config set @workbench-ai:registry https://npm.pkg.github.com
npm install -g @workbench-ai/pipeline-cli
pipelines --version
```

If npm reports a GitHub Packages auth or registry error, tell the user that npm needs `@workbench-ai` GitHub Packages access with a token that can read packages, then stop cleanly instead of falling back to Flow.

## Working Rules

- Use `pipelines validate` before `pipelines run` unless the user explicitly asks to skip validation.
- Use exactly one spec source: `--file PATH` for YAML or `.json` files, or `--stdin` for YAML or JSON from stdin.
- Use `--schema-only` only for structural validation when repo readiness, harnesses, or secrets are intentionally unavailable.
- Treat `pipelines run --dry-run` as the readiness preflight before mutation.
- Default to `--mode scratch`; use `--mode project` only when the user explicitly wants side effects in the target repo.
- Use `--repo PATH` for readiness checks and runs. Do not use `--server`.
- For payloads, use repeated `--input key=value`, exactly one `--payload-json`, or exactly one `--payload-file PATH`.
- Use `--payload-file -` when raw JSON payloads should come from stdin.
- Prefer `--json` when another tool or agent needs structured output.
- Do not use removed Flow-owned pipeline flags such as `--pipeline-file`, `--pipeline-stdin`, or `--pipeline-json`.

## Common Flow

```bash
pipelines validate --file pipeline.yaml --repo . --json
pipelines run --file pipeline.yaml --repo . --dry-run --json
pipelines run --file pipeline.yaml --repo . --json
```

For generated specs:

```bash
cat pipeline.yaml | pipelines validate --stdin --repo . --json
cat pipeline.yaml | pipelines run --stdin --repo . --json
```

For an intentional in-place run:

```bash
pipelines run --file pipeline.yaml --repo . --mode project --json
```

## JSON Output

For `pipelines validate --json`, read `success`, `schema_valid`, `readiness_checked`, `pipeline_id`, `workspace_mode`, `stage_ids`, `harnesses`, and `errors`.

For `pipelines run --json`, read `status`, `terminal_reason`, `workspace_path`, `final_output`, `trace.summaries[]`, and `harness_events`.

Do not treat provider stderr or tool-level error spans as terminal unless the top-level `status` or stage summary failed.

## Local References

- Read [references/docs/cli.md](references/docs/cli.md) for the canonical command contract. In the authored repo tree, the same content lives under `docs/cli.md`.
- Use [references/docs/examples/pipelines](references/docs/examples/pipelines) for standalone pipeline examples.
- Use [evals/evals.json](evals/evals.json) and [evals/README.md](evals/README.md) when improving this skill's product-local eval surface.

