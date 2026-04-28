# From Existing Workflow

Use this path when the user already has a script, test suite, benchmark command, or manual scoring process. The goal is to wrap that workflow in the Workbench runner/grader contract without changing the workflow more than needed.

## Process

1. Identify the command that already produces candidate artifacts or pass/fail evidence.
2. Put mutable files under the candidate root.
3. Put fixtures, expected outputs, and case metadata under the cases root.
4. Write a runner that executes the existing workflow and writes evidence.
5. Write a required grader that reads the evidence and writes `WORKBENCH_REWARD_FILE`.
6. Validate the spec, upload snapshots, and run one sample.

## Adapter Pattern

The runner can preserve the existing command. The grader translates its result into Workbench reward JSON:

```python
import json
import os
import subprocess
from pathlib import Path

candidate_dir = Path(os.environ["WORKBENCH_CANDIDATE_DIR"])
output_dir = Path(os.environ["WORKBENCH_OUTPUT_DIR"])
output_dir.mkdir(parents=True, exist_ok=True)

completed = subprocess.run(
    ["python", "scripts/check.py"],
    cwd=candidate_dir,
    text=True,
    capture_output=True,
)

(output_dir / "workflow-evidence.json").write_text(json.dumps({
    "exitCode": completed.returncode,
    "stdout": completed.stdout[-4000:],
    "stderr": completed.stderr[-4000:],
}), encoding="utf8")
```

The grader writes:

```python
import json
import os
from pathlib import Path

evidence = json.loads((Path(os.environ["WORKBENCH_OUTPUT_DIR"]) / "workflow-evidence.json").read_text())
score = 1.0 if evidence["exitCode"] == 0 else 0.0
Path(os.environ["WORKBENCH_REWARD_FILE"]).write_text(json.dumps({
    "score": score,
    "summary": "Existing workflow passed." if score == 1.0 else "Existing workflow failed.",
    "fileChanges": [],
    "feedback": evidence,
}, indent=2), encoding="utf8")
```

## Spec

```yaml
optimization:
  selection:
    use: greedy
    metric: score
    direction: maximize
evaluation:
  environment:
    use: oci
    with:
      image: docker://workbench/workbench-python-3.12:envv_python_3_12
  runner:
    use: command
    with:
      run: python "$WORKBENCH_CANDIDATE_DIR/scripts/run_existing_workflow.py"
  grader:
    use: command
    with:
      run: python "$WORKBENCH_CANDIDATE_DIR/scripts/grade_workflow.py"
```

Use [runner-contract.md](runner-contract.md) to keep the reward output valid.
