---
name: factset-cli
description: Use this skill whenever the user wants FactSet data or wants to use the local `factset` CLI, even if they do not know the API family, operation name, or request shape.
---

# FactSet CLI

Use the `factset` CLI to discover, inspect, and run FactSet API operations instead of guessing API names, request bodies, or raw HTTP routes.

Treat this file as the thin agent-facing wrapper. The synced references are the source of truth for exact command syntax and request-shape guidance.

If you are reading the authored repo copy under `skills/factset-cli`, the `references/` folder may not exist yet. In that case, use the canonical repo file at `docs/cli.md`. In the public install surface, that same content lives under `workbench-ai/workbench-skills/skills/factset-cli/references/commands.md`.

## Working Rules

- Start from the user’s business question, not from an API guess.
- Use `factset list`, then `factset <api>`, then `factset <api> <operation> --help` before falling back to raw schema inspection.
- Prefer `--example` over `--template`, and prefer `--template=full` over reading raw OpenAPI when you still need more input detail.
- Use the narrowest operation that directly answers the question.
- Report exact commands, identifiers, filters, and absolute dates for time-sensitive results.
- If a request needs input and none was provided, use the CLI’s missing-input guidance instead of inventing your own request shape.
- Treat `403 Forbidden` as an entitlement hint unless the response clearly says auth failed.

## Local References

- Read [references/commands.md](references/commands.md) for the canonical CLI guide, input-shape conventions, examples, and common error handling. In the authored repo tree, the same content lives in `docs/cli.md`.
- Use [evals/evals.json](evals/evals.json) as regression prompts when improving the skill.
- Do not use the generated per-API helper skills under `generated/skills/factset-*` as the primary interface. The public install surface is the single general `factset-cli` skill.
