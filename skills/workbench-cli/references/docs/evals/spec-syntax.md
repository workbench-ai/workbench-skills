# Workbench Spec Syntax

Workbench stores one `workbench.yaml` spec per project. The version-6 shape is used by local development and hosted Workbench: `candidate` names the mutable artifact, `optimization` names the proposer adapter and selection rule, and `evaluation` names cases, the runner adapter, required grader adapter, optional OCI environment for command adapters, and optional comparison variants.

Use `workbench check --dir <source-dir>` locally or `workbench sync --project <project-id> --dry-run` before uploading candidate and case snapshots.

## Minimal Shape

```yaml
version: 6
name: artifact-eval
candidate:
  kind: command
  root: candidate
  entry: evaluate-artifacts.py
  editable:
    - evaluate-artifacts.py
optimization:
  goal: Improve the candidate so it satisfies the uploaded cases.
  proposer:
    use: codex
  selection:
    use: greedy
    metric: score
    direction: maximize
evaluation:
  task: Score the candidate against the uploaded artifact cases.
  cases:
    root: cases
  environment:
    use: oci
    with:
      image: docker://workbench/workbench-libreoffice-python:envv_libreoffice_python
  runner:
    use: command
    with:
      run: python "$WORKBENCH_CANDIDATE_DIR/evaluate-artifacts.py" --run-only
  grader:
    use: command
    with:
      run: python "$WORKBENCH_CANDIDATE_DIR/evaluate-artifacts.py" --grade-only
```

## Required Fields

- `version`: must be `6`.
- `name`: short project-readable name.
- `candidate.kind`: `skill`, `pipeline`, or `command`.
- `candidate.root`: uploaded candidate root.
- `candidate.entry`: primary candidate artifact path inside `candidate.root`.
- `candidate.editable`: paths inside the candidate root that the proposer may change.
- `optimization.goal`: success target for proposer, reviewers, and humans.
- `optimization.proposer.use`: proposer adapter, commonly `codex`, `claude`, or `pi`.
- `optimization.proposer.with.model`: optional provider model name.
- `optimization.proposer.with.effort`: optional provider effort setting.
- `optimization.selection.use`: currently `greedy`.
- `optimization.selection.metric`: numeric metric to optimize.
- `optimization.selection.direction`: `maximize` or `minimize`.
- `evaluation.task`: clear evaluation task.
- `evaluation.cases.root`: uploaded case root.
- `evaluation.environment.use`: currently `oci`, required when any command adapter is present.
- `evaluation.environment.with.image`: exact Docker/OCI image reference for command adapters.
- `evaluation.runner.use`: `skill`, `pipeline`, or `command`.
- `evaluation.runner.with`: runner-specific configuration.
- `evaluation.grader`: required command or rubric grader.

Top-level `goal`, `eval`, `runtime`, `runner`, `strategy`, and `variants` are stale and rejected. `candidate.proposer`, `candidate.strategy`, and `candidate.variants` are also stale.

## Optimization

`optimization.proposer` is a sandboxed adapter block. The built-in proposer shape is:

```yaml
optimization:
  goal: Improve the workbook builder while preserving the case contract.
  proposer:
    use: codex
    with:
      model: gpt-5.4
  selection:
    use: greedy
    metric: score
    direction: maximize
```

The proposer produces a candidate patch. Agent provider YAML is deliberately small: `use`, `with.model`, and `with.effort` are public; provider auth and harness config are resolved by the sandbox adapter and are not stored in `workbench.yaml`.

## Evaluation

`evaluation.runner` produces artifacts or evidence. `evaluation.grader` is required and produces comparable metrics. Use `skill` for a candidate skill folder, `pipeline` for a candidate pipeline YAML, and `command` for shell-command execution inside an OCI environment.

Skill runner:

```yaml
evaluation:
  runner:
    use: skill
    with:
      agent: codex
      skill: invoice-review
      promptFile: prompt.md
      output:
        path: skill-output.md
```

Pipeline runner:

```yaml
evaluation:
  runner:
    use: pipeline
    with:
      agent: codex
      file: pipeline.yaml
      output:
        path: pipeline-result.json
```

Command runner:

```yaml
evaluation:
  task: Preserve formulas, pass balance checks, and match the expected workbook layout.
  cases:
    root: cases
  environment:
    use: oci
    with:
      image: docker://workbench/workbench-libreoffice-python:envv_libreoffice_python
  runner:
    use: command
    with:
      prepare:
        - run: python scripts/extract_case_index.py
          cwd: candidate
      cwd: candidate
      env:
        EVAL_MODE: smoke
      run: python scripts/run.py
  grader:
    use: command
    with:
      run: python candidate/scripts/grade.py
```

Built-in image refs for command adapters:

- `docker://workbench/workbench-node-22:envv_node_22`
- `docker://workbench/workbench-python-3.12:envv_python_3_12`
- `docker://workbench/workbench-libreoffice-python:envv_libreoffice_python`

After creating a custom environment, put the exact returned `imageRef` into `evaluation.environment.with.image`.

## Graders

Command graders run inside the evaluation OCI image and `evaluation.grader.with.run` writes `WORKBENCH_REWARD_FILE`. Workbench captures that reward as the grader scorecard output; graders do not mutate durable candidate files.

```yaml
evaluation:
  grader:
    use: command
    with:
      prepare:
        - run: python "$WORKBENCH_CANDIDATE_DIR/scripts/collect_evidence.py"
      run: python "$WORKBENCH_CANDIDATE_DIR/scripts/grade.py"
```

Rubric graders nest the judge agent because an agent is specific to rubric grading:

```yaml
evaluation:
  grader:
    use: rubric
    with:
      judge:
        use: codex
        with:
          model: gpt-5.4
      instructions: Grade only from rendered evidence and runtime traces.
      criteria:
        - id: required_tables
          description: Required tables are present and readable.
          weight: 1
```

Base grader blocks are kind-specific. Command graders may contain only `use` plus `with.prepare`, `with.run`, `with.cwd`, and `with.env`; rubric graders may contain only `use` plus `with.judge`, `with.instructions`, and `with.criteria`. Fields for the wrong grader kind are rejected instead of ignored.

## Variants

Variants are evaluation overlays used for comparison. Hosted and local development improve/eval workflows use the `current` variant for promotion; `workbench compare` and `workbench dev compare` evaluate `current` plus configured variants.

```yaml
evaluation:
  variants:
    strict:
      label: Strict scoring
      runner:
        use: command
        with:
          run: python "$WORKBENCH_CANDIDATE_DIR/scripts/evaluate.py"
          env:
            SCORING_MODE: strict
    fast:
      label: Fast smoke
      runner:
        use: command
        with:
          run: python "$WORKBENCH_CANDIDATE_DIR/scripts/evaluate.py" --smoke
```

Variants provide full runner or grader adapter blocks. Command variants use the same `evaluation.environment` OCI image; skill and pipeline variants do not need an OCI environment. The variant id `current` is reserved for the base evaluation path and cannot be configured.

Every variant must include `runner`, `grader`, or both. Hosted Workbench compiles variants into the same generic `execute` job model as the base runner and grader path.

## Score Direction

`optimization.selection.metric` must match a numeric metric emitted by the grader. Workbench aggregates every finite numeric key in `WORKBENCH_REWARD_FILE.metrics` across samples and selects only by the configured metric; it does not fall back to `score` when that metric is missing. Use `direction: maximize` for reward-like metrics such as `score`; use `direction: minimize` for error rates, distances, failures, or costs.
