# PerturbSeq_Benchmarking

Benchmarking Perturb-seq analysis methods across Alzheimer-relevant microglia and public single-cell CRISPR datasets.

Public Shiny result browser: https://caffeinated-code.shinyapps.io/PerturbSeq_Benchmarking/

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
- validate RNA perturbation hits against chromatin accessibility evidence
- reproduce paper-native analyses where possible
- compare methods using statistical, biological, and scalability metrics
- summarize where each method is strong, fragile, or inappropriate

## Datasets

The first benchmark tier uses:

| Dataset | Biology | Readout | Why it matters |
|---|---|---|---|
| Drager et al. iPSC-derived microglia CROP-seq | human microglia disease states | scRNA-seq plus guides | strongest microglia perturbation anchor |
| Yang/Shen AD microglia CRISPRi-HyPr-seq, GSE207628 | Alzheimer risk loci in microglia | targeted single-cell RNA panel | direct AD genetics anchor |
| Replogle et al. genome-scale Perturb-seq | K562 and RPE1 CRISPRi | scRNA-seq plus direct guide capture | scale and statistical benchmark |
| Frangieh et al. Perturb-CITE-seq | melanoma immune evasion | RNA plus surface protein | multimodal and context-aware benchmark |
| Papalexi et al. IFN-gamma Perturb-CITE-seq | immune signaling | RNA plus surface protein | perturbation escapee and Mixscape benchmark |
| SEA-AD and AD regulome resources | Alzheimer brain and microglia chromatin | snATAC-seq or multiome | regulatory validation track |

See [Dataset Catalog](docs/03_dataset_catalog.md).

## Regulatory Validation Track

Perturb-seq identifies genes and pathways affected by perturbation. The regulatory validation track asks whether those hits are supported by Alzheimer or microglia chromatin evidence.

It checks:

- whether hit genes map to accessible peaks in microglia
- whether peaks overlap Alzheimer risk loci or candidate regulatory elements
- whether linked peaks carry microglia-relevant TF motifs
- whether perturbation hits align with disease-state regulatory programs
- whether RNA-only findings remain plausible in a chromatin context

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

The demo pipeline writes baseline QC, perturbation effects, regulatory validation tables, and a compact Markdown report.

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
- [Regulatory Validation Track](docs/12_regulatory_validation_track.md)
- [Dataset-Aware Method Routing](docs/13_method_routing.md)
- [External Validation Plan](docs/14_external_validation.md)
- [Concise Analysis Report](docs/15_concise_analysis_report.md)
- [Real Public Data Audit](docs/16_real_public_data_audit.md)
- [Manuscript Draft](manuscript/review_paper_draft.md)
- [Manuscript Revision Log](manuscript/revision_log.md)

## Status

This repository currently contains a runnable demo benchmark, dataset-aware method routing, regulatory validation, a public Shiny result browser, real public data provenance, and first-pass public dataset audits. Full raw CROP-seq processing remains the heavier Nextflow and AWS Batch path.
