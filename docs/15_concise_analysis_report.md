# Analysis Report

## Scope

The project processed three public datasets and one generated test dataset.

| Dataset | Measured data | Current use |
|---|---:|---|
| GSE178317 microglia CROP-seq | 58,302 cells; 33,538 genes | expression QC, lane QC, cell-state summaries |
| GSE207628 AD microglia CRISPRi-HyPR-seq | 10,463 cells; 49 targeted features | panel QC and replicate agreement |
| Replogle K562 Perturb-seq | 2,285 guide-pair pseudobulks; 8,563 genes | target and control audit; paper-native summary |
| Generated test data | 360 cells; 20 genes | software, routing, and expected-effect tests |

The two microglia deposits do not include cell-to-guide assignments. They cannot support perturbation-effect estimates in this release.

## Methods Run

Two analysis strategies produced results:

- paper-native summaries for compatible public products
- a transparent pseudobulk baseline for the generated test data

Six other adapters were checked against assay requirements. A method is marked `INCOMPATIBLE` when the data lack its required readout, guide assignments, controls, or MOI information. Eligibility is not evidence that a method ran.

## Generated Benchmark

The test dataset contains five perturbations and one non-targeting control. It has low guide multiplicity and no guide collisions.

| Result | Value |
|---|---:|
| perturbation-gene pairs tested | 100 |
| non-neutral pairs | 14 |
| response genes represented | 11 |
| generated evidence examples | 14 |

These values test expected software behavior. They are not biological discoveries.

## Public-Data Result

The Replogle product contains 2,134 targeting guide-pair pseudobulks. Median target-expression change was -82.7%. The compact pseudobulk product supports target-level auditing. It does not support cell-level escapee analysis or a new count of significant genes.

## Alzheimer Corroboration

A reproducible NHGRI-EBI GWAS Catalog query tested candidate genes against Alzheimer disease and child traits. APOE, TREM2, INPP5D, and SPI1 had mapped-gene associations at `p <= 5e-8`.

This result supports disease relevance. It does not prove that a mapped gene is causal. It does not validate perturbation magnitude, direction, or microglial specificity.

## Next Analysis

1. Obtain cell-to-guide assignments for a microglia perturbation dataset.
2. Record MOI, guide efficiency, controls, donor, and replicate structure.
3. Run only methods that match the assay design.
4. Use shared contrasts and prespecified error control.
5. Replicate leading effects in an independent perturbation dataset.
6. Add chromatin or QTL evidence only after cell context and genome build are harmonized.
