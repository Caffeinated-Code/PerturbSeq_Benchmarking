# Roadmap

## Phase 1: Repository Scaffold

- Add primers
- Add dataset catalog
- Add method catalog
- Add schema
- Add demo pipeline
- Add validation checks

## Phase 2: Dataset Acquisition

- Complete: download and checksum Drager GSE178317, Yang/Shen GSE207628, and the Replogle K562 essential pseudobulk object
- Complete: convert measured expression products into the shared schema
- Complete: preserve missing guide assignments and unknown MOI as missing, rather than inferring them
- Remaining: obtain or reconstruct guide-level assignments for the two GEO microglia datasets

## Phase 3: Baseline Analyses

- Complete: dataset QC for all three processed resources
- Complete: guide-archive audit for GSE178317 and control audit for Replogle
- Complete: expression-state, targeted-replicate, and author-pseudobulk baselines
- Remaining: perturbation-level microglia baselines after guide assignments become available

## Phase 4: Method Integration

- Complete: executable adapters, compatibility checks, and lifecycle statuses for SCEPTRE, Mixscape, GSFA, PS/scMAGeCK, pertpy, and transparent pseudobulk
- Complete: synthetic positive/null fixtures and benchmark output contracts
- Remaining: install frozen upstream environments and execute eligible methods on guide-resolved real datasets

## Phase 5: Biological Interpretation

- Complete: typed evidence schema and conservative support tiers
- Complete: resource registry for SEA-AD, ROSMAP, microglia regulome, and ClinVar
- Complete: claim-traceability and app result contracts
- Remaining: ingest source-native regulatory extracts, harmonize genome builds, and run donor-aware analyses
- Remaining: compare real method findings with paper-native conclusions

## Phase 6: Scale-Out

- Add AWS Batch profile
- Add container image
- Add cost notes
- Add large-dataset sharding strategy
- Add runtime and memory benchmark table

The real-data workflow includes a local and AWS Batch execution path. Container publication, full-scale cost measurements, and sharded method runs remain open.
