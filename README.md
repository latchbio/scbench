# scBench

**Evaluating AI Agents on Single-Cell RNA-seq Analysis**

scBench is a benchmark of 195 verifiable problems derived from practical single-cell RNA-seq workflows. Each problem pairs a data snapshot (AnnData `.h5ad`) with a natural-language task prompt and a deterministic grader that maps the agent's structured output to pass/fail.

## Key Findings

| model_name | harness | Accuracy (%) | Cost ($) |
|---|---|---:|---:|
| gpt-5.5 | mini-swe-agent | 57.95 | 1.1136 |
| gpt-5.5 | openai-codex | 57.78 | 2.4685 |
| gpt-5.4 | mini-swe-agent | 57.44 | 0.8240 |
| claude-opus-4-7 | mini-swe-agent | 55.21 | 1.5378 |
| claude-opus-4-7 | claude-code | 54.02 | 1.1465 |
| gemini-3.1-pro-preview | mini-swe-agent | 53.85 | 0.8948 |
| claude-opus-4-6 | mini-swe-agent | 52.65 | 1.1917 |
| gpt-5.2 | mini-swe-agent | 52.31 | 0.8874 |
| claude-sonnet-4-6 | mini-swe-agent | 50.26 | 0.9872 |
| claude-opus-4-5 | mini-swe-agent | 47.18 | 0.6553 |
| grok-4.20-beta-0309-reasoning | mini-swe-agent | 44.44 | 0.2957 |
| grok-4.3 | mini-swe-agent | 44.27 | 0.2147 |
| gpt-5.1 | mini-swe-agent | 38.80 | 0.2177 |
| claude-sonnet-4-5 | mini-swe-agent | 33.16 | 0.2682 |
| grok-4-1-fast-reasoning | mini-swe-agent | 30.26 | 0.0282 |
| gemini-2.5-pro | mini-swe-agent | 23.59 | 0.1368 |

Full results with per-task and per-platform breakdowns are in [`results/`](results/).

## Benchmark Structure

195 evaluations across:
- **6 platforms**: BD Rhapsody, Chromium, CSGenetics, Illumina, MissionBio, ParseBio
- **6 task categories**: QC, Normalization, Dimensionality Reduction, Clustering, Cell Typing, Differential Expression

Tasks require empirical interaction with the data—agents that rely on prior knowledge without performing the requisite analysis fail.

## Canonical Examples

Six canonical examples are in [`evals/`](evals/). The sample covers all current platforms and task categories. The full 195-evaluation benchmark is withheld to prevent training contamination.

| Task | Platform | Eval |
|---|---|---|
| QC | BD Rhapsody | `bd_rhapsody_tnbc_panel_aware_qc` |
| Dimensionality Reduction | Chromium | `dr_05_pca_preprocessing_sentinels` |
| Normalization | CS Genetics | `NRM01_sparse_normalization` |
| Cell Typing | Illumina snRNA | `T04a_endothelin_niche_sources` |
| Clustering | Mission Bio Tapestri | `tapestri_ccus_clustering_12_largest_mutant_clone` |
| Differential Expression | Parse Bio | `DE01_pseudobulk_de` |

## Quick Start

```bash
pip install -e .

# Validate an evaluation
scbench validate evals/qc/bd_rhapsody_tnbc_panel_aware_qc.json

# Run with mini-swe-agent
export ANTHROPIC_API_KEY=your_key
scbench run evals/qc/bd_rhapsody_tnbc_panel_aware_qc.json --agent minisweagent --model anthropic/claude-opus-4-5
```

### Custom Agent

```python
from scbench import EvalRunner

def my_agent(task_prompt, work_dir):
    import json
    answer = {
        "n_pbmcs_retained": 14346,
        "median_genes_per_pbmc": 68,
        "n_monocytes_pbmc": 2592,
    }
    (work_dir / "eval_answer.json").write_text(json.dumps(answer))
    return answer

runner = EvalRunner("evals/qc/bd_rhapsody_tnbc_panel_aware_qc.json")
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

See [latch-eval-tools](https://github.com/latchbio/latch-eval-tools) for implementations.

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
