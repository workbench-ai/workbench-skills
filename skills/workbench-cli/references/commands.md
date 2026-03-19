# Workbench CLI

The publishable CLI package is `@workbench-ai/workbench`, published privately from `https://github.com/workbench-ai/workbench-control` to GitHub Packages. Installing that package still exposes the repo-scoped shell command `workbench`. The CLI is optimized for the common repo automation path: bootstrap a repo, install one starter, validate YAML, run a workflow, resume a waiting execution, and inspect the result. For the workflow YAML contract itself, use `docs/workflow-authoring.md`; this file is only about CLI behavior.

## Private Install And npx

Authenticate npm to GitHub Packages for the `@workbench-ai` scope before trying to install or execute the CLI. The repository-level `.npmrc` already maps that scope to `https://npm.pkg.github.com`; users still need to provide credentials in their own npm config or environment. On a machine outside this repo, add the scope mapping to the user's own `~/.npmrc`.

`GITHUB_PACKAGES_TOKEN` here is only the environment variable name. The value should normally be a GitHub personal access token (classic). For install and `npx`, that token needs `read:packages`. For publishing, it also needs `write:packages`.

GitHub web login, `git push` auth, and npm registry auth are separate. `npm install -g @workbench-ai/workbench` and `npx @workbench-ai/workbench ...` still require npm auth unless that registry token is already configured in npm.

Typical user `~/.npmrc` entries are:

```ini
@workbench-ai:registry=https://npm.pkg.github.com
//npm.pkg.github.com/:_authToken=${GITHUB_PACKAGES_TOKEN}
always-auth=true
```

Once authenticated, the normal private install and run flows are:

```bash
npm install -g @workbench-ai/workbench
workbench doctor
```

```bash
npx @workbench-ai/workbench doctor
```

The package name is scoped for GitHub Packages, but the executable command stays `workbench`.

## Publishing

Maintainers publish the package family under `packages/` to GitHub Packages. The private CLI release is not a single-package publish: the repo ships `@workbench-ai/contracts`, `@workbench-ai/harness-sdk`, `@workbench-ai/platform-sdk`, `@workbench-ai/client`, `@workbench-ai/runtime`, `@workbench-ai/harness-openai-codex`, `@workbench-ai/harness-anthropic-claude-code`, `@workbench-ai/platform-local`, and `@workbench-ai/workbench` together under one shared release version.

Before publishing:

- bump the shared version across the publishable `packages/*/package.json` family
- run `pnpm publish:local`

`pnpm publish:local` is the canonical maintainer entrypoint. It resolves GitHub Packages auth in this order:

- `NODE_AUTH_TOKEN`
- `GITHUB_PACKAGES_TOKEN`
- `GITHUB_TOKEN`
- the current `git credential` helper entry for the `origin` host

The script writes a temporary npm user config for `https://npm.pkg.github.com`, runs `npm whoami`, then runs the publish guard, build, test, and publish steps in order. No token is stored in tracked files. A fully published release still requires a new shared version bump before the workflow will run again, but a partially published release can be retried safely because already-published packages at the current version are skipped.

If npm auth is already configured separately, `pnpm publish:github` remains available as the low-level publisher. The guard enforces the shared lockstep release instead of a package-by-package manual process: unpublished packages are published at the current shared local version, while already-published packages require that shared local version to be higher than their highest published version before the workflow will proceed. If a publish partially succeeds, rerunning the same command is safe: already-published packages at the current release version are skipped and only the remaining packages are published.

## Command Model

The CLI is repo-first, but runtime lifetime is explicit.

- Repo-local setup and maintenance commands: `start`, `open`, `status`, `ps`, `close`, `init`, `template list`, `validate`, `skill install`, and `doctor`
- Runtime-backed read commands: `workflow list`, `execution list`, `execution show`, `execution history`, `execution trace`, `execution changes`, `execution preview`, and `execution transcript`
- Runtime-backed execution-mutating commands: `execution run`, `execution resume`, `execution action run`, and `execution watch`

Use the lifecycle commands directly:

