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
- method agreement UpSet plot
- runtime and memory bar plot

## Report Structure

Each dataset report should include:

1. Dataset design
2. QC summary
3. Native analysis reproduction
4. Method comparison
5. Alzheimer or disease-relevant interpretation
6. Limitations
7. Recommended method choice

## Final Cross-Dataset Report

The cross-dataset report should answer:

- Which method was most statistically conservative?
- Which method recovered paper-native biology best?
- Which method handled heterogeneous response best?
- Which method scaled best?
- Which method was most useful for microglia-state interpretation?
- Which datasets were incompatible with each method, and why?

