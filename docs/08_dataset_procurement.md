# Dataset Procurement Plan

This benchmark starts with processed public data when possible. Raw FASTQ processing is optional and should be reserved for reproducibility checks or guide-assignment audits.

## Procurement Strategy

1. Record source, accession, publication, license, and access date.
2. Prefer processed h5ad, h5, mtx, or Seurat objects with cell-level metadata.
3. Keep raw downloads out of Git.
4. Store large files under `data/raw/` or S3.
5. Convert every dataset into the common AnnData schema.
6. Write a provenance table with checksums.

## Dataset-Specific Notes

### Drager Microglia CROP-seq

Primary source:

- publication: https://www.nature.com/articles/s41593-022-01131-4
- data commons mentioned by paper: https://www.crisprbrain.org/
- lab resources: https://kampmannlab.ucsf.edu/resources

Expected work:

- locate Seurat object or count matrix
- extract guide assignment metadata
- retain original cluster/state labels if available
- preserve non-targeting control annotations
- reproduce cluster proportion analysis as native baseline

### Yang/Shen AD Microglia CRISPRi-HyPr-seq

Primary source:

- GEO: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE207628

Expected work:

- download processed supplementary files
- parse probe panel and targeted counts
- treat as targeted single-cell CRISPR readout
- benchmark only compatible methods
- retain resting and IFN-beta stimulated conditions

### Replogle Genome-Scale Perturb-seq

Primary source:

- processed AnnData files: https://plus.figshare.com/articles/dataset/_Mapping_information-rich_genotype-phenotype_landscapes_with_genome-scale_Perturb-seq_Replogle_et_al_2022_processed_Perturb-seq_datasets/20029387

Expected work:

- start with K562 essential-scale subset for development
- use genome-scale K562 for scalability tests
- avoid loading full data into memory unnecessarily
- run method subsets by perturbation or gene block

### Frangieh Perturb-CITE-seq

Primary source:

- Broad Single Cell Portal: https://singlecell.broadinstitute.org/single_cell/study/SCP1064/

Expected work:

- retrieve RNA and protein modalities
- preserve condition and co-culture metadata
- benchmark RNA-only and multimodal summaries separately
- include paper-native context-specific interpretation

### Papalexi IFN-gamma Perturb-CITE-seq

Expected work:

- locate processed Seurat or AnnData object
- retain perturbation classification metadata if present
- reproduce Mixscape-style local perturbation signatures
- compare perturbed-cell calls to newer response-scoring methods

## Provenance Table

Every converted dataset should produce:

| Field | Meaning |
|---|---|
| dataset_id | internal dataset ID |
| source_url | source page or DOI |
| accession | GEO, SCP, Figshare, Zenodo, or other accession |
| download_date | local download date |
| file_name | downloaded file |
| file_size_bytes | file size |
| sha256 | checksum |
| license | data license if stated |
| conversion_script | script used to standardize data |

## Access Caveats

Some portals require manual login, click-through terms, or controlled-access approval. Those files should be documented clearly and excluded from automated public CI.

