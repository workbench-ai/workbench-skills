# Skills

This document owns the skill layout for the Workbench CLI product tree.

## Source Of Truth

The canonical general public skill source lives under `skills/workbench-cli/`. Keep that authored tree thin:

- `SKILL.md` is the agent-facing wrapper.
- `agents/openai.yaml` is the install metadata.
- `evals/` is the product-local ergonomics catalog.
- `skill.assets.json` declares which canonical docs are copied into the installed skill.

`docs/cli.md` owns the command and operator flow, `SPEC.md` owns the hosted CLI contract, `docs/evals/` owns eval authoring and artifact-first evaluation creation, and `docs/testing.md` owns validation and hosted e2e guidance. The authored skill should point to those canonical files instead of carrying its own product guide.

## Generated Local Mirror

Run `pnpm skills:sync` from `products/workbench-cli` to refresh `.agents/skills/workbench-cli`.

That command copies the authored `skills/workbench-cli/` tree into the generated install surface, overlays the canonical files declared in `skill.assets.json`, and removes `skill.assets.json` from the generated output.

`.agents/skills/workbench-cli/` is generated output, not authored source. Keep the tracked source of truth under `skills/workbench-cli/`.

## Validation Boundary

This product tree owns `skills.json`, the authored `skills/workbench-cli/` tree, and the product-local eval catalog. `skills.json` also states whether the skill is published to the `workbench-skills` channel. The combined public skill repository, shared assembly tests, and publishing flow are root-owned and documented at [`../../../PUBLIC_SKILLS.md`](../../../PUBLIC_SKILLS.md).

The local proof loop for the authored Workbench skill surface is:

- `pnpm skills:sync`
- `pnpm cli-skill-evals:validate`
- `pnpm test`

The `skills/workbench-cli/evals/` directory is only the skill-ergonomics catalog used to test the public skill. It is not the user-facing guide for Workbench project eval authoring; that guide lives under `docs/evals/`.
