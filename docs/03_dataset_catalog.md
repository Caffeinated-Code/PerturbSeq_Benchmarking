# Dataset Catalog

The active project contains three processed public resources and one synthetic software fixture. A dataset appears here only when its files have been downloaded or generated, inspected, and connected to a reproducible workflow.

## Availability And Analytical Role

| Dataset | Available data | Missing data | What it supports now | What it cannot support now |
|---|---|---|---|---|
| Drager GSE178317 microglia CROP-seq | 58,302 deposited RNA profiles across four lanes; 33,538 genes; matched sgRNA-enrichment archives | authors' consensus cell-to-guide table and usable guide identities | lane-aware expression QC, mitochondrial/count QC, microglial state-program summaries, guide-archive audit | perturbation effects, targeting-control contrasts, guide concordance, escapee detection |
| Yang/Shen GSE207628 AD microglia CRISPRi-HyPR-seq | 10,463 cells, two biological differentiations, 49 targeted/barcode probes | public cell-to-guide or cCRE mapping and experimental MOI | targeted-panel QC, feature coverage, replicate agreement, AD-locus gene context | enhancer-specific effects, guide-level contrasts, whole-transcriptome methods |
| Replogle K562 essential Perturb-seq | 2,285 author-deposited guide-pair pseudobulks by 8,563 genes, summarizing 310,385 filtered cells; target and control labels | cell-level expression object in the compact workflow; donor structure is not applicable to K562 | target/control audit, paper-native pseudobulk summaries, scale engineering, method input development | cell-level escapees, heterogeneous response scores, donor-aware inference |
| Synthetic demo | 360 generated cells with known guides, controls, positive effects, and null effects | real biological signal | workflow tests, routing tests, null/positive controls, output contracts, transparent pseudobulk execution | biological or Alzheimer conclusions |

## Why The Two Microglia Resources Remain

GSE178317 and GSE207628 cannot currently support guide-resolved effect estimation, but they still make a valid contribution. They test assay-aware ingestion, preserve microglial and Alzheimer context, expose missing-metadata failure modes, and support measured QC or replicate baselines. Every unavailable field remains explicitly `unknown`.

## Why Replogle Is The Perturbation-Labeled Anchor

The compact Replogle object retains guide-pair and non-targeting labels. It is therefore the only processed public object in this release that supports perturbation/control auditing. It is pseudobulk rather than cell-level, so methods requiring individual-cell response heterogeneity remain inapplicable.

## Admission Rule

Additional datasets will enter the active catalog only after the repository contains:

- a retrievable source file or generated fixture
- checksum and provenance
- a reproducible conversion or analysis command
- measured dimensions and QC
- explicit controls and assignment status
- at least one committed output used by the report or app

## Primary Sources

- Drager et al., *Nature Neuroscience* (2022), DOI: 10.1038/s41593-022-01131-4; GEO GSE178317
- Yang et al., *Nature Genetics* (2023), DOI: 10.1038/s41588-023-01506-8; GEO GSE207628
- Replogle et al., *Cell* (2022), DOI: 10.1016/j.cell.2022.05.013; Figshare+ 10.25452/figshare.plus.20029387
