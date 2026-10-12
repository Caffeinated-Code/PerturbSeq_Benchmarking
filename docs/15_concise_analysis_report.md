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
- evidence-model checks against synthetic peak, peak-to-gene, motif, and annotation tables

## Current Results

| Result | Value |
|---|---:|
| perturbation-gene effects tested | 100 |
| non-neutral effects | 14 |
| Alzheimer gene effects | 4 |
| microglia-state gene effects | 10 |
| synthetic evidence tests | 14 |
| synthetic PASS fixtures | 7 |
| synthetic WARN fixtures | 0 |
| synthetic LOW_SUPPORT fixtures | 7 |

## Interpretation

The demo proves that the workflow can connect perturbation-effect tables to a typed evidence interface. It does not provide regulatory validation or biological claims because every evidence record is synthetic.

## Next Real-Data Analyses

1. Recover or reconstruct guide assignments for GSE178317.
2. Obtain the guide/cCRE mapping for GSE207628.
3. Add the Replogle cell-level object for methods that require individual cells.
4. Freeze upstream method environments and execute only compatible routes.
5. Add an external evidence source only after source-native data are ingested, harmonized, and connected to reproducible outputs.
