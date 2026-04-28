## Pipelines CLI Product-Local Eval Suite

This directory holds the product-local ergonomics catalog for the `pipelines-cli` skill.

Tasks here stay scoped to standalone pipeline specs and the `pipelines` binary. They may cover validation, dry-run readiness, one-shot execution, payload handling, and scratch-versus-project workspace selection. They must not require Flow runtime commands, durable Flow executions, hosted Workbench, FactSet, browser automation, or any other cross-product skill.

The product-local proof loop is:

- `pnpm cli-skill-evals:validate` for catalog shape and latency-target checks
- deterministic package tests under `packages/pipeline` and `packages/cli`
- a live temp-repo `pipelines validate` plus `pipelines run` proof when changing command behavior

