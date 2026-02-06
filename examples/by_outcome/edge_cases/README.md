# Edge Cases

This directory documents evaluations where unexpected behaviors or edge conditions affected agent performance.

## Documented Edge Cases

### Empty Results
- **Empty cluster**: Clustering produces a cluster with 0 cells at certain resolutions
- **No DE genes**: Statistical test returns no significant genes at FDR threshold
- **All cells filtered**: Overly aggressive QC removes entire dataset

### Numerical Edge Cases
- **Tied rankings**: Multiple genes with identical p-values in DE ranking
- **Zero variance**: Gene with zero expression across all cells causes division error
- **Floating point**: Small numerical differences accumulate across pipeline steps

### Data Structure Issues
- **Sparse vs dense**: Some operations require dense matrix, causing memory issues
- **Missing annotations**: Expected `.obs` column not present in dataset
- **Duplicate indices**: Cell barcodes not unique after merge

### Platform-Specific
- **MissionBio protein data**: Multi-modal data with protein assay alongside RNA
- **ParseBio multiplexing**: Sample demultiplexing metadata in non-standard format
- **CSGenetics UMI structure**: Different UMI deduplication affects counts

## Impact on Evaluation

Edge cases are handled through:
1. **Wider tolerances**: Accept range of valid answers
2. **Multiple correct answers**: Grader accepts alternative solutions
3. **Explicit notes**: Eval definition documents known edge behavior
