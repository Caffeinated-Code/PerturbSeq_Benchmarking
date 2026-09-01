# Dataset-Aware Method Routing

## Purpose

Perturb-seq methods are not interchangeable. The benchmark profiles each dataset before method execution and records which methods are appropriate.

## Routing Inputs

The method selector uses:

- mean guides per cell
- guide collision rate
- cells per perturbation
- readout breadth
- modality
- presence of chromatin or protein features

## MOI Classification

| Class | Rule | Interpretation |
|---|---|---|
| low-MOI | mean guides per cell <= 1.2 and guide collision rate <= 0.15 | most cells carry one perturbation |
| high-or-mixed-MOI | mean guides per cell > 1.2 or guide collision rate > 0.15 | guide combinations or collisions are common |

## Method Decisions

| Method | Routing rule |
|---|---|
| paper-native analysis | always planned when source study design is available |
| pseudobulk baseline | RNA or targeted RNA with adequate cells per perturbation |
| SCEPTRE low-MOI | low-MOI RNA designs |
| SCEPTRE high-MOI or mixed-MOI workflow | high-MOI or mixed-MOI RNA designs |
| Mixscape | whole-transcriptome RNA with adequate perturbation coverage |
| GSFA | whole-transcriptome RNA with enough signal for module inference |
| PS | RNA or targeted RNA with adequate cells per perturbation |
| pertpy distance workflow | compatible single-cell objects |
| Signac, ArchR, chromVAR track | scATAC, multiome, or regulatory-validation resources |

## Output

The selector writes:

- `dataset_profile.csv`
- `method_decisions.csv`

These files are included in the benchmark report.

## Current Implementation

`bin/select_methods.py` implements the first routing layer for CSV demo inputs. Real AnnData-based routing should extend the same rules after dataset conversion.

