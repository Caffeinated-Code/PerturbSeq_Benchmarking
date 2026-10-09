# Alzheimer Microglia Evidence Track

## Purpose

The RNA Perturb-seq benchmark estimates perturbation effects. This separate track asks whether independent human Alzheimer and microglia resources corroborate the cellular and regulatory context. Observational overlap is support, not causal validation.

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

## Evidence endpoints

| Endpoint | Required context | Interpretation boundary |
|---|---|---|
| Microglial expression/state specificity | donor, region, diagnosis/stage, state definition | observational relevance |
| Accessible chromatin | cell type, genome build, peak definition | element is accessible; no target or causal claim |
| AD locus/credible variant | GWAS, fine-mapping method, ancestry, credible set | disease association; no clinical pathogenicity claim |
| Peak-to-gene | link method, score/FDR, distance, cell type | probabilistic regulatory link |
| QTL | molecular trait, allele, effect, FDR/colocalization | genetic association with a molecular phenotype |
| TF motif/regulon | motif database, background, enrichment statistic | TF-family binding potential or inferred activity |
| Pathway concordance | gene set/version, statistic, direction | program-level agreement |
| Direction consistency | comparable contrast and sign convention | agreement only when contrasts are commensurate |
| Replication | independent donors/cohort/assay | robustness across independent resources |

## Evidence tiers

- **Tier A — replicated perturbation plus regulatory corroboration:** at least two independent perturbation sources, a microglia/AD-context peak-to-gene or QTL link, at least two independent observational sources, and no unresolved directional conflict.
- **Tier B — perturbation plus multi-source observational corroboration:** a completed perturbation result, at least two observational evidence classes from at least two sources, and a peak-to-gene or QTL link, without unresolved directional conflict.
- **Tier C — perturbation with limited or mixed corroboration:** a completed perturbation result that lacks the breadth required for Tier B or has directional conflict.
- **Tier D — observational context only or not assessed:** no eligible perturbation result. Database overlaps and synthetic examples remain here.

Missing support is not evidence against a perturbation result. Every tier retains the component records and their uncertainty; the tier is a compact audit aid, not a truth score.

Synthetic records are permitted only to test infrastructure and cannot receive a biological tier. The legacy additive demo score remains in bundled fixture files for backward compatibility and must be labeled `infrastructure_testing_only`.

## Outputs

| Output | Meaning |
|---|---|
| `regulatory_validation.csv` | one row per perturbation-gene effect with chromatin evidence |
| `regulatory_validation_summary.csv` | counts of PASS, WARN, and LOW_SUPPORT hits |
| `validated_ad_microglia_hits.csv` | legacy demo filename; supported examples, never proof of validation |

The canonical model is `schemas/regulatory_evidence_schema.yml`; resources and ingestion state are recorded in `configs/ad_validation_resources.yml`.

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
