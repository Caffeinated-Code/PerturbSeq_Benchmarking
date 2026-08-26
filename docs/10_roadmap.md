# Roadmap

## Phase 1: Repository Scaffold

- Add primers
- Add dataset catalog
- Add method catalog
- Add schema
- Add demo pipeline
- Add validation checks

## Phase 2: Dataset Acquisition

- Download Drager microglia CROP-seq
- Download Yang/Shen AD microglia HyPr-seq
- Download Replogle K562 essential subset
- Add checksums and provenance
- Convert each dataset to the standard schema

## Phase 3: Baseline Analyses

- Run dataset QC
- Run guide QC
- Run pseudobulk baseline
- Reproduce paper-native summaries
- Add first benchmark report

## Phase 4: Method Integration

- Add SCEPTRE low-MOI workflow
- Add Mixscape workflow
- Add GSFA workflow
- Add PS workflow
- Add pertpy perturbation-distance workflow

## Phase 5: Biological Interpretation

- Add Alzheimer and microglia gene-set recovery
- Add state-shift analysis
- Add chromatin accessibility validation
- Add peak-to-gene and motif evidence tables
- Compare method findings to native paper conclusions
- Write dataset-specific interpretation notes

## Phase 6: Scale-Out

- Add AWS Batch profile
- Add container image
- Add cost notes
- Add large-dataset sharding strategy
- Add runtime and memory benchmark table
