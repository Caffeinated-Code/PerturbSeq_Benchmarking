# Evidence Boundary

The current release does not claim external Alzheimer regulatory validation. No external chromatin, QTL, population-genetic, or clinical-variant matrix is bundled as analyzed evidence.

The repository retains a typed evidence schema and synthetic fixtures to test software behavior. These fixtures demonstrate how future evidence could be represented without implying that a named external resource was analyzed.

## Current Evidence Levels

| Evidence | Current source | Valid interpretation |
|---|---|---|
| microglial expression state | GSE178317 RNA matrices | measured expression-program context without guide-resolved causality |
| targeted AD-locus expression | GSE207628 HyPR-seq matrices | measured targeted-panel and replicate context without guide/cCRE effects |
| perturbation/control labels | Replogle guide-pair pseudobulk | author-deposited perturbation/control audit at pseudobulk level |
| regulatory-support demonstration | generated synthetic tables | infrastructure testing only |

## Rule For Future Evidence

An external resource will be named in results only after source-native records are ingested, genome build and cell context are recorded, provenance is frozen, and at least one reproducible output is used by the analysis. Until then, it is outside the active project scope.