- `workbench start` starts or reuses a persistent repo-local runtime in the background and prints its URL.
- `workbench open` starts or reuses that same persistent runtime, opens the browser, and prints its URL.
- `workbench status` reports whether the repo currently has a local runtime owner, its mode, pid, and whether it serves the bundled UI.
- `workbench ps` lists currently running local persistent and dev-server runtimes across repos.
- `workbench close` stops that local runtime and refuses by default if it still has active work.

Persistent local runtimes do not self-retire anymore. They stay up until you stop them with `workbench close`, terminate the owning process, or reboot the machine.

`workbench ps` is discovery-only. It does not start or attach to runtimes. Instead it enumerates a small running-runtime registry under `${WB_HOME}/running-runtimes`, validates each candidate against the repo-local lock under `.workbench/runtime/instance-lock` plus `/api/v1/status`, and prunes stale records automatically. Transient read-only runtimes used for inspection commands are intentionally excluded from that registry, so `ps` stays focused on durable user-visible runtimes.

Runtime-backed commands resolve their target in this order:

1. `--server URL`
2. `WB_SERVER_URL` from the process environment
3. if inside a git repo, attach to a healthy repo-local owner recorded under `.workbench/runtime/instance-lock`
4. if inside a git repo and the command is read-only, run against a transient read-only local runtime
5. otherwise fail and require a persistent local runtime or an explicit server target

If `WB_SERVER_URL` is present in the process environment but blank, the CLI fails fast instead of silently falling through to local runtime resolution. Outside a git repo, runtime-backed commands therefore require an explicit server target. The CLI does not fall back to `http://127.0.0.1:4318` implicitly. Use `WB_SERVER_URL` or `--server URL` only when you intentionally want to target an already running Workbench server.

Read-only inspection commands do not leave a background process behind. When no local runtime is already running, they use a transient read-only runtime only for the lifetime of that command. Execution-mutating commands do not auto-start a hidden helper. If no repo-local runtime is already running, they fail and tell you to run `workbench start` or `workbench open`, or to pass `--server URL`.

- `open`, `init`, `skill install`, and `doctor` accept an optional repo path.
- `validate` accepts an optional target path, which may be a workflow file, a workflow directory, or a repo root.
- If a repo-local command omits its path, Workbench walks upward from cwd until it finds a git root.
- Non-git directories are rejected.

`workbench validate` is more ergonomic than the other repo-local commands because it understands both workflow directories and nested repo paths:

- if the target is a workflow file, it validates that file
- if the target directory contains direct `*.yaml` files, it validates that directory as one collection
- if the target directory is inside a git repo but does not contain direct YAML files, it falls back to that repo's `.workbench/workflows`

`workbench init [repo]` creates only the minimal scaffold:

- `.workbench/`
- `.workbench/workflows/`
- `.gitignore` entries for `.workbench/queue`, `.workbench/runtime`, and `.workbench/executions`

If you pass `--template TEMPLATE`, `init` installs exactly one bundled starter workflow into `.workbench/workflows/`. Existing files are not overwritten unless `--force` is also passed.

`workbench start [repo]` performs the same bootstrap step first, then starts or reuses the persistent repo-local runtime and bundled web UI for that repo. `workbench open [repo]` does the same thing and also opens the browser. Before any server starts listening, the runtime owner claims the repo-local lock under `.workbench/runtime/instance-lock`. When no `--port` is passed, the CLI asks the operating system for a free local port and prints the actual bound URL. On first start the runtime also materializes `.workbench/runtime/`, `.workbench/queue/`, `.workbench/executions/`, and `.workbench/runtime/schema.json`. If you pass `--port` and another owner is already serving that repo on a different port, `start` and `open` fail instead of pretending the requested port was used.

List running local runtimes across repos:

```bash
workbench ps
workbench ps --json
```

## Quick Start

Bootstrap a repo and install one starter workflow:

```bash
workbench init . --template codex-review-loop
```

See available starters:

```bash
workbench template list
```

Validate workflow YAML:

```bash
workbench validate
```

List runnable workflows from the repo:

```bash
workbench workflow list
```

Start a persistent local runtime once for execution-creating commands:

