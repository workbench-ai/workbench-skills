# Testing

Use the product root from `products/workbench-cli`.

Root workspace commands live in [`../../../CONTRIBUTING.md`](../../../CONTRIBUTING.md), and the shared public-skills maintainer flow lives in [`../../../PUBLIC_SKILLS.md`](../../../PUBLIC_SKILLS.md).

## Core Validation

The always-on product validation surface is:

- `pnpm build`
- `pnpm lint`
- `pnpm test`
- `pnpm test:e2e`
- `pnpm cli-skill-evals:validate`

These commands exercise the shared local/hosted CLI, contract, runtime, UI helpers, docs, and skill packaging surfaces.
Runtime tests include deterministic coverage for generic execution planning, scoped capabilities, provider endpoint allowlists, Firecracker network/boot planning, profile-owned sandbox-host health policy, and in-sandbox adapter runner validation. Docker reports only `none` and `open` network capability; allowlist enforcement belongs to Firecracker. Local hosted smoke uses the `sandbox-host-local.mjs` and `dispatcher-local.mjs` entrypoints, and full Firecracker VM execution is covered by production smoke through the `sandbox-host-prod.mjs` and `dispatcher-prod.mjs` entrypoints.
When the local Docker backend runs a repo-owned Workbench built-in image ref such as `docker://workbench/workbench-python-3.12:envv_python_3_12`, it seeds the exact image from `products/workbench-cli/environments/` if the tag is not already present.

Useful manual spot checks:

- `pnpm exec workbench --help`
- `tmpdir=$(mktemp -d); pnpm exec workbench init "$tmpdir" --json`
- `pnpm exec workbench check --dir "$tmpdir" --json`
- `pnpm exec workbench dev improve --dir "$tmpdir" --budget 1 --samples 2 --json`
- `pnpm exec workbench launch --help`
- `pnpm exec workbench sync --help`
- `pnpm exec workbench eval --help`
- `pnpm exec workbench improve --help`
- `pnpm exec workbench compare --help`
- `pnpm exec workbench envs list --help`
- `pnpm exec workbench envs create --help`
- `pnpm exec workbench candidates pull --help`
- `pnpm exec workbench --version`

## Hosted E2E

Start Workbench Web locally:

```bash
docker rm -f workbench-runtime-registry || true
docker run -d --name workbench-runtime-registry -p 5050:5000 registry:2
AUTH_SECRET=test-secret \
NEXTAUTH_SECRET=test-secret \
NEXTAUTH_URL=http://127.0.0.1:3000 \
AUTH_COGNITO_CLIENT_ID=local-client \
AUTH_COGNITO_CLIENT_SECRET=local-secret \
AUTH_COGNITO_ISSUER=http://127.0.0.1:3000/local-cognito \
WORKBENCH_WORKER_TOKEN_SHA256="$(printf '%s' local-worker-token | shasum -a 256 | awk '{print $1}')" \
WORKBENCH_BUILDER_TOKEN_SHA256="$(printf '%s' local-builder-token | shasum -a 256 | awk '{print $1}')" \
WORKBENCH_RUNTIME_REGISTRY=127.0.0.1:5050 \
WORKBENCH_ENABLE_DEV_LOGIN=1 \
pnpm --dir ../workbench-web dev
```

With only Workbench Web running, use the CLI for hosted project setup and state
commands:

```bash
WORKBENCH_API_URL=http://127.0.0.1:3000 pnpm exec workbench launch --name smoke --json
WORKBENCH_API_URL=http://127.0.0.1:3000 pnpm exec workbench envs list --json
WORKBENCH_API_URL=http://127.0.0.1:3000 pnpm exec workbench sync --json
```

Commands that execute runs also need the builder, sandbox-host, and runner
dispatcher services. Use the Workbench Web smoke harness for local hosted e2e
coverage; it starts those workers and starts the local Docker sandbox-host
entrypoint:

```bash
AUTH_SECRET=test-secret NEXTAUTH_SECRET=test-secret WORKBENCH_WORKER_TOKEN=local-worker-token WORKBENCH_BUILDER_TOKEN=local-builder-token WORKBENCH_RUNTIME_REGISTRY=127.0.0.1:5050 WORKBENCH_SANDBOX_TEMPLATE_IMAGES='{"workbench/agent-codex:latest":"workbench-web:local","workbench/agent-claude:latest":"workbench-web:local","workbench/agent-pi:latest":"workbench-web:local","workbench/agent-rubric:latest":"workbench-web:local"}' pnpm --dir ../workbench-web smoke:local
```

