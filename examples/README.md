# scBench Canonical Examples

This directory provides easy access to 30 canonical evaluations across 5 platforms. Each platform includes one evaluation per task category where available.

## Canonical Evaluations by Platform

### Chromium (7 evals)

| Task | Eval ID | Description |
|------|---------|-------------|
| QC | `chromium_qc_4T1_filter_cells` | Filter low-quality cells from 4T1 tumor data |
| Normalization | `chromium_4t1_normalization` | Normalize expression values |
| Dim. Reduction | `chromium_4t1_hvg_gene_sets` | Select highly variable genes |
| Clustering | `chromium_clustering_01_4t1_pericyte_adjacent_to_caf` | Identify cell clusters |
| Cell Typing | `chromium_celltyping_01_4t1_compartment_fractions` | Annotate cell type fractions |
| Diff. Expression | `chromium_de_01_contractile_caf_marker_recovery` | Recover marker genes |
| Trajectory | `chromium_trajectory_01_caf_terminal_marker_recovery` | Pseudotime analysis |

### CSGenetics (6 evals)

| Task | Eval ID | Description |
|------|---------|-------------|
| QC | `csgenetics_qc_filtering` | Filter cells from PBMC data |
| Normalization | `csgenetics_normalization_full_pipeline` | Full normalization pipeline |
| Dim. Reduction | `csgenetics_pca_pc1_biological_axis` | Interpret PC1 biological axis |
| Clustering | `csgenetics_clustering_avg_purity` | Measure average cluster purity |
| Cell Typing | `csgenetics_celltyping_major_immune_lineages` | Identify major immune lineages |
| Diff. Expression | `csgenetics_de_monocyte_pseudobulk` | Monocyte pseudobulk DE analysis |

### Illumina (6 evals)

| Task | Eval ID | Description |
|------|---------|-------------|
| QC | `illumina_qc_report_initial_nuclei` | Report nuclei count after filtering |
| Normalization | `illumina_normalization_cp10k_log1p` | CP10K + log1p normalization |
| Dim. Reduction | `illumina_dimred_choose_batch_key` | Choose batch correction key |
| Clustering | `illumina_clustering_leiden_n_clusters` | Leiden clustering count |
| Cell Typing | `illumina_celltyping_major_cell_types` | Identify major cell types |
| Diff. Expression | `illumina_de_edn1_maximal` | EDN1 maximal expression test |

### MissionBio (6 evals)

| Task | Eval ID | Description |
|------|---------|-------------|
| QC | `missionbio_qc_variant_call_rate` | Variant call rate metrics |
| Normalization | `missionbio_normalization_protein_integrity` | Protein normalization integrity |
| Dim. Reduction | `missionbio_dimred_normalization_choice` | Normalization method choice |
| Clustering | `missionbio_clustering_n_clusters` | Count clusters from Louvain |
| Cell Typing | `missionbio_celltyping_present_cell_types` | Identify present cell types |
| Diff. Expression | `missionbio_de_mutation_frequency` | Differential mutation frequency |

### ParseBio (5 evals)

| Task | Eval ID | Description |
|------|---------|-------------|
| Normalization | `parsebio_normalization_edge_decision` | Edge normalization decision |
| Dim. Reduction | `parsebio_pca_pc1_primary_driver` | PC1 primary driver interpretation |
| Clustering | `parsebio_clustering_celltype_purity` | Cell type purity assessment |
| Cell Typing | `parsebio_celltyping_coarse_distribution` | Coarse cell type distribution |
| Diff. Expression | `parsebio_de_ifnb_cd14mono_markers` | IFN-beta CD14 monocyte markers |

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

## Eval Definition Format

Each `.json` in `evals_canonical/` contains:
- `id`: Unique evaluation identifier
- `task`: Natural language prompt
- `data_node`: Pointer to .h5ad file
- `grader`: Type and configuration (tolerances, ground truth)
- `metadata`: Task category, platform, eval type
