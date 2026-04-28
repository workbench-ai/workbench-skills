# Workbench Skills

A collection of public skills for AI coding agents working with products from the Workbench monorepo.

Skills follow the [Agent Skills](https://agentskills.io) format.

## Available Skills

### Pipelines CLI (`pipelines-cli`)

Validate and run standalone pipeline YAML or JSON files with the lightweight `pipelines` CLI.

Use when:

- Running a one-shot pipeline file without Flow repo initialization or durable execution state
- Validating standalone PipelineSpec YAML or JSON from a file or stdin
- Dry-running local harness readiness before executing a pipeline
- Running pipeline side effects in scratch mode or explicitly in the target repo

### Workbench CLI (`workbench-cli`)

Create evals, configure, run, inspect, and export hosted Workbench projects with workbench.

Use when:

- Verifying or installing the published `@workbench-ai/workbench-cli` package before hosted setup
- Authoring Workbench eval specs from existing workflows or artifact examples such as DOCX, XLSX, PDF, and PPTX files
- Creating a hosted Workbench project and linking local source with `workbench launch --name` or `workbench link PROJECT_ID`
- Listing hosted runtime environments and creating project-specific Dockerfile environments with exact image refs
- Uploading spec, candidate, and case snapshots through `workbench sync`
- Starting hosted eval, improve, and compare workflows, watching completion, inspecting candidate files, and exporting selected candidates

## Installation

```bash
npx skills add workbench-ai/workbench-skills --skill pipelines-cli
npx skills add workbench-ai/workbench-skills --skill workbench-cli
```

## Usage

Skills are automatically available once installed. The agent will use them when relevant tasks are detected.

The agent will pick the right installed skill when the task matches its trigger description.

## Skill Structure

Each skill contains `SKILL.md`. Supporting directories such as `references/`, `examples/`, and `evals/` are included only when the authored skill tree or its `skill.assets.json` manifest declares them.
