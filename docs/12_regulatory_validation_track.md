# Regulatory Validation Track

## Purpose

The RNA Perturb-seq benchmark identifies perturbation effects. The regulatory validation track asks whether those effects are plausible in Alzheimer and microglia chromatin context.

This track is separate from the primary Perturb-seq benchmark because many Alzheimer scATAC datasets are observational. They do not carry CRISPR perturbations. They can still validate whether a perturbation hit maps to accessible regulatory biology in the relevant cell type.

## Core Question

Do perturbation hits point to genes, enhancers, motifs, and regulatory programs that are active in Alzheimer-relevant microglia?

## Data Sources

| Source | Data type | Role |
|---|---|---|
| SEA-AD / Allen Brain Knowledge Platform | human brain snATAC-seq and multiome | Alzheimer brain chromatin context |
| AD regulome repository | ATAC-seq, QTL, peak-to-gene, regulatory modules | AD variant and enhancer interpretation |
| scPerturb ATAC files | perturbation-response chromatin features | method extension for perturbational chromatin data |
| Perturb-ATAC / CRISPR-sciATAC / Spear-ATAC-style datasets | scCRISPR plus chromatin accessibility | true perturbational chromatin benchmark when compatible data are available |

## Validation Logic

Each perturbation hit receives a regulatory validation score.

| Evidence | Weight | Interpretation |
|---|---:|---|
| Accessible microglia peak near or linked to hit gene | 30 | gene is visible in relevant regulatory space |
| Peak-to-gene link supports hit gene | 25 | chromatin signal can plausibly regulate the gene |
| Alzheimer locus or AD regulome annotation | 20 | hit connects to disease-relevant genetics or regulatory modules |
| Microglia TF motif in linked peak | 15 | effect may involve microglial transcriptional regulators |
| Disease-state or cell-state annotation | 10 | hit aligns with an Alzheimer-relevant microglial state |

Score interpretation:

- PASS: 70 or higher
- WARN: 40 to 69
- LOW_SUPPORT: below 40

LOW_SUPPORT does not mean the perturbation result is false. It means the available chromatin evidence does not strongly support the hit in the selected validation resource.

## Outputs

| Output | Meaning |
|---|---|
| `regulatory_validation.csv` | one row per perturbation-gene effect with chromatin evidence |
| `regulatory_validation_summary.csv` | counts of PASS, WARN, and LOW_SUPPORT hits |
| `validated_ad_microglia_hits.csv` | Alzheimer or microglia hits with strongest regulatory support |

## Methods To Add Later

The first implementation uses a transparent scoring baseline. Later versions should add:

- Signac peak processing
- ArchR project summaries
- chromVAR motif deviations
- Cicero or ABC-style peak-to-gene links
- motif enrichment against background peaks
- AD variant overlap
- regulon enrichment with SCENIC-style outputs

## Caveats

- Observational scATAC data validate context, not causality.
- Peak-to-gene links are probabilistic.
- Microglia annotations can vary by donor, brain region, disease stage, and protocol.
- A negative validation result can reflect missing chromatin coverage rather than a false perturbation hit.

## Sources

- SEA-AD / Allen Brain Knowledge Platform: https://knowledge.brain-map.org/data?filter.technique.name=CONTAINS~ATAC-seq
- AD regulome repository: https://compbio.mit.edu/ad_epigenome/
- scPerturb ATAC files: https://plus.figshare.com/articles/dataset/scPerturb_Single-Cell_Perturbation_Data_ATAC_files/24160968
- Single-cell CRISPR chromatin accessibility screen: https://www.nature.com/articles/s41467-021-23213-w

