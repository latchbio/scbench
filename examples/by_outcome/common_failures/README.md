# Common Failure Modes

This directory documents recurring failure patterns observed across models and evaluations.

## Failure Categories

### 1. Data Loading Errors
- **Wrong file path**: Agent assumes incorrect location for .h5ad file
- **Missing import**: Forgot to import scanpy or anndata
- **Memory overflow**: Tried to load full matrix instead of sparse

### 2. Methodology Errors
- **Wrong function**: Used `sc.pp.normalize_per_cell` instead of `sc.pp.normalize_total`
- **Parameter confusion**: Mixed up `min_genes` and `min_cells` in filtering
- **Order of operations**: Normalized before filtering, affecting results

### 3. Output Format Errors
- **Schema mismatch**: Returned `{"cell_count": N}` instead of `{"cells_after_filtering": N}`
- **Type error**: Returned string instead of int
- **Missing field**: Omitted required output field

### 4. Interpretation Errors
- **Threshold misread**: Applied "greater than 20%" when prompt said "at least 20%"
- **Column confusion**: Used `n_counts` when `n_genes` was required
- **Subset error**: Filtered wrong cell population for DE analysis

## Most Common by Task Category

| Task | Top Failure Mode | Frequency |
|------|------------------|-----------|
| QC | Forgot one filter criterion | 23% |
| Normalization | Wrong normalization function | 15% |
| Dim. Reduction | Incorrect n_top_genes parameter | 18% |
| Clustering | Resolution parameter out of range | 21% |
| Cell Typing | Marker gene list hallucination | 31% |
| Diff. Expression | Wrong comparison groups | 28% |
