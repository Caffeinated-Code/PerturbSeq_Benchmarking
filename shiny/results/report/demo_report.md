# Perturb-seq Benchmark Report

## Scope

- Three public datasets were processed.
- One generated dataset tests the workflow.
- Two analysis strategies produced results.
- Six more method adapters were checked for compatibility.

## Generated Test

- Cells: 360
- Perturbations: 5 plus one non-targeting control
- Genes: 20
- Perturbation-gene pairs: 100
- Non-neutral pairs: 14 across 11 response genes

These results test the software. They are not biological discoveries.

## Public Data

- GSE178317 supports expression, lane, and cell-state QC.
- GSE207628 supports targeted-panel QC and replicate comparison.
- Replogle K562 supports target and control auditing at pseudobulk level.

The two microglia datasets lack cell-to-guide assignments. Perturbation effects cannot be estimated from their deposited matrices.

## Disease Corroboration

GWAS Catalog supports Alzheimer disease relevance for APOE, TREM2, INPP5D, and SPI1 at `p <= 5e-8`.

This evidence supports prioritization. It does not prove causality or validate an expression-effect direction.

## Next Step

Obtain guide-resolved microglia data. Then compare compatible methods with shared contrasts, biological replicates, and prespecified error control.
