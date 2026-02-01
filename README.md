# scBench

**Can AI agents analyze real-world single-cell data?**

SCBench is a benchmark of verifiable problems derived from practical single-cell RNA-seq workflows. Each problem snapshots an analysis state immediately before a target step and pairs it with a deterministic grader that evaluates recovery of a key biological result.

## Key Findings

| Model | Accuracy | Cost/Eval | Latency |
|-------|----------|-----------|---------|
| Opus-4.5 | 50.0% | $0.39 | 275s |
| GPT-5.2 | 46.6% | $0.04 | 89s |
| Sonnet-4.5 | 41.4% | $0.08 | 116s |
| Gemini-2.5-Pro | 41.1% | $0.19 | 194s |

Full results with 95% confidence intervals are in [`results/`](results/).

## Benchmark Structure

Evaluations across:
- **6 platforms**: Chromium, BD Rhapsody, Parse, Illumina, MissionBio, CSGenetics
- **7 task categories**: QC, Normalization, Dimensionality Reduction, Clustering, Cell Typing, Differential Expression, Trajectory Analysis

Tasks require empirical interaction with the data—agents that rely on prior knowledge without performing the requisite analysis fail to complete many tasks correctly.

## Canonical Examples

This repository includes canonical examples in [`evals_canonical/`](evals_canonical/) demonstrating the evaluation format. The full benchmark is withheld to prevent overfitting.

| Task | Platform | Grader |
|------|----------|--------|
| QC | Chromium | Numeric |
| Normalization | Chromium | Numeric |
| Dimensionality Reduction | Chromium | MCQ |
| Clustering | Chromium | MCQ |
| Cell Typing | Chromium | Cosine |
| Differential Expression | Chromium | P@K |
| Trajectory Analysis | Chromium | P@K |

## Quick Start

```bash
pip install -e .

# Validate an evaluation
scbench validate evals_canonical/chromium/chromium_qc_4T1_filter_cells.json

# Run with mini-swe-agent
export ANTHROPIC_API_KEY=your_key
scbench run evals_canonical/chromium/chromium_qc_4T1_filter_cells.json --agent minisweagent
```

### Custom Agent

```python
from scbench import EvalRunner

def my_agent(task_prompt, work_dir):
    import json
    answer = {"cells_after_filtering": 6355}
    (work_dir / "eval_answer.json").write_text(json.dumps(answer))
    return answer

runner = EvalRunner("evals_canonical/chromium/chromium_qc_4T1_filter_cells.json")
result = runner.run(agent_function=my_agent)
print(f"Passed: {result['passed']}")
```

## Graders

Five grader families handle different answer types:

| Grader | Use Case |
|--------|----------|
| NumericTolerance | QC metrics, counts, expression values |
| MultipleChoice | Discrete interpretation questions |
| MarkerGenePrecisionRecall | Gene lists (P@K, R@K) |
| LabelSetJaccard | Cell type sets |
| DistributionComparison | Cell type proportions |

See [eval-graders](https://github.com/latchbio/eval-graders) for implementations.

## Citation

```bibtex
TODO
```

## License

Apache 2.0
