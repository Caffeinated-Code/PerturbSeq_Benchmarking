# External Corroboration and Evidence Boundary

## What Was Added

The current release queries the NHGRI-EBI GWAS Catalog API v2 for Alzheimer disease associations mapped to genes represented by a non-neutral synthetic benchmark effect or used as a synthetic perturbation. The committed snapshot is `results/external_corroboration/gwas_catalog_ad_corroboration.csv`. Query provenance is stored beside it.

At a prespecified genome-wide threshold of `p <= 5e-8`, GWAS Catalog corroborates Alzheimer disease locus relevance for APOE, TREM2, INPP5D, and SPI1. SPP1 has a catalogued mapped-gene association below this project's corroboration threshold and is not counted as genome-wide support. GWAS evidence does not establish that these genes caused the synthetic response, reproduce an expression-effect direction, or identify the causal gene at every associated locus.

The release still contains no analyzed external chromatin, QTL, clinical-variant, or independent perturbation matrix. The typed synthetic fixtures remain software tests only.

## Reproduce the Query

```bash
python scripts/fetch_gwas_corroboration.py
```

The query uses `MONDO_0004975`, includes child traits, disables the extended gene set, and records the GWAS Catalog data release and genome annotation builds. Association counts are database records, not independent loci or replicated experiments.

## Current Evidence Levels

| Evidence | Current source | Valid interpretation |
|---|---|---|
| microglial expression state | GSE178317 RNA matrices | measured expression-program context without guide-resolved causality |
| targeted AD-locus expression | GSE207628 HyPR-seq matrices | measured targeted-panel and replicate context without guide/cCRE effects |
| perturbation/control labels | Replogle guide-pair pseudobulk | author-deposited perturbation/control audit at pseudobulk level |
| regulatory-support demonstration | generated synthetic tables | infrastructure testing only |

## Rule For Future Evidence

An external resource is named in results only after source-native records are queried or ingested, the relevant build and context are recorded, provenance is frozen, and a reproducible output is committed. Corroboration, mechanistic validation, and perturbation replication remain separate evidence classes.
