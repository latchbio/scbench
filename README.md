# scBench

**Evaluating AI Agents on Single-Cell RNA-seq Analysis**

scBench is a benchmark of 394 verifiable problems derived from practical single-cell RNA-seq workflows. Each problem pairs a data snapshot (AnnData `.h5ad`) with a natural-language task prompt and a deterministic grader that maps the agent's structured output to pass/fail.

## Key Findings

| Model | Accuracy | 95% CI | Latency |
|-------|----------|--------|---------|
| Claude Opus 4.6 | 52.8% | (48.3, 57.2) | 303s |
| Claude Opus 4.5 | 49.9% | (45.3, 54.4) | 154s |
| GPT-5.2 | 45.2% | (40.9, 49.5) | 133s |
| Claude Sonnet 4.5 | 44.2% | (39.9, 48.6) | 193s |
| GPT-5.1 | 37.9% | (33.7, 42.0) | 94s |
| Grok-4.1 | 35.6% | (31.6, 39.7) | 180s |
| Grok-4 | 33.9% | (30.1, 37.8) | 203s |
| Gemini 2.5 Pro | 29.2% | (25.6, 32.9) | 300s |

Full results with per-task and per-platform breakdowns are in [`results/`](results/).

## Benchmark Structure

394 evaluations across:
- **6 platforms**: BD Rhapsody, Chromium, CSGenetics, Illumina, MissionBio, ParseBio
- **7 task categories**: QC, Normalization, Dimensionality Reduction, Clustering, Cell Typing, Differential Expression, Trajectory Analysis

Tasks require empirical interaction with the data—agents that rely on prior knowledge without performing the requisite analysis fail.

## Canonical Examples

Seven canonical examples (one per task category) are in [`evals_canonical/`](evals_canonical/) with organized access via [`examples/`](examples/). The full 394-evaluation benchmark is withheld to prevent training contamination.

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
scbench run evals_canonical/chromium/chromium_qc_4T1_filter_cells.json --agent minisweagent --model anthropic/claude-opus-4-5
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
@article{scbench2026,
  title={scBench: Evaluating AI Agents on Single-Cell RNA-seq Analysis},
  author={Workman, Kenny and Yang, Zhen and Muralidharan, Harihara and Abdulali, Aidan and Le, Hannah},
  year={2026},
  note={LatchBio}
}
```

## License

Apache 2.0
