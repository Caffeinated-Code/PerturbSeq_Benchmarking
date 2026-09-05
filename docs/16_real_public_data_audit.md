# Real Public Data Audit

This audit separates confirmed public data from analysis that requires larger compute.

## Public Files Processed

### GSE207628

GSE207628 is an Alzheimer risk-locus CRISPRi-HYPR-seq study in human iPSC-derived microglia.

Processed files:

- `GSE207628_RAW.tar`
- `GSE207628_probes_hyprseq.tsv.gz`

The raw archive contains two targeted count matrices:

- `GSM6304115_XY077-1_collapsed_filtered_emul.count_matrix.txt.gz`
- `GSM6304116_XY078-2_collapsed_filtered_emul.count_matrix.txt.gz`

The current audit reports:

- number of cells
- number of targeted features
- number of exon target genes
- number of barcode features
- median counts per cell
- median detected features
- low-depth cell fraction
- duplicate cell barcode count
- probe-panel composition

This dataset is targeted HYPR-seq, so it should not be treated like whole-transcriptome Perturb-seq. It is valuable because the panel is directly focused on Alzheimer risk-locus biology, including genes such as `TREM2`, `BIN1`, `PICALM`, `INPP5D`, and `RIN3`.

### GSE178317

GSE178317 is a human iPSC-derived microglia CROP-seq resource. The full raw archive is public and large. The current local audit uses the public abundance table to verify microglia context and sample structure.

Processed file:

- `GSE178317_iTF_Microglia_RNAseq_abundance.csv.gz`

The current audit reports:

- number of genes
- number of public abundance samples
- sample groups
- detected genes per sample
- microglia marker presence
- group with highest marker abundance

The full CROP-seq archive is recorded in the manifest and skipped by default. It should be processed through the Nextflow workflow on a workstation, HPC, or AWS Batch.

## Commands

```bash
python scripts/procure_public_datasets.py --outdir results/real_public
mkdir -p data/raw/GSE207628/extracted
tar -xf data/raw/GSE207628/GSE207628_RAW.tar -C data/raw/GSE207628/extracted
python bin/analyze_gse207628_hyprseq.py --outdir results/real_public
python bin/analyze_gse178317_abundance.py --outdir results/real_public
python scripts/prepare_shiny_bundle.py
```

The same steps can be run through the modular replication script:

```bash
bash scripts/run_analysis_modules.sh public
bash scripts/run_analysis_modules.sh bundle
```

For the full GSE178317 CROP-seq raw archive:

```bash
python scripts/procure_public_datasets.py --include-large --outdir results/real_public
nextflow run main.nf \
  -profile aws \
  --dataset_manifest configs/datasets.yml \
  --method_manifest configs/methods.yml \
  --outdir s3://your-bucket/perturbseq_benchmarking/gse178317
```

## Interpretation

The hosted Shiny app includes compact, public-derived CSV summaries. It does not bundle raw archives. This keeps the public app fast and inexpensive while preserving a clear route to larger reproducible processing.

## Sources

- GSE207628: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE207628
- GSE178317: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE178317