To run individual hosted execution commands manually, keep the same worker
services running and then call:

```bash
WORKBENCH_API_URL=http://127.0.0.1:3000 pnpm exec workbench eval --samples 1 --watch --json
WORKBENCH_API_URL=http://127.0.0.1:3000 pnpm exec workbench improve --budget 1 --samples 1 --watch --json
WORKBENCH_API_URL=http://127.0.0.1:3000 pnpm exec workbench compare --samples 1 --watch --json
```

For browser validation, open `/workbench` in Workbench Web with an agent browser, create or select the same project, save the spec, start a run through the hosted API or CLI, then switch through Evaluation, Files, Comparisons, Archive, and Lineage. Verify desktop plus mobile layout and confirm the browser and CLI show the same hosted candidate/run state.

Workbench Web owns the e2e runtime smoke harness for local and remote hosted
testing:

```bash
AUTH_SECRET=test-secret NEXTAUTH_SECRET=test-secret WORKBENCH_WORKER_TOKEN=local-worker-token WORKBENCH_BUILDER_TOKEN=local-builder-token WORKBENCH_RUNTIME_REGISTRY=127.0.0.1:5050 WORKBENCH_SANDBOX_TEMPLATE_IMAGES='{"workbench/agent-codex:latest":"workbench-web:local","workbench/agent-claude:latest":"workbench-web:local","workbench/agent-pi:latest":"workbench-web:local","workbench/agent-rubric:latest":"workbench-web:local"}' pnpm --dir ../workbench-web smoke:local
pnpm --dir ../workbench-web smoke:prod
```

Both modes exercise the same project/environment/spec/snapshot/run/candidate
path through the sandbox-host abstraction. Local smoke runs against a
local Workbench Web server, starts the
builder, sandbox-host, and runner dispatchers, creates and builds a custom
Dockerfile environment, pushes it to `WORKBENCH_RUNTIME_REGISTRY`, and then
runs the eval inside that exact image. If a sandbox host is already running,
set both `WORKBENCH_SANDBOX_HOST_URL` and `WORKBENCH_SANDBOX_HOST_TOKEN`;
that host must have been started through `sandbox-host-local.mjs`.
Otherwise the smoke starts one, starts `dispatcher-local.mjs`, sets
`WORKBENCH_DOCKER_RUNTIME_IMAGE=workbench-web:local` for the local hosted
container-shape proof, and uses `WORKBENCH_SANDBOX_TEMPLATE_IMAGES` as the
template-ref image map for snapshot-based agent adapters. Build or tag those
images before running local smoke.
Production smoke targets `https://v2.workbench.ai`, where Terraform supplies
DynamoDB/S3/SQS state, an S3-backed local OCI registry, and long-lived builder,
queue-runner, and sandbox-host services on the sandbox runner fleet. The runner
fleet starts `sandbox-host-prod.mjs` and `dispatcher-prod.mjs`, which assert the
Firecracker backend with nested virtualization on C8i/M8i/R8i-compatible x86 instances. The
smoke covers hosted `improve`, `eval`, and `compare` workflows through the
generic sandbox-plane contract and proves that execution reaches the sandbox
host rather than the web request path.
Apply the prod Terraform plan before `deploy:prod` whenever launch-template user
data or infrastructure inputs change; `deploy:prod` only publishes the image and
refreshes instances from the already-applied launch templates.
`smoke:prod` reuses the normal
`workbench login` token from `~/.workbench/workbench.json`; set
`WORKBENCH_SMOKE_BEARER_TOKEN` or `WORKBENCH_SMOKE_COOKIE` only when you need to
override auth.

## Release

The guarded release path is:

- `pnpm publish:check-versions`
- `pnpm publish:build`
- `pnpm publish:test`
- `pnpm publish:local`

`pnpm publish:prepare <version>` rewrites the publishable CLI manifest. `pnpm publish:check-versions` compares the package version against GitHub Packages and fails when there is nothing new to publish. `pnpm publish:local` resolves GitHub Packages auth, reruns the guarded build and test steps, and publishes the pending CLI package with `--no-git-checks`.
