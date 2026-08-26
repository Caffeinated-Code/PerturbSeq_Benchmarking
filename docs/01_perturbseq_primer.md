# Perturb-seq Primer

## What Is Perturb-seq?

Perturb-seq combines pooled CRISPR perturbation with single-cell RNA sequencing.

Each cell receives one or more guide RNAs. The guide tells us which gene or regulatory element was perturbed. The single-cell transcriptome tells us how the cell responded.

This makes Perturb-seq useful for asking causal questions:

- What happens when this gene is knocked down?
- Which genes control a cell state?
- Which enhancers regulate which target genes?
- Which perturbations shift cells into disease-like states?
- Which perturbations reverse an unwanted state?

## What Data Come Out?

A typical Perturb-seq dataset has three linked data types.

| Data | What it contains |
|---|---|
| Gene expression matrix | genes by cells, usually UMI counts |
| Guide assignment table | guide RNA detected in each cell |
| Cell metadata | batch, sample, donor, condition, cell type, QC metrics |

Some datasets also include surface protein counts, chromatin accessibility, imaging, or targeted RNA panels.

## CRISPRi, CRISPRa, and Knockout

| Perturbation type | Mechanism | Common interpretation issue |
|---|---|---|
| CRISPR knockout | cuts DNA and disrupts gene sequence | editing may be incomplete; essential genes may deplete cells |
| CRISPRi | represses transcription without cutting DNA | knockdown strength varies by guide and target expression |
| CRISPRa | activates transcription | response depends on chromatin state and promoter accessibility |

For microglia and Alzheimer biology, CRISPRi and CRISPRa are especially useful because many disease variants affect regulation rather than protein sequence.

## Why Analysis Is Hard

Perturb-seq is powerful, but several problems can distort conclusions.

| Problem | Why it matters |
|---|---|
| Guide efficiency | some guides produce weak knockdown or activation |
| Escapee cells | cells can carry a guide but show no detectable perturbation effect |
| Low target expression | true knockdown can be hard to measure when the target is rarely captured |
| Batch and donor effects | technical or biological covariates can mimic perturbation effects |
| Cell-state heterogeneity | a perturbation may affect only one state or shift state abundance |
| Cell viability | perturbations can remove cells before sequencing |
| Multiple testing | thousands of perturbation-gene tests can inflate false positives |

## What Good Analysis Should Report

A strong Perturb-seq analysis should include:

- cells per perturbation
- guides per target
- non-targeting control balance
- guide assignment confidence
- perturbation efficiency
- batch and donor structure
- target knockdown or activation
- differential expression
- cell-state shifts
- pathway or gene-module effects
- method assumptions
- false discovery control
- runtime and memory use

## Beginner Mental Model

Think of each perturbation as a controlled nudge to the cell. The analysis asks whether cells receiving that nudge move in a consistent molecular direction compared with non-targeting controls.

Different methods define the movement differently. Some look gene by gene. Some look at whole expression profiles. Some look at latent pathways. Some ask whether a cell was truly perturbed before testing downstream biology.