```bash
workbench start .
```

Run a workflow:

```bash
workbench execution run codex-review-loop --input reviewer_feedback=ready
```

Resume a waiting, non-terminal workflow execution whose latest attempt completed into a continuation state:

```bash
workbench execution resume exec_123 --input reviewer_feedback="follow up"
```

Native chat is not part of the CLI surface. Start native chat from the web `/chat` route or through the runtime `/api/v1/chat/*` API.

Open the same-origin UI when you want the browser:

```bash
workbench open .
```

## Templates

`workbench template list` is the only template discovery command.

```bash
workbench template list
workbench template list --json
```

Template installation is part of bootstrap, not a separate command family:

```bash
workbench init . --template hook-only-deterministic
workbench init . --template codex-review-loop --force
```

## Validate After Editing YAML

Run validation after every workflow edit:

```bash
workbench validate
```

By default the CLI checks both:

- structural validity of the YAML
- readiness in the current local platform

That means a workflow can be reported as structurally valid but still fail `workbench validate` when its harness is unavailable or its harness-specific local auth or readiness check fails.

Use schema-only mode when you want the same structural answer used by Monaco and the server save path:

```bash
workbench validate --schema-only
```

Or validate one file directly:

```bash
workbench validate .workbench/workflows/review.yaml
```

Validate checked-in examples without requiring local harness auth:

```bash
workbench validate docs/examples/workflows --schema-only
```

## List Workflows

`workflow list` is the only workflow-management command exposed by the CLI.

```bash
workbench workflow list
workbench workflow list --json
workbench workflow list --server http://127.0.0.1:4318
```

`workflow list` returns every workflow record the runtime exposes. Text mode prints the workflow name, id, load status, and enabled state.

## Run, Resume, And Inspect Executions

Most execution commands manage workflow-owned executions only. Native chat threads are intentionally excluded from `execution list`, and chat-owned execution ids are rejected with a redirect to the web `/chat` flow or the runtime chat API. `execution delete` is the one exception: it can hard-delete any stored terminal execution id, including a chat thread, as long as you pass `--yes`.

When no explicit server is configured, runtime-backed CLI commands first attach to the current healthy repo-local owner if one exists. Read-only inspection commands can otherwise use a transient read-only runtime. For `execution run`, `execution resume`, `execution action run`, and `execution watch`, start a persistent repo-local runtime first or pass `--server URL`:

```bash
workbench start .
```

List executions:

```bash
workbench execution list
workbench execution list --workflow-id codex-review-loop
```

Create an execution with resolved manual inputs:

```bash
workbench execution run codex-review-loop --input reviewer_feedback=ready
```

Create an execution with a raw JSON payload:

```bash
workbench execution run codex-review-loop --payload-json '{"reviewer_feedback":"ready"}'
```

Resume a waiting execution:

```bash
workbench execution resume exec_123 --input reviewer_feedback="follow up"
```

`execution resume` resolves continuation inputs from the execution's recorded workflow definition, not from the current workflow file. Saved workflow edits therefore affect new executions immediately but do not rewrite an already waiting execution.

Follow immediately:

```bash
workbench execution run codex-review-loop --follow transcript
```

Inspect execution state and artifacts:

```bash
workbench execution show exec_123
workbench execution history exec_123
workbench execution trace exec_123
workbench execution changes exec_123
workbench execution preview exec_123 notes.md --view raw
workbench execution transcript exec_123
workbench execution watch exec_123 --follow transcript
```

`execution show` keeps workflow provenance minimal. When the current saved workflow no longer matches the execution's recorded definition, it prints one short note telling you that the execution is using its recorded workflow definition and that starting a new execution is how to use current workflow changes.

Reprocess stored canonical traces for older executions:

```bash
workbench execution reprocess exec_123
workbench execution reprocess --all
```

`execution reprocess` is local-only. It rebuilds `snapshot.trace` from the persisted per-stage adapter event files already stored under `.workbench/executions/.../stage-runs/...`, replays only the generic canonical notification methods, asks the installed local harness packages to interpret provider-specific replay envelopes, repairs same-run lifecycle ordering by timestamp plus phase, and rewrites `snapshot.json` in place without touching `events.ndjson`.

