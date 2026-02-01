# Adding New Evaluations

This guide describes how to create new evaluations for SCBench.

## Prerequisites

1. Access to single-cell RNA-seq dataset
2. Verified ground truth answer
3. Appropriate grader type

## Steps

### 1. Prepare the Dataset

Upload your dataset to Latch Data and note the node ID:

```
latch://157798549.node
```

### 2. Create Evaluation JSON

```json
{
  "id": "chromium_task_description_version",
  "task": "Detailed task description...",
  "data_node": "latch://157798549.node",
  "grader": {
    "type": "numeric_tolerance",
    "config": {
      "ground_truth": {"field_name": 1234},
      "tolerance": 10
    }
  },
  "metadata": {
    "task": "qc",
    "kit": "chromium"
  }
}
```

### 3. Validate

```bash
scbench validate path/to/eval.json
```

### 4. Test

```bash
scbench run path/to/eval.json --agent minisweagent --keep-workspace
```

## Task Description Guidelines

- Be specific about expected output format
- Include all necessary context
- Specify exact field names in JSON output
- Avoid ambiguity

## Ground Truth Guidelines

- Verify with multiple methods when possible
- Document analysis pipeline and parameters
- Include random seeds for reproducibility
