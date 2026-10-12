# Project Summary

PerturbSeq_Benchmarking tests analysis choices for single-cell CRISPR data.

The project focuses on Alzheimer-relevant microglia. It also uses a large K562 Perturb-seq product to test scale and target-level summaries.

The repository provides:

- short primers on Perturb-seq and Alzheimer microglia
- provenance and checksums for public inputs
- assay-aware method routing
- expression, guide, replicate, and cell-state QC
- paper-native and transparent pseudobulk summaries
- explicit method states: `RUN`, `INCOMPATIBLE`, `FAILED`, or `NOT_AVAILABLE`
- GWAS Catalog corroboration with a strict evidence boundary
- a searchable Shiny result browser
- local, Nextflow, and AWS Batch execution paths

The project serves two audiences. Beginners can follow the primers and blog series. Computational biologists can inspect method requirements, provenance, code, and limitations.
