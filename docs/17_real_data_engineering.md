# Real-data engineering and paper-native baselines

This track processes three genuine public perturbation resources. Version-controlled outputs in
`artifacts/real_data/` are measurements from public files. Generated AnnData products are written
under ignored `data/processed/real_data/`; synthetic demonstrations remain under `demo_data/` and
are never combined with these results.

## Reproducible local run

```bash
python scripts/procure_public_datasets.py --include-large
mkdir -p data/raw/GSE178317/extracted data/raw/GSE207628/extracted
tar -xf data/raw/GSE178317/GSE178317_RAW.tar -C data/raw/GSE178317/extracted
tar -xf data/raw/GSE207628/GSE207628_RAW.tar -C data/raw/GSE207628/extracted
python scripts/process_real_datasets.py --dataset all
python scripts/validate_real_products.py
python -m unittest tests/test_real_data_processing.py
```

The default Dräger product is a deterministic, lane-balanced 8,000-cell subset. Use
`--drager-cells-per-lane 0` for all deposited filtered cells. The output and input manifests record
byte sizes and SHA-256 digests. The Figshare MD5 supplied by the depositor is additionally pinned in
`configs/real_datasets.yml`.

## Dataset-specific handling

### GSE178317: Dräger et al. microglia CROP-seq

The complete GEO archive contains four filtered 10x RNA matrices and four matched filtered
sgRNA-enrichment matrices. The RNA matrices measure 58,302 cells by 33,538 features, exactly matching
the GEO processing description. The paper reports one pooled screen, four 10x lanes, 81 sgRNAs
targeting 38 genes, infection below 0.15 MOI, and consensus single-guide assignment by demuxEM plus a
z-score method. It retained 28,905 consensus single-guide cells and analyzed 19,834 microglia.

The deposited sgRNA-enrichment H5 files use the transcriptome feature reference and contain no
explicit guide features. They are therefore insufficient to recreate the authors' consensus
cell-to-guide table. The converter preserves lane identity, calculates cell-level count, feature, and
mitochondrial QC, and writes `guide_id`, `perturbation`, and `control_type` as `unknown`. It does not
use the reported low MOI as a substitute for measured guide calls.

The available paper-native baseline is a lane-stratified score audit for the homeostatic, chemokine,
interferon, SPP1-associated disease, and proliferative programs described in the paper. It is an
expression-state baseline, not a perturbation-effect reproduction. A perturbation-level reproduction
requires the original guide-calling output or reprocessing of the SRA reads with the 81-guide library.

### GSE207628: Yang et al. AD microglia CRISPRi-HyPR-seq

The archive contains two independent differentiation replicates totaling 10,463 cells and 49 measured
features: 20 targeted RNA probes and 29 assay-barcode probes. HyPR-seq is a targeted readout, so the
workflow deliberately omits whole-transcriptome metrics such as highly variable genes, transcriptome
PCA, or genome-wide differential expression. Cell QC uses total targeted counts, detected probes, and
targeted-expression counts. The baseline reports per-target mean abundance and Spearman agreement
between the two biological replicates.

The GEO record establishes WTC11 iPSC-derived microglia, two independent differentiations, CRISPRi of
candidate regulatory elements at five AD loci, hg19 processing, and targeted HyPR-seq. Neither the
GEO matrix nor the probe file supplies a cell-barcode-to-guide/cCRE mapping or an experimental MOI.
Those fields therefore remain `unknown`; barcode-probe counts are not promoted to guide identities.
This prevents an unsupported enhancer-to-gene contrast.

### Replogle K562 essential-scale Perturb-seq

The processed object is the authors' raw guide-pair pseudobulk, not their 10 GB single-cell object. It
contains 2,285 guide-pair rows by 8,563 expression features and summarizes 310,385 filtered cells.
The converter preserves all author-supplied QC, marks the observation type as
`guide_pair_pseudobulk`, parses target and non-targeting labels from the source row identifiers, and
records all source-labeled non-targeting pairs as controls and preserves the stricter deposited
`core_control` flag separately as `benchmark_control`.

The paper-native baseline reports target-expression change, source energy-test significance, and
cells per targeting guide pair. These are audit summaries of author-derived pseudobulk statistics.
Cell-level guide QC and donor analyses are impossible from this smaller object. The full-scale route
uses the 10 GB raw single-cell file listed in Figshare+ article 20029387.

## Full-scale workstation or AWS Batch run

The Nextflow workflow accepts the two GEO archives and Replogle pseudobulk file as staged inputs:

```bash
nextflow run workflows/real_data.nf -profile local \
  --drager_cells_per_lane 0 \
  --outdir results/real_data_full
```

For AWS Batch, upload source files to a shared filesystem or S3-mounted staging location, set the
queue, region, and work directory, and override the file parameters:

```bash
export AWS_BATCH_QUEUE=your-queue
export AWS_REGION=us-west-2
export PERTURBSEQ_WORKDIR=s3://your-bucket/perturbseq/work
nextflow run workflows/real_data.nf -profile real_awsbatch \
  --gse178317_archive /shared/GSE178317_RAW.tar \
  --gse207628_archive /shared/GSE207628_RAW.tar \
  --replogle_file /shared/K562_essential_raw_bulk_01.h5ad \
  --drager_cells_per_lane 0 \
  --outdir s3://your-bucket/perturbseq/results
```

The process requests 8 CPUs, 48 GB RAM, and 12 hours. Reprocessing raw SRA reads for missing guide
assignments is outside this deposited-matrix workflow and must pin the source guide library before
guide calls are accepted.

## Primary sources

- Dräger et al., *Nature Neuroscience* (2022), DOI: 10.1038/s41593-022-01131-4; GEO GSE178317.
- Yang et al., *Nature Genetics* (2023), DOI: 10.1038/s41588-023-01506-8; GEO GSE207628.
- Replogle et al., *Cell* (2022), DOI: 10.1016/j.cell.2022.05.013; Figshare+ 10.25452/figshare.plus.20029387.

Claims about assay design, controls, MOI, replicate structure, and source processing are restricted to
these primary articles, their GEO SOFT records, and the author-deposited Figshare object.
