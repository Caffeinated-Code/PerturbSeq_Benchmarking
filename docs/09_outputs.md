# Benchmark Outputs

The benchmark should produce compact tables for review and machine-readable files for reuse.

## Core Tables

| File | Purpose |
|---|---|
| `dataset_qc.csv` | dataset size, guide coverage, control balance, design status |
| `guide_qc.csv` | guide-level cell counts and warning flags |
| `perturbation_qc.csv` | target knockdown or activation, guide concordance, escapee rate |
| `method_effects.csv` | perturbation-gene or perturbation-feature effects |
| `method_summary.csv` | discoveries, calibration metrics, runtime, memory |
| `cell_state_summary.csv` | state abundance by perturbation |
| `ad_microglia_recovery.csv` | recovery of Alzheimer and microglia marker programs |
| `regulatory_validation.csv` | synthetic evidence-model fixture with explicit scope labels |
| `regulatory_validation_summary.csv` | synthetic support-status counts for app testing |
| `method_agreement.csv` | agreement across benchmarked methods |
| `benchmark_summary.csv` | final method-level summary |

## Figures

Recommended figures:

- cells per perturbation
- guides per target
- non-targeting control balance
- target knockdown dot plot
- perturbation effect heatmap
- cell-state proportion heatmap
- AD/microglia gene-set recovery plot
- synthetic evidence score plot, labeled as infrastructure testing
- peak-to-gene support heatmap
- method agreement UpSet plot
- runtime and memory bar plot

## Report Structure

Each dataset report should include:

1. Dataset design
2. QC summary
3. Native analysis reproduction
4. Method comparison
5. Synthetic evidence-model checks or real external evidence when actually ingested
6. Alzheimer or disease-relevant interpretation
7. Limitations
8. Recommended method choice

## Final Cross-Dataset Report

The cross-dataset report should answer:

- Which method was most statistically conservative?
- Which method recovered paper-native biology best?
- Which method handled heterogeneous response best?
- Which method scaled best?
- Which method was most useful for microglia-state interpretation?
- Which datasets were incompatible with each method, and why?

## Modular Replication

Use `scripts/run_analysis_modules.sh` when you want to rerun a specific stage.

| Module | Command | Output |
|---|---|---|
| `demo` | `bash scripts/run_analysis_modules.sh demo` | demo input CSVs |
| `nextflow` | `bash scripts/run_analysis_modules.sh nextflow` | QC, method, benchmark, validation, and report outputs |
| `public` | `bash scripts/run_analysis_modules.sh public` | public dataset manifests and lightweight audits |
| `bundle` | `bash scripts/run_analysis_modules.sh bundle` | Shiny-ready result bundle |
| `validate` | `bash scripts/run_analysis_modules.sh validate` | repository, output, and Shiny checks |
| `all` | `bash scripts/run_analysis_modules.sh all` | full lightweight local replication |

The `nextflow` module accepts environment variables:

```bash
PROFILE=aws \
OUTDIR=s3://your-bucket/perturbseq/demo \
bash scripts/run_analysis_modules.sh nextflow
```
