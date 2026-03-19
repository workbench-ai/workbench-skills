# Workbench Skills

A collection of public skills for AI coding agents working with Workbench.

Skills follow the [Agent Skills](https://agentskills.io) format.

## Available Skills

### workbench-cli

Bootstrap, validate, run, inspect, and troubleshoot Workbench through the `workbench` CLI.

Use when:

- Setting up Workbench in a git repo
- Installing starter workflows or the bundled Workbench skill
- Authoring or validating workflow YAML
- Starting the local runtime or inspecting executions
- Resuming waiting executions and reviewing traces or transcripts

## Installation

```bash
npx skills add workbench-ai/workbench-skills --skill workbench-cli
```

## Usage

Skills are automatically available once installed. The agent will use them when relevant tasks are detected.

Examples:

```text
Set up Workbench in this repo
Validate this workflow and tell me how to run it locally
Resume this waiting execution and show me the trace
```

## Skill Structure

Each skill contains:

- `SKILL.md` - Instructions for the agent
- `references/` - Supporting documentation loaded as needed
- `examples/` - Example workflow files and starter material
- `evals/` - Regression prompts for improving the skill
