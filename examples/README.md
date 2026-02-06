# scBench Canonical Examples

This directory provides easy access to the 7 canonical evaluations with their trajectories. These examples cover one problem from each task category, all using the Chromium platform.

## Canonical Evaluations

| Task | Eval ID | Description |
|------|---------|-------------|
| QC | `chromium_qc_4T1_filter_cells` | Filter low-quality cells from 4T1 tumor data |
| Normalization | `chromium_4t1_normalization` | Normalize expression values |
| Dim. Reduction | `chromium_4t1_hvg_gene_sets` | Select highly variable genes |
| Clustering | `chromium_clustering_01_4t1_pericyte_adjacent_to_caf` | Identify cell clusters |
| Cell Typing | `chromium_celltyping_01_4t1_compartment_fractions` | Annotate cell type fractions |
| Diff. Expression | `chromium_de_01_contractile_caf_marker_recovery` | Recover marker genes |
| Trajectory | `chromium_trajectory_01_caf_terminal_marker_recovery` | Pseudotime analysis |

## Directory Structure

```
examples/
├── by_task/                     # Symlinks to eval definitions
│   ├── qc/
│   ├── normalization/
│   ├── ...
│
└── by_outcome/                  # Failure mode documentation
    ├── common_failures/
    └── edge_cases/
```

## Accessing Trajectories

Full trajectories are stored in `trajectories/minisweagent/`. To find results for a canonical eval:

```bash
# Find results for the QC canonical example
grep -r "chromium_qc_4T1_filter_cells" trajectories/minisweagent/chromium/minisweagent/qc/*/results.json

# View a specific model's result
cat trajectories/minisweagent/chromium/minisweagent/qc/anthropic_claude-opus-4-5_r1/results.json | \
  jq '.results[] | select(.eval == "chromium_qc_4T1_filter_cells")'
```

## Trajectory Data Location

```
trajectories/minisweagent/
└── chromium/
    └── minisweagent/
        ├── qc/
        │   ├── anthropic_claude-opus-4-5_r1/
        │   │   ├── results.json       # Eval outcomes with grader output
        │   │   └── workspaces/        # Per-eval execution artifacts
        │   ├── anthropic_claude-opus-4-5_r2/
        │   ├── ...
        │   └── xai_grok-4-fast-reasoning_r3/
        ├── normalization/
        ├── dimensionality_reduction/
        ├── clustering/
        ├── cell_typing/
        ├── differential_expression/
        └── trajectory_analysis/
```

## Results Format

Each `results.json` contains:
- `metadata`: Model, run ID, timestamp, aggregate stats
- `by_task` / `by_kit`: Breakdown summaries
- `results[]`: Per-eval outcomes including:
  - `eval`: Evaluation ID
  - `passed`: Boolean outcome
  - `grader_result`: Detailed metrics and reasoning
  - `duration_s`, `total_cost`, `n_steps`

## Eval Definition Format

Each `.json` in `evals_canonical/` contains:
- `id`: Unique evaluation identifier
- `task`: Natural language prompt
- `data_node`: Pointer to .h5ad file
- `grader`: Type and configuration (tolerances, ground truth)
- `metadata`: Task category, platform, eval type
