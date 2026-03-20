# FactSet CLI

The `factset` CLI is a spec-first Node.js command line tool for discovering and calling FactSet APIs through checked-in OpenAPI specs and direct HTTP execution. It is designed so the user does not need to know the API family, operation name, or request shape in advance.

This file is the canonical command reference for the general `factset-cli` skill. The tracked skill source under `skills/factset-cli` is intentionally thin and points here instead of restating the full command surface.

## Install

Node.js 18+ is required.

For local development from this repo:

```bash
npm install
npm run build
node dist/cli.js list
```

To install the CLI globally from GitHub Packages:

```bash
npm install -g @workbench-ai/factset-cli@0.0.3
factset list
```

## Auth

The CLI automatically loads a local `.env` file from the current directory or a parent directory.

Preferred OAuth config:

```dotenv
FACTSET_APP_CONFIG=/absolute/path/to/app-config.json
```

API key fallback:

```dotenv
FACTSET_USERNAME=YOUR-SERIAL
FACTSET_API_KEY=YOUR-API-KEY
```

`factset refresh` uses OAuth when `FACTSET_APP_CONFIG` is available. With API-key-only auth, `refresh` still regenerates repo-local generated skills but skips spec downloads.

## Command Model

The CLI is API-first and intentionally small:

```bash
factset list
factset <api>
factset <api> <operation> --help
factset <api> <operation> --example
factset <api> <operation> --template[=full]
factset <api> <operation> --schema
factset <api> <operation> --input JSON|@file [--set dotted.path=json]
factset refresh
factset doctor
```

The normal discovery flow is:

```bash
factset list
factset <api>
factset <api> <operation> --help
factset <api> <operation> --example > request.json
factset <api> <operation> --input @request.json
```

The CLI does not invent cross-API top-level categories. It preserves the natural API families from the cached specs, such as `fundamentals`, `events`, `global-prices`, `streetaccount-news`, and `global-filings`.

## Core Behaviors

`factset list` shows the available API families.

`factset <api>` is the landing page for one API family. It prints the title, summary, source URLs, recommended operations, request previews, and grouped operations.

`factset <api> <operation> --help` is the default way to learn an operation. It prints:

- the HTTP method and path
- the normalized input mode (`none`, `params`, `body`, or `body + params`)
- accepted top-level input keys
- required and optional params
- body-field outlines
- minimal input and example input
- exact next-step commands

`factset <api> <operation> --example` prefers concrete OpenAPI examples when available.

`factset <api> <operation> --template` prints the minimal valid input shape.

`factset <api> <operation> --template=full` includes useful optional fields derived generically from the spec, such as pagination, date ranges, sort fields, and attribute lists when they exist.

For body-only endpoints, the CLI accepts the request body object directly instead of generated wrapper names from code-generated SDKs.

For mixed endpoints, the accepted input shape is:

```json
{
  "body": { "...": "..." },
  "queryOrPathParam": "value"
}
```

## Examples

Discover and inspect filings:

```bash
factset global-filings
factset global-filings filings --help
factset global-filings filings --example > request.json
factset global-filings filings --input @request.json
```

Get a body template for fundamentals:

```bash
factset fundamentals fundamentals-list --template=full
```

Call a metadata endpoint with no body:

```bash
factset global-filings sources
```

Inspect a schema directly when help and examples are not enough:

```bash
factset events timezone --schema
```

Override small fields without editing a file:

```bash
factset fundamentals fundamentals-list \
  --input @request.json \
  --set data.ids='["AAPL-US","MSFT-US"]'
```

## Error Interpretation

Common failures should be read this way:

- `403 Forbidden`: credentials worked, but the account is probably not entitled for that endpoint
- `401 Unauthorized`: credentials were rejected or missing
- missing input: rerun the operation with `--help`, then `--example` or `--template=full`
- ambiguous alias: rerun `factset <api>` and choose one explicit recommended alias
- `400` on a date-bounded series: retry a later or narrower range and report the earliest successful coverage you actually verified
- `503 Service Unavailable`: the endpoint is unstable right now; try the closest sibling API family only if the user asked for the business result rather than a specific endpoint

`factset doctor` is the local environment check. It reports the resolved `.env` path, auth mode, cached spec count, and a simple live probe recommendation.

## Skill Use

The general skill is installed as `factset-cli`. Once installed, it should use this command flow:

```bash
factset <api>
factset <api> <operation> --help
factset <api> <operation> --example
factset <api> <operation> --input @request.json
```

The skill should start from the business question, not from an API guess, and it should always report exact identifiers, filters, and absolute dates for time-sensitive results.
