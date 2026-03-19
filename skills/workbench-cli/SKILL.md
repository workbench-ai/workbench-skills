---
name: workbench-cli
description: >-
  Use this skill whenever the user wants to work with Workbench through the
  `workbench` CLI: bootstrap or repair a repo-local `.workbench`, install
  starters, author or validate workflow YAML, start or
  inspect the repo-local runtime, run or resume or watch workflow executions,
  inspect execution state or artifacts, or troubleshoot CLI install, auth, repo
  resolution, or server targeting. Trigger even when the user asks in repo
  terms like "set up Workbench here", "install the template", "why won't
  validate pass", "run this workflow", "resume this execution", or "show what
  executions exist".
---

# Workbench CLI

Use the `workbench` CLI instead of hand-creating `.workbench`, editing `.gitignore` manually, or guessing at runtime API calls.

Treat this file as the thin agent-facing wrapper. The synced references and examples are the source of truth for exact behavior and syntax.

If you are reading the authored repo copy under `skills/workbench-cli`, the generated `references/` and `examples/` folders may not exist yet. In that case, use the canonical repo files under `docs/cli.md`, `docs/workflow-authoring.md`, and `docs/examples/workflows/`. In the public install surface, those same materials live in `workbench-ai/workbench-skills` under `skills/workbench-cli/`.

## Working Rules

- Prefer the repo-local flow. Run the CLI from the target git repo unless the user intentionally wants `--server` or `WB_SERVER_URL`.
- For bootstrap, prefer `workbench init . --template <starter>` over manually creating `.workbench` or copying starter YAML.
- After workflow edits, run `workbench validate`. Use `--schema-only` only when the user explicitly wants structural validation without local readiness checks.
- For read-only inspection, prefer the CLI surfaces that already exist: `workbench workflow list`, `workbench execution list`, `workbench execution show`, `workbench execution history`, `workbench execution trace`, `workbench execution transcript`, and `workbench execution changes`.
- For `execution run`, `execution resume`, `execution action run`, and `execution watch`, ensure a persistent runtime exists with `workbench start` or `workbench open` unless the user intentionally passed an explicit server target.
- Let `execution run`, `execution resume`, and `execution action run` surface missing-input requirements instead of inventing separate input-discovery commands.
- Native chat is outside the CLI surface. Use the web `/chat` route or the runtime `/api/v1/chat/*` API for native chat threads.
- Do not use deleted commands such as `workflow template ...`, `workflow inputs`, `execution continue`, or `execution action inputs`.

## Local References

- Read [references/commands.md](references/commands.md) for the canonical CLI guide, exact syntax, installation notes, runtime lifecycle rules, and server-target resolution. In the authored repo tree, the same content lives in `docs/cli.md`.
- Read [references/workflow-authoring.md](references/workflow-authoring.md) only when you need the workflow contract itself. In the authored repo tree, the same content lives in `docs/workflow-authoring.md`.
- Use the checked-in starter workflows under [examples/workflows](examples/workflows) only as reference material or when the user explicitly wants a raw workflow file; otherwise prefer `workbench init . --template <starter>`.
- For a continuable workflow example, see [examples/workflows/interactive-conversation.yaml](examples/workflows/interactive-conversation.yaml). It uses `state.on_attempt.completed: waiting_for_input`, `stages[].session: resume`, and later turns continue through the same execution id.
- Do not overwrite an existing template install or public skill install unless the user explicitly asked to replace it.
