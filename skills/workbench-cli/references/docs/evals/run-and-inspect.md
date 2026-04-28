# Run And Inspect

Use this loop after writing `workbench.yaml`, candidate files, and cases.

## Check And Sync

```bash
workbench check
workbench launch --name <project-name>
workbench sync --json
```

If the hosted project already exists, use `workbench link <project-id>` or pass `--project <project-id>` to each hosted command. Fix validation errors before running. If the runtime is custom, confirm the image version is ready before using its exact `imageRef` in `evaluation.environment.with.image`.

## Start Smoke Workflows

Run one sample first:

```bash
workbench eval --samples 1 --watch --json
workbench improve --budget 1 --samples 1 --watch --json
workbench compare --samples 1 --watch --json
```

If the sample fails, inspect the proposer, runner, grader, runtime environment, and `WORKBENCH_REWARD_FILE` writing logic. Most first-pass failures are one of:

- the command path assumes a different working directory
- the configured command grader writes reward JSON somewhere other than `WORKBENCH_REWARD_FILE`
- the result is missing the configured finite numeric selection metric
- the runtime image is missing an artifact parser or renderer
- the evaluator writes durable evidence only to `WORKBENCH_OUTPUT_DIR` instead of `WORKBENCH_CANDIDATE_DIR`

## Inspect The Candidate

```bash
workbench candidates list --json
workbench candidates files <candidate-id> --json
workbench candidates preview <candidate-id> --path eval-summary.md --output -
workbench pull <candidate-id> --out ./best-candidate
```

Use the first run to verify that score direction, case evidence, durable summary files, and candidate file changes are all understandable before increasing budget or samples.
