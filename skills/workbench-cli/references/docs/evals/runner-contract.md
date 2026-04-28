# Runtime Contract

Workbench version 6 compiles `workbench.yaml` into proposer, runner, and grader executions. Hosted Workbench stores each executable node as one durable `execute` job with a `purpose` of `propose`, `run`, or `grade`.

Proposer executions run once per trial and produce a candidate patch. Built-in proposer adapters such as `optimization.proposer.use: codex` receive archive context and an editable candidate surface.

Command runner and command-grader executions run inside the exact Docker/OCI image named by `evaluation.environment.with.image`. Skill and pipeline runners are agent/template backed and do not require an OCI environment unless a command adapter is also present. Run executions use the `current` candidate path. Comparison jobs can additionally use configured `evaluation.variants` adapters. Command adapters execute in separate runner and grader nodes:

1. `evaluation.runner.with.prepare[]`
2. `evaluation.runner.with.run`
3. runner evidence is persisted
4. `evaluation.grader.with.prepare[]`, for command graders
5. `evaluation.grader.with.run`, for command graders
6. the rubric grader adapter, for rubric graders

The runner produces artifacts or evidence. The grader is required and scores the immutable runner evidence.

Hosted workflows and local `workbench dev` workflows use the same adapter contract for command, skill, and pipeline runners. The sandbox plane runs proposer, runner, and grader adapters behind one execution contract with separate input and output schemas.

## Staged Directories

Every command execution receives these environment variables:

- `WORKBENCH_ARCHIVE_DIR`: materialized run archive with spec, job metadata, current candidate files, cases, state summaries, and evaluation manifests.
- `WORKBENCH_CANDIDATE_DIR`: directory containing the candidate snapshot. Files written here can become part of the resulting candidate.
- `WORKBENCH_CASES_DIR`: directory containing the uploaded case snapshot.
- `WORKBENCH_OUTPUT_DIR`: scratch output directory for phase logs and intermediate evidence.
- `WORKBENCH_RUNNER_OUTPUT_DIR`: optional runner scratch subdirectory.
- `WORKBENCH_GRADER_OUTPUT_DIR`: optional grader scratch subdirectory.
- `WORKBENCH_SPEC_JSON`: JSON version of the resolved spec.
- `WORKBENCH_JOB_JSON`: JSON metadata for the current job.
- `WORKBENCH_EXECUTION_PURPOSE`: `run` for runner commands and `grade` for command graders.
- `WORKBENCH_CANDIDATE_ID`: id of the candidate being evaluated.
- `WORKBENCH_TRIAL_INDEX`: zero-based trial index.
- `WORKBENCH_SAMPLE_INDEX`: zero-based sample index.
- `WORKBENCH_VARIANT_ID`: evaluation variant id, usually `current`.

Only `evaluation.grader.with.run` receives `WORKBENCH_REWARD_FILE`, the required grader output JSON path currently inside `WORKBENCH_OUTPUT_DIR`. Runner and grader-prepare phases do not receive the reward path. Workbench deletes any stale reward file immediately before `evaluation.grader.with.run`, so the score must be produced by the required command grader run or by the rubric grader adapter.

Treat `WORKBENCH_CASES_DIR` as read-only evidence. Runner and grader executions should also treat `WORKBENCH_CANDIDATE_DIR` as read-only; any mutation there is ignored for durable candidate materialization. Files under `WORKBENCH_OUTPUT_DIR` become runner evidence or grader traces depending on the execution purpose.

## Reward Boundary

The command grader writes `WORKBENCH_REWARD_FILE`. `score` is required and must be finite.

```json
{
  "score": 0.82,
  "metrics": {
    "score": 0.82,
    "criterion__required_tables": 1
  },
  "summary": "Matched required tables and headings; missed footer formatting.",
  "fileChanges": ["report.docx", "eval-summary.md"],
  "cases": [
    {
      "id": "case-001",
      "status": "passed",
      "metrics": { "score": 0.82 },
      "artifacts": [
        { "id": "summary", "kind": "markdown", "relative_path": "artifacts/case-001-summary.md" }
      ]
    }
  ],
  "feedback": {
    "notes": "Footer was missing."
  }
}
```

Fields:

- `score`: required numeric metric used by `optimization.selection.metric: score`.
- `metrics`: optional additional numeric metrics. Keys prefixed with `criterion__` render as rubric metrics.
- `summary`: optional short human-readable result.
- `fileChanges`: optional relative paths inside `WORKBENCH_CANDIDATE_DIR` that changed or were generated.
- `cases`: optional case-level results, artifacts, logs, feedback, and criterion scores.
- `feedback`: optional structured JSON for diagnostics.

If any phase exits non-zero, Workbench marks the execution failed. Grader executions also fail when `WORKBENCH_REWARD_FILE` is missing a finite `score`.

## Durable Artifacts

If a generated report, normalized text dump, screenshot, workbook, or debug file should be inspectable after the run, write it into `WORKBENCH_OUTPUT_DIR` from the runner and reference it from grader feedback or case artifacts.

For artifact evaluations, a practical pattern is:

1. Runner extracts comparable signals from candidate artifacts into `WORKBENCH_OUTPUT_DIR`.
2. Runner writes durable evidence summaries or generated artifacts into `WORKBENCH_OUTPUT_DIR`.
3. Grader compares runner evidence against cases and rubric criteria.
4. Grader writes `WORKBENCH_REWARD_FILE`.

## Command Shape

Prefer checked-in candidate scripts and explicit prepare hooks:

```yaml
evaluation:
  runner:
    use: command
    with:
      prepare:
        - run: python "$WORKBENCH_CANDIDATE_DIR/scripts/extract.py"
      run: python "$WORKBENCH_CANDIDATE_DIR/scripts/run.py"
  grader:
    use: command
    with:
      prepare:
        - run: python "$WORKBENCH_CANDIDATE_DIR/scripts/build-evidence.py"
      run: python "$WORKBENCH_CANDIDATE_DIR/scripts/grade.py"
```

Use shell glue only for small setup steps. If the evaluator needs packages not present in a built-in runtime, create a custom Dockerfile environment instead of installing dependencies during every evaluation job.
