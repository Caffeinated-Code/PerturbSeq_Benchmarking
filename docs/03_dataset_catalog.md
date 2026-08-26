# Dataset Catalog

This project starts with datasets that are public, biologically useful, and different enough to stress-test analysis methods.

## Tier 1 Datasets

| ID | Dataset | Perturbation | Readout | Status | Role in benchmark |
|---|---|---|---|---|---|
| `drager_microglia_cropseq` | Drager et al. human iPSC-derived microglia CROP-seq | CRISPRi | scRNA-seq plus sgRNA | public | microglia disease-state anchor |
| `yang_ad_microglia_hyprseq` | Yang/Shen AD risk-locus microglia CRISPRi-HyPr-seq, GSE207628 | CRISPRi to cCREs | targeted single-cell RNA panel | public | direct Alzheimer genetics anchor |
| `replogle_k562_gwps` | Replogle et al. K562 genome-scale Perturb-seq | CRISPRi | scRNA-seq plus direct guide capture | public processed h5ad | scale benchmark |
| `frangieh_perturb_citeseq` | Frangieh et al. Perturb-CITE-seq | CRISPR perturbation | RNA plus surface protein | public | multimodal context benchmark |
| `papalexi_ifng_perturb_citeseq` | Papalexi et al. IFN-gamma Perturb-CITE-seq | CRISPR perturbation | RNA plus surface protein | public | perturbation escapee benchmark |

## Why These Datasets

### Drager et al. Microglia CROP-seq

This is the core microglia Perturb-seq dataset. The study used human iPSC-derived microglia and a CRISPRi/a platform to identify regulators of microglial survival, activation, phagocytosis, and disease-relevant cell states.

Key benchmark uses:

- target-gene knockdown review
- non-targeting control comparison
- cell-state redistribution
- SPP1-like disease-state interpretation
- microglia-specific biological validation

### Yang/Shen AD Microglia CRISPRi-HyPr-seq

This dataset directly addresses Alzheimer risk loci in microglia. It perturbs candidate cis-regulatory elements near loci such as TREM2, PICALM, BIN1, INPP5D, and SLC24A4/RIN3.

Important caveat:

This is targeted HyPr-seq rather than whole-transcriptome Perturb-seq. It should be analyzed as a targeted single-cell CRISPR readout. It is still valuable because it is close to the biological question.

Key benchmark uses:

- enhancer-to-target inference
- AD risk-locus interpretation
- resting versus stimulated microglia comparison
- targeted-panel limitations

### Replogle et al. Genome-scale Perturb-seq

This dataset is essential for testing scale. It includes processed AnnData files from genome-scale CRISPRi Perturb-seq experiments in K562 and RPE1 cells.

Key benchmark uses:

- runtime and memory benchmark
- large perturbation universe
- pseudobulk profiles
- effect-size matrix comparison
- stress-testing method scalability

### Frangieh et al. Perturb-CITE-seq

This dataset adds multimodal analysis. It includes RNA and protein readouts across immune-evasion contexts.

Key benchmark uses:

- RNA/protein concordance
- context-specific perturbation effects
- multimodal method compatibility
- condition-aware effect interpretation

### Papalexi et al. IFN-gamma Perturb-CITE-seq

This dataset is a strong Mixscape-style benchmark for distinguishing true perturbation from cells that carry a guide but look transcriptionally unperturbed.

Key benchmark uses:

- perturbation escapee detection
- local perturbation signatures
- IFN-gamma response biology
- RNA/protein validation

## Dataset Selection Rules

A dataset enters the benchmark if it has:

- public access
- cell-level expression data or processed single-cell object
- perturbation or guide assignment
- non-targeting controls
- enough cells per perturbation for at least one statistical method
- clear paper provenance

Datasets are excluded or downgraded if:

- guide assignments are missing
- controls are unclear
- access requires restricted human-subject approval
- readout is incompatible with most benchmarked methods
- metadata cannot support batch-aware analysis

## Sources

- Drager et al. 2022, Nature Neuroscience: https://www.nature.com/articles/s41593-022-01131-4
- Yang/Shen GSE207628: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE207628
- Replogle et al. processed data: https://plus.figshare.com/articles/dataset/_Mapping_information-rich_genotype-phenotype_landscapes_with_genome-scale_Perturb-seq_Replogle_et_al_2022_processed_Perturb-seq_datasets/20029387
- Frangieh et al. Broad Single Cell Portal: https://singlecell.broadinstitute.org/single_cell/study/SCP1064/multi-modal-pooled-perturb-cite-seq-screens-in-patient-models-define-novel-mechanisms-of-cancer-immune-evasion
- scPerturb resource: https://experiments.springernature.com/articles/10.1038/s41592-023-02144-y

