# Executable Method and Benchmark Contract

## Lifecycle semantics

Every attempted adapter writes `method_status.csv`. `RUN` means that the named upstream method (or the explicitly named transparent baseline) returned and its expected output was written. The other states are not aliases:

| State | Meaning |
|---|---|
| `RUN` | The named implementation executed successfully and output validation passed. |
| `SKIP` | An operator or benchmark plan intentionally omitted an otherwise compatible run. |
| `INCOMPATIBLE` | Measured dataset properties violate the method contract. |
| `FAILED` | Execution began but the adapter or output validation failed. |
| `NOT_AVAILABLE` | The adapter, runtime, or pinned upstream dependency is absent. |

An absent package is never reported as `RUN`. A transparent baseline is never relabeled as SCEPTRE, Mixscape, PS, GSFA, pertpy, or a paper-native method.

## Pinned integrations and constraints

| Adapter | Pin | Executable entry point | Compatibility contract |
|---|---|---|---|
| transparent pseudobulk | `builtin-1` | `bin/run_method.py` | RNA/targeted RNA, controls, adequate coverage; aggregates by replicate or batch before inference. |
| SCEPTRE | commit `21f9ea098b69c444a884a49bc254de711968e3b5` | `bin/adapters/run_r_method.R` | Low-MOI and high/mixed-MOI routes are separate. Counts, binary guide assignments, controls, and covariates are required. |
| Mixscape | Seurat `5.3.0` | same | Whole-transcriptome RNA only. Requires non-targeting cells and enough genes to form perturbation signatures. |
| perturbation-response score | scMAGeCK commit `e24aa0f3c9734c26ffbc200107adf0e199b26208` | same | RNA response signature, guide table, perturbation label, and non-targeting label. Targeted panels below 50 genes are rejected. |
| GSFA | commit `8e7cf03fdeeb008ef7dec7b6bc6407642d14376e` | same | Whole-transcriptome normalized RNA, multiple perturbations, and enough features for factors. |
| pertpy distance | `0.10.0` | `bin/run_method.py` | Python 3.10–3.12, AnnData-compatible grouped RNA data, controls. Uses energy distance. |
| paper-native | dataset-specific | registered per dataset | `NOT_AVAILABLE` unless an executable dataset-specific adapter is declared. A prose description is not execution. |

Pins are reproducibility inputs, not claims that every dependency is preinstalled. The environment deliberately pins pertpy 0.10.0 because the repository uses Python 3.11, while pertpy 1.x requires Python 3.12 or newer.

Primary documentation inspected: the [SCEPTRE package and manual](https://katsevich-lab.github.io/sceptre/), [Seurat Mixscape reference](https://satijalab.org/seurat/reference/runmixscape), [PS/scMAGeCK implementation](https://github.com/davidliwei/PS), [GSFA reference](https://xinhe-lab.github.io/GSFA/reference/fit_gsfa_multivar.html), and [pertpy distance reference](https://pertpy.readthedocs.io/en/stable/tutorials/notebooks/distances.html). Publication links remain in `configs/methods.yml`.

## Routing inputs

`select_methods.py` records measured cell/feature/perturbation/guide counts, minimum target coverage, mean guides per cell, collision rate, MOI class, declared or inferred readout breadth, modality, replicate count, non-targeting-control count, and available covariates. These values—not a dataset name—drive compatibility.

The low-MOI SCEPTRE route requires mean guides per cell at most 1.2 and collision rate at most 0.15. The high/mixed-MOI route requires the complement. Exactly one can be compatible. Feature count alone is only a default readout inference; callers should pass `--readout-class targeted` for designed panels.

## Benchmark outputs

`score_benchmark.py` emits a long table with the method lifecycle state, metric state, estimate, interval fields, and detail. Missing estimands are `NOT_AVAILABLE`; structurally irrelevant estimands are `NOT_APPLICABLE`. Runtime, peak memory, failure reason, FDR discoveries, target engagement, program recovery, null calibration/type-I error, guide concordance, effect stability, and escapee fraction have explicit rows. Metrics requiring guide-level, null, classification, replicate, or resampling outputs remain missing until those outputs exist.

`compare_methods.py` reports pairwise effect agreement and never creates a composite winner or rank. Benchmark conclusions must show uncertainty, downsampling/covariate sensitivity, lifecycle states, and dataset-specific limitations. Synthetic fixtures test calibration and known injected effects; they validate software behavior only and cannot support biological-superiority claims.

## Focused checks

Run `python -m unittest discover -s tests -v`. Fixtures cover mutually exclusive MOI routing, targeted-panel incompatibility, positive-control recovery, honest `RUN`, and `NOT_AVAILABLE` behavior. The `--null` fixture supports downstream type-I-error checks without a biological claim.
