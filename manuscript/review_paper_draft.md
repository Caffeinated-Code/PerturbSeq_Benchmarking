# Benchmarking Single-Cell CRISPR Analysis Strategies For Perturbation Biology And Alzheimer Microglia Regulatory Interpretation

## Abstract

Single-cell CRISPR screens connect genetic perturbations to molecular phenotypes at cell-level resolution. Perturb-seq and related assays have become central tools for mapping gene function, regulatory mechanisms, and cell-state control. Their analysis remains difficult because guide efficiency, partial perturbation responses, batch structure, cell-state heterogeneity, and readout modality can change the appropriate statistical model. Alzheimer disease provides a demanding use case: genetic risk is enriched in microglial regulatory programs, and perturbation effects may appear as state shifts rather than simple differential expression. This review outlines a benchmark framework for single-cell CRISPR analysis across microglia, Alzheimer risk-locus, genome-scale, multimodal, and chromatin-accessibility resources. The framework combines dataset profiling, method routing, paper-native baselines, perturbation QC, method comparison, and regulatory validation using Alzheimer brain chromatin resources. The goal is to support method choice that is statistically calibrated, biologically interpretable, and scalable.

## Introduction

Single-cell CRISPR screens measure the molecular consequence of genetic perturbation across thousands to millions of cells. These assays can identify regulators of cell identity, stress response, immune signaling, enhancer function, and disease-associated states.

The central analysis problem is design dependence. A low-MOI CRISPRi screen, a high-MOI combinatorial screen, a targeted HyPr-seq panel, a CITE-seq perturbation screen, and a single-cell ATAC perturbation assay require different assumptions. A benchmark should profile each dataset before method execution and document the rationale for each method choice.

## Alzheimer Microglia As A Benchmark Use Case

Microglia are a key cellular context for Alzheimer disease genetics. Genes such as TREM2, APOE, INPP5D, BIN1, PICALM, CD33, CSF1R, SPI1, and SPP1 connect immune signaling, lipid handling, phagocytosis, survival, and disease-associated cell states.

Perturbation analysis in microglia should track:

- direct target knockdown or activation
- guide concordance
- non-targeting control behavior
- donor and batch structure
- disease-associated state shifts
- interferon and inflammatory programs
- lipid-handling and phagocytic programs
- chromatin support for implicated genes

## Dataset Classes

The benchmark should include five dataset classes.

| Class | Example | Benchmark role |
|---|---|---|
| microglia Perturb-seq | Drager iPSC-derived microglia CROP-seq | disease-state perturbation biology |
| AD risk-locus targeted scCRISPR | Yang/Shen GSE207628 | Alzheimer regulatory genetics |
| genome-scale Perturb-seq | Replogle K562/RPE1 | scalability and statistical calibration |
| multimodal Perturb-CITE-seq | Frangieh, Papalexi | RNA/protein and perturbation classification |
| AD scATAC or multiome | SEA-AD, AD regulome | regulatory validation |

## Method Routing

Method choice should be determined from dataset profile.

Low-MOI datasets support low-MOI association testing. High-MOI or mixed-MOI datasets require models that account for guide combinations or collisions. Targeted RNA panels support focused regulatory interpretation, but do not provide whole-transcriptome signatures for module inference. Whole-transcriptome datasets support pseudobulk effects, Mixscape-style perturbation classification, latent-factor models, and perturbation-distance workflows. Chromatin datasets require peak, motif, and peak-to-gene methods.

## Benchmark Outputs

A complete benchmark should report:

- dataset QC
- guide QC
- perturbation QC
- method decisions
- effect-size tables
- false-positive checks using controls
- guide concordance
- cell-state shifts
- Alzheimer and microglia gene recovery
- regulatory validation
- runtime and memory
- method limitations

## Regulatory Validation

RNA perturbation hits should be compared with independent chromatin and population-genetic evidence. Accessible microglia peaks, peak-to-gene links, transcription-factor motifs, Alzheimer risk loci, and disease-state regulatory modules provide context for interpreting perturbation effects.

This validation is not causal proof. It tests whether a perturbation hit is plausible in the disease-relevant regulatory landscape.

## Recommendations

Dataset profiling should precede method selection. Paper-native analysis should be reproduced or adapted before newer methods are compared. Low-MOI and high-MOI designs should not be analyzed with the same assumptions. Targeted panels should be treated as targeted readouts. Chromatin validation should be reported separately from perturbation discovery.

## Limitations

Public datasets differ in guide assignment quality, donor structure, perturbation strength, readout modality, and metadata completeness. Some methods cannot be run fairly on every dataset. Alzheimer chromatin atlases are observational and cannot validate causality by themselves. These limitations should be visible in the benchmark report.

## Data And Code Availability

The benchmark framework is organized as a public repository with dataset manifests, method manifests, Nextflow workflows, validation scripts, documentation, and an RShiny result browser scaffold.

