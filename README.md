# PerturbSeq_Benchmarking

Benchmarking Perturb-seq analysis methods across Alzheimer-relevant microglia and public single-cell CRISPR datasets.

Public Shiny result browser: https://caffeinated-code.shinyapps.io/PerturbSeq_Benchmarking/

## Conclusion at a Glance

This release analyzes **three public datasets** and one synthetic software fixture. The public inputs contain 58,302 microglial whole-transcriptome profiles with 33,538 measured genes, 10,463 targeted AD-microglia profiles with 49 measured features, and 2,285 K562 guide-pair pseudobulks with 8,563 genes derived from 310,385 filtered cells. These feature counts overlap and must not be added as a unique-gene total.

Two analysis strategies have produced results: dataset-specific paper-native summaries and a transparent pseudobulk baseline. Six additional method adapters were evaluated for compatibility, but they did not complete a real-data head-to-head benchmark. Missing cell-to-guide assignments block perturbation-level inference in both GEO microglia deposits.

The executable synthetic benchmark tested five perturbations against 20 genes. It recovered **14 non-neutral perturbation-gene effects involving 11 response genes**. These are positive-control software results, not new biological discoveries. The real Replogle product evaluates 2,134 targeting guide-pair pseudobulks and shows a median target-expression change of -82.7%; the current compact output does not support a new gene-level significance count.

