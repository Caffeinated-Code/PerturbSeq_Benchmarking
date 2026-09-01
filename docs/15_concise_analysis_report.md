# Concise Analysis Report

## Current Demo Analysis

The current repository runs a synthetic Perturb-seq benchmark that validates the workflow structure.

## Dataset QC

| Metric | Value |
|---|---:|
| cells | 360 |
| genes | 20 |
| perturbations | 6 |
| guides | 6 |
| batches | 2 |
| non-targeting control cells | 60 |
| minimum cells per perturbation | 60 |
| design status | PASS |

## Method Routing

The demo dataset is low-MOI. Mean guide count is 1 guide per cell, and the guide collision rate is 0.

Current routing:

- pseudobulk baseline: RUN
- SCEPTRE low-MOI: RUN candidate
- SCEPTRE high-MOI or mixed-MOI workflow: SKIP
- Mixscape: SKIP for this demo because the readout has 20 genes and is treated as targeted
- GSFA: SKIP for this demo because the readout is targeted
- PS: RUN candidate
- pertpy workflow: RUN candidate
- chromatin-specific methods: SKIP for RNA-only input

## Implemented Analysis

The demo analysis currently includes:

- dataset-level QC
- guide-level QC
- cell-state summary
- pseudobulk perturbation-effect estimation
- Alzheimer gene recovery
- microglia-state gene recovery
- regulatory validation against synthetic peak, peak-to-gene, motif, and annotation tables

## Current Results

| Result | Value |
|---|---:|
| perturbation-gene effects tested | 100 |
| non-neutral effects | 14 |
| Alzheimer gene effects | 4 |
| microglia-state gene effects | 10 |
| regulatory validation tests | 14 |
| regulatory validation PASS | 7 |
| regulatory validation WARN | 0 |
| regulatory validation LOW_SUPPORT | 7 |

## Interpretation

The demo proves that the benchmark can connect perturbation effects to downstream biological interpretation and regulatory validation. It does not make biological claims about Alzheimer disease because the input data are synthetic.

## Next Real-Data Analyses

1. Convert Drager microglia CROP-seq into the shared schema.
2. Run paper-native microglia state-shift analysis.
3. Run pseudobulk, Mixscape, PS, and SCEPTRE according to MOI profile.
4. Convert Yang/Shen GSE207628 and analyze it as targeted AD microglia CRISPRi-HyPr-seq.
5. Add Replogle K562 as a scale and calibration benchmark.
6. Add SEA-AD chromatin validation for microglia regulatory context.

