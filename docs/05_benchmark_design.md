# Benchmark Design

## Benchmark Goal

The goal is to compare methods by biological usefulness, statistical reliability, and scalability.

A method is useful if it helps answer a real perturbation question without hiding design caveats.

## Benchmark Questions

1. Does the method recover expected on-target knockdown or activation?
2. Does it handle non-targeting controls correctly?
3. Does it distinguish guide efficiency from downstream biology?
4. Does it detect microglial cell-state redistribution?
5. Does it recover known Alzheimer and microglia biology?
6. Does it avoid excess false positives?
7. Does it run at practical scale?

## Standard Inputs

Each dataset is converted to a common AnnData schema.

Required fields:

- cell barcode
- gene expression counts
- perturbation target
- guide identity
- non-targeting control label
- batch or replicate label
- dataset ID

Recommended fields:

- donor
- condition
- stimulation
- cell type
- cell state
- guide count
- target-gene expression
- protein counts
- chromatin features

## Baseline QC

Each dataset receives the same QC report before method-specific analysis.

| QC layer | Metrics |
|---|---|
| Cell QC | total counts, detected genes, mitochondrial fraction, doublet annotation if available |
| Guide QC | cells per guide, guides per target, guide collision rate, guide dropout |
| Perturbation QC | target expression, knockdown or activation direction, guide concordance |
| Control QC | non-targeting cell count, batch balance, donor balance |
| Design QC | perturbation coverage, condition coverage, replicate structure |

## Benchmark Metrics

### Statistical Metrics

- number of discoveries
- FDR-adjusted discoveries
- p-value calibration using negative controls
- guide-level concordance
- replicate concordance
- stability under downsampling
- covariate sensitivity

### Biological Metrics

- recovery of expected target knockdown or activation
- recovery of known pathway effects
- enrichment of Alzheimer and microglia gene sets
- agreement with paper-native findings
- detection of cell-state shifts
- consistency across guides targeting the same gene

### Scalability Metrics

- runtime
- peak memory
- disk use
- failed jobs
- cost estimate on AWS Batch
- practical maximum dataset size

## Alzheimer Microglia Gene Sets

The first interpretation layer will track:

- AD GWAS genes: TREM2, APOE, BIN1, PICALM, INPP5D, CD33, ABCA7, CR1
- microglia identity: P2RY12, CX3CR1, TMEM119, CSF1R, SPI1
- disease-associated programs: SPP1, CST7, LPL, APOE, CLEC7A, CD9
- interferon response: ISG15, IFIT1, IFIT2, IFI6, MX1
- antigen presentation: HLA-DRA, HLA-DRB1, CD74
- lysosome and phagocytosis: LAMP1, LAMP2, CTSB, CTSD, TREM2

## Method Agreement

Method agreement will be summarized at four levels:

- perturbation-level hit agreement
- gene-level effect agreement
- pathway-level agreement
- cell-state-shift agreement

Disagreement is valuable. It can reveal weak guide efficiency, cell-state-specific effects, targeted-panel limitations, or poor statistical calibration.

## Fairness Rules

- Do not force every method onto every dataset.
- Mark incompatible analyses clearly.
- Use paper-native analysis as a biological baseline.
- Use negative controls to detect false positives.
- Separate target knockdown from downstream biology.
- Report runtime and memory next to biological results.
- Keep raw conclusions linked to dataset design.