Cancel an execution:

```bash
workbench execution cancel exec_123
```

Delete a terminal execution:

```bash
workbench execution delete exec_123 --yes
workbench execution delete exec_chat_123 --yes --json
```

Deletion is permanent. It removes `.workbench/executions/<id>` and any managed workspace or managed chat worktree owned by that execution. Project-mode executions delete only the execution record and leave the repo checkout untouched. The runtime rejects deletion for non-terminal executions with HTTP `409`, and the CLI intentionally requires `--yes` instead of prompting interactively.

### Input Ergonomics

There are no standalone `workflow inputs`, `execution continue`, or `execution action inputs` commands.

Instead:

- `execution run` resolves manual inputs internally
- `execution resume` resolves continuation inputs internally from the execution's recorded definition
- `execution action run` resolves action inputs internally

If required inputs are missing, the CLI fails with a readable missing-input summary that includes each input's label, id, type, required state, defaults, and select options when present.

### Payload Rules

`execution run` and `execution resume` accept either:

- repeated `--input key=value` flags for resolved inputs, or
- exactly one raw JSON source: `--payload-json`, `--payload-file`, or stdin

Do not mix raw JSON sources with `--input` values.

`--json` cannot be combined with `--follow`.

## Actions

List available actions for a waiting execution:

```bash
workbench execution action list exec_123
```

Run an action:

```bash
workbench execution action run exec_123 approve_review --confirm --input approval_mode=ready_to_ship
```

`execution action run` resolves action inputs internally and uses defaults when available. `--json` cannot be combined with `--follow`.

## Workbench Home

Cross-repo defaults live under `WorkbenchHome`, which defaults to `~/.workbench` and is overrideable with `WB_HOME`.

- `${WB_HOME}/.env` is the fallback env file for repo-scoped auth lookups.
- `${WB_HOME}/workspaces` is the default managed execution-workspace root.

Repo-local runtime ownership is not stored in `WorkbenchHome`. It lives under `.workbench/runtime/instance-lock` inside the target repo so every local entrypoint for that repo coordinates on the same owner record.

Env precedence is always:

1. target repo `.env`
2. `${WB_HOME}/.env`
3. process environment

`WB_RUNTIME_URL` follows that same repo `.env` then `${WB_HOME}/.env` then process-environment precedence. When set, Workbench trims whitespace plus trailing slashes and uses the result as the canonical self URL exposed by the runtime.

## Bundled Skill

`workbench skill install` installs the canonical `workbench-cli` skill for LLMs. The authored `SKILL.md` is intentionally thin and routes the agent to the canonical references instead of restating command behavior. The installed skill tree contains:

- destination: `.agents/skills/workbench-cli` in the target repo
- this file as `references/commands.md`
- `docs/workflow-authoring.md` as `references/workflow-authoring.md`
- the same bundled starter workflow YAML files used by `workbench template list` and `workbench init --template ...`
- a small `evals/evals.json` seed for regression-testing or improving the skill itself

Maintainers can also export that same installable skill payload to the generated public `workbench-ai/workbench-skills` repository. The root commands are:

- `pnpm skills:public:build` to regenerate `.workbench/public-skills/workbench-skills`
- `pnpm skills:public:validate` to run upstream `skills-ref validate`, `skills add --list`, and a temp-repo install smoke test against that generated repo
- `pnpm skills:public:publish` to require a clean source worktree, rebuild the generated repo, and push it to `WORKBENCH_SKILLS_PUBLIC_REPO_URL` or the default `https://github.com/workbench-ai/workbench-skills.git` on `WORKBENCH_SKILLS_PUBLIC_BRANCH` or `main`

That public generated repo is the supported GitHub-shorthand install surface for generic `skills` users:

```bash
npx skills add workbench-ai/workbench-skills --skill workbench-cli
```

For exact syntax, use `workbench --help`, `workbench template --help`, `workbench workflow --help`, `workbench execution --help`, `workbench execution action --help`, and `workbench skill --help`.
