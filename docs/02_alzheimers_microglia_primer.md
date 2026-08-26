# Alzheimer Microglia Primer

## Why Microglia Matter In Alzheimer Disease

Microglia are the resident immune cells of the brain. They survey the tissue environment, clear debris, respond to injury, remodel synapses, and coordinate inflammatory programs.

Human genetic studies have repeatedly linked Alzheimer disease risk to genes that are active in microglia or myeloid biology. This makes microglia a strong cell type for functional genomics.

Key Alzheimer and microglia genes include:

| Gene | Why it matters |
|---|---|
| TREM2 | lipid sensing, phagocytosis, disease-associated microglia programs |
| APOE | lipid handling, amyloid and tau-associated risk biology |
| INPP5D | immune signaling, inhibitory myeloid regulation |
| BIN1 | endocytosis, immune and neuronal context |
| PICALM | endocytosis and amyloid-related biology |
| CD33 | inhibitory immune receptor in myeloid cells |
| CSF1R | microglial survival and state control |
| SPI1 | myeloid transcriptional regulation |
| SPP1 | disease-associated and phagocytic microglia state marker |

## Microglial States

Microglia do not exist as one uniform population. Single-cell studies show multiple states that vary by tissue context, age, disease, stimulation, and model system.

Common state programs include:

- homeostatic microglia: P2RY12, CX3CR1, TMEM119
- interferon-responsive microglia: IFIT genes, ISG15, IFI6
- inflammatory microglia: cytokine and NF-kB-linked programs
- phagocytic microglia: lysosomal and antigen-presentation genes
- lipid-handling microglia: APOE, LPL, lipid metabolism genes
- SPP1-like disease-associated states: SPP1, CST7, CD9, CLEC7A-like programs

The exact labels vary across studies. A careful analysis should compare gene programs, not rely only on cluster names.

## Why Perturb-seq Is Useful Here

Alzheimer genetics can nominate risk loci, but risk loci do not automatically explain mechanism. Perturb-seq can help connect:

```text
variant or gene -> regulatory effect -> microglial state -> disease-relevant pathway
```

For example:

- CRISPRi can repress an enhancer near an Alzheimer risk locus.
- CRISPRi can knock down a candidate regulator.
- CRISPRa can activate a candidate gene.
- Single-cell readout can show whether the perturbation shifts inflammatory, phagocytic, lipid, or SPP1-like states.

## Model-System Caveats

Human iPSC-derived microglia are useful and scalable, but they are not the same as adult human brain microglia.

Important caveats:

- differentiation protocols can create immature or culture-adapted states
- donor genotype and batch can affect response
- monoculture lacks full brain tissue context
- stimulation conditions can dominate subtle genetic effects
- targeted panels cannot capture whole-transcriptome shifts
- CRISPRi/a effects depend on chromatin accessibility and guide design

These caveats do not weaken the project. They make the benchmark more realistic.

## Biological Readouts To Track

For Alzheimer-focused interpretation, the benchmark should track:

- target knockdown or activation
- TREM2/APOE/INPP5D/BIN1/PICALM-linked programs
- interferon response
- lipid metabolism
- phagocytosis and lysosome genes
- antigen presentation
- inflammatory cytokine programs
- homeostatic marker loss
- SPP1-like state gain or loss
- cell-state proportion shifts

