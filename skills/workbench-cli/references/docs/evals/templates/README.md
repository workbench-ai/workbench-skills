# Starter Template

This directory is project-shaped. Copy `workbench.yaml`, `candidate/`, and `cases/` together before adapting the names, `evaluation.environment.with.image`, cases, and scoring logic.

The included evaluator is a smoke test, not a production benchmark. It requires non-empty `cases/*/expected/text.txt`, reads `candidate/outputs/<case-id>.txt` or `candidate/output.txt`, writes `candidate/eval-summary.md`, writes runner evidence in run-only mode, and writes `WORKBENCH_REWARD_FILE` in grade-only mode.
