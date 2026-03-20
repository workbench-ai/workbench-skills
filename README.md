# Workbench Skills

A collection of public skills for AI coding agents working with Workbench.

Skills follow the [Agent Skills](https://agentskills.io) format.

## Available Skills

### factset-cli

Discover and run FactSet API operations through the `factset` CLI.

Use when:

- Looking up fundamentals, estimates, prices, filings, events, or news through FactSet
- Finding the right FactSet API family and request shape from a business question
- Running a concrete `factset` command and summarizing the result clearly

### workbench-cli

Bootstrap, validate, run, inspect, and troubleshoot Workbench through the `workbench` CLI.

Use when:

- Setting up Workbench in a git repo
- Installing starter workflows and validating YAML
- Running, resuming, and inspecting workflow executions

## Installation

```bash
npx skills add workbench-ai/workbench-skills --skill factset-cli
npx skills add workbench-ai/workbench-skills --skill workbench-cli
```

## Usage

Skills are automatically available once installed. The agent will use them when relevant tasks are detected.

The agent will pick the right installed skill when the task matches its trigger description.

## Skill Structure

Each skill contains:

- `SKILL.md` - Instructions for the agent
- `references/` - Supporting documentation loaded as needed
- `examples/` - Example workflow files and starter material
- `evals/` - Regression prompts for improving the skill