The [NHGRI-EBI GWAS Catalog](https://www.ebi.ac.uk/gwas/) independently corroborates Alzheimer disease locus relevance for **APOE, TREM2, INPP5D, and SPI1** among the benchmark candidates. This evidence supports disease prioritization. It does not validate the magnitude or direction of a perturbation response. The main research opportunity is to recover or reconstruct cell-to-guide assignments, rerun compatible methods on real microglia perturbations, and test whether genetically supported genes causally shift homeostatic, lipid-handling, inflammatory, or phagocytic states.

See the [external corroboration report](docs/14_external_validation.md) for the query, provenance, evidence boundary, and gene-level table.

## Why This Project Exists

Perturb-seq links a genetic perturbation to a single-cell molecular phenotype. It can reveal how a gene, enhancer, or regulatory program changes cell state. This matters for Alzheimer biology because many disease-associated variants act in microglia, and microglia can move between homeostatic, inflammatory, phagocytic, interferon-responsive, lipid-handling, and SPP1-like disease states.

The analysis is method-dependent. Association tests, escapee detection, latent-factor models, and distance-based workflows each emphasize a different signal. This benchmark compares those signals on shared datasets and reports where each method is reliable, fragile, or out of scope.

## Core Question

Which analysis strategies best recover credible perturbation effects, microglial state shifts, and Alzheimer-relevant regulatory biology from single-cell CRISPR datasets?

## What This Repository Will Do

- curate public Perturb-seq and scCRISPR datasets
- prioritize Alzheimer and microglia datasets
- standardize data into an AnnData-based schema
- run baseline single-cell QC and perturbation QC
- benchmark recent analysis methods
- test typed evidence and provenance safeguards with explicitly synthetic fixtures
- reproduce paper-native analyses where possible
- compare methods using statistical, biological, and scalability metrics
- summarize where each method is strong, fragile, or inappropriate

## Datasets

The first benchmark tier uses:

| Dataset | What is available | What is missing | Current use |
|---|---|---|---|
| Drager GSE178317 microglia CROP-seq | 58,302 RNA profiles across four lanes and matched sgRNA-enrichment archives | authors' consensus cell-to-guide assignments | expression QC, lane audit, and microglial state summaries |
| Yang/Shen GSE207628 AD microglia CRISPRi-HyPr-seq | 10,463 targeted profiles across two biological replicates | cell-to-guide/cCRE mapping and experimental MOI | targeted-panel QC and replicate agreement |
| Replogle K562 essential Perturb-seq | 2,285 labeled guide-pair pseudobulks covering 8,563 genes and 310,385 filtered source cells | cell-level object in the compact workflow | perturbation/control audit, paper-native summaries, and scale engineering |
| Synthetic software fixture | 360 generated cells with known guides, controls, positive effects, and null effects | real biological signal | pipeline, routing, null, and positive-control tests |

See the [Dataset Catalog](docs/03_dataset_catalog.md) for exact analytical boundaries.

## Evidence Infrastructure

The repository includes a typed evidence schema and synthetic tables that test how perturbation, expression, chromatin, genetic, and clinical evidence should remain separate. No external Alzheimer regulatory dataset is currently presented as analyzed evidence.

The infrastructure checks:

- whether synthetic records remain labeled as infrastructure tests
- whether database overlap is prevented from becoming a validation claim
- whether evidence types and provenance remain distinct
- whether directional conflicts limit evidence strength

## Methods

The initial benchmark compares:

| Method | Main use |
|---|---|
| SCEPTRE low-MOI | calibrated perturbation-gene association testing |
| perturbation-response score, PS | heterogeneous and partial perturbation response scoring |
| GSFA | pathway and latent-factor perturbation effects |
| Mixscape | perturbed vs non-perturbed cell classification |
| pertpy workflow | scverse-based perturbation distances and reusable analysis |
| paper-native analysis | original analysis strategy used by each dataset paper |

See [Methods](docs/04_methods.md).

## Repository Structure

```text
configs/      Dataset and method manifests
docs/         Primers, design notes, benchmark interpretation
schemas/      Standard AnnData schema
scripts/      Utility scripts and demo-data generator
bin/          Pipeline step scripts
workflow/     Nextflow configuration
main.nf       Reproducible benchmark workflow
```

## Quick Start

Create a small demo dataset:

```bash
python scripts/make_demo_dataset.py --outdir demo_data
python scripts/make_demo_regulatory_data.py --outdir demo_data
```

Run the local pipeline scaffold:

```bash
nextflow run main.nf \
  -profile local \
  --dataset_manifest configs/datasets.yml \
  --method_manifest configs/methods.yml \
  --outdir results/demo
```

The demo run is intentionally small. Full public datasets can be large and should be run on a workstation, HPC, or AWS Batch.

The demo pipeline writes baseline QC, perturbation effects, synthetic evidence tables, and a compact Markdown report.

Run analysis modules one step at a time:

```bash
bash scripts/run_analysis_modules.sh demo
bash scripts/run_analysis_modules.sh nextflow
bash scripts/run_analysis_modules.sh public
bash scripts/run_analysis_modules.sh bundle
bash scripts/run_analysis_modules.sh validate
```

Run the full lightweight workflow:

```bash
bash scripts/run_analysis_modules.sh all
```

Open the local result browser:

```bash
Rscript -e "shiny::runApp('shiny', host = '127.0.0.1', port = 3850)"
```

## Benchmark Philosophy

This project does not rank methods by one number. A useful benchmark asks:

- Did the method recover expected target knockdown or activation?
- Did it handle non-targeting controls correctly?
- Did it separate guide efficiency from downstream biology?
- Did it detect cell-state redistribution?
- Did it control false positives?
- Did it recover known Alzheimer and microglia biology?
- Did it scale without fragile memory use?

## Key Documentation

- [Perturb-seq Primer](docs/01_perturbseq_primer.md)
- [Alzheimer Microglia Primer](docs/02_alzheimers_microglia_primer.md)
- [Dataset Catalog](docs/03_dataset_catalog.md)
- [Methods](docs/04_methods.md)
- [Benchmark Design](docs/05_benchmark_design.md)
- [Interpretation Guide](docs/06_interpretation_guide.md)
- [AWS Scaling Plan](docs/07_aws_scaling.md)
- [Dataset Procurement](docs/08_dataset_procurement.md)
- [Benchmark Outputs](docs/09_outputs.md)
- [Roadmap](docs/10_roadmap.md)
- [Paper-Native Baselines](docs/11_paper_native_baselines.md)
- [Regulatory Evidence Infrastructure](docs/12_regulatory_validation_track.md)
- [Dataset-Aware Method Routing](docs/13_method_routing.md)
- [Evidence Boundary](docs/14_external_validation.md)
- [Concise Analysis Report](docs/15_concise_analysis_report.md)
- [Real Public Data Audit](docs/16_real_public_data_audit.md)
- [Result Product Data Contract](docs/17_app_data_contract.md)
- [Future Blog Series Editorial Brief](docs/18_blog_series_outline.md)
- [Expert Gap Assessment](docs/19_expert_gap_assessment.md)
- [Real-Data Engineering and Paper-Native Baselines](docs/17_real_data_engineering.md)
- [Manuscript Draft](manuscript/review_paper_draft.md)
- [Manuscript Revision Log](manuscript/revision_log.md)

## Status

The current release processes three public perturbation resources through reproducible, checksum-tracked workflows. GSE178317 contributes 58,302 deposited RNA profiles and an 8,000-cell lane-balanced analysis product. GSE207628 contributes 10,463 targeted HyPR-seq profiles across two biological replicates. The Replogle K562 object contains 2,285 guide-pair pseudobulks spanning 8,563 genes and summarizes 310,385 filtered source cells.

The repository also contains executable adapters and lifecycle states for SCEPTRE, Mixscape, PS/scMAGeCK, GSFA, pertpy, and transparent pseudobulk. Only transparent pseudobulk has completed in the bundled synthetic benchmark. The other adapters report `FAILED`, `NOT_AVAILABLE`, or `INCOMPATIBLE` when dependencies or dataset requirements are unmet. This is an execution framework, not yet a completed real-data head-to-head benchmark.

Two public-data limits determine the next scientific step. The GSE178317 GEO deposit lacks the authors' consensus cell-to-guide assignment table, and GSE207628 lacks a public cell-to-guide or cCRE mapping. Their current outputs are expression/QC and replicate baselines, not perturbation-effect estimates. The project no longer lists unprocessed external datasets as active resources.
