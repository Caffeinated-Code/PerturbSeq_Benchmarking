# Analysis Methods

The benchmark compares recent named methods and the original analysis strategy used by each dataset paper.

## Method Selection

Methods are selected if they are published, relevant to single-cell perturbation analysis, and useful for at least one benchmark dataset.

| Method | Year | Primary question | Best use |
|---|---:|---|---|
| SCEPTRE low-MOI | 2024 | Is a perturbation associated with expression of a gene or feature? | calibrated association testing |
| perturbation-response score, PS | 2025 | Which cells show strong or partial perturbation response? | heterogeneous response and perturbation strength |
| GSFA | 2023 | Which latent pathways or modules respond to perturbation? | pathway-level effects |
| Mixscape | 2021 | Which guide-positive cells look truly perturbed? | escapee detection and perturbation classification |
| pertpy workflow | 2025/2026 | How can perturbation effects be analyzed inside a modern scverse workflow? | reusable analysis, distances, data handling |
| Paper-native analysis | dataset-specific | What did the original study conclude using its own analysis design? | biological baseline |

## Why Paper-Native Analysis Is Included

Each dataset was designed for a specific question. The original analysis often reflects choices that generic tools do not know.

Examples:

- microglia CROP-seq: cluster proportion shifts and disease-state interpretation
- AD CRISPRi-HyPr-seq: enhancer-to-target effects in a targeted RNA panel
- genome-scale Perturb-seq: pseudobulk effect matrices and scale-aware analysis
- Perturb-CITE-seq: RNA and protein response in specific stimulation contexts

These native analyses become benchmark baselines. A new method should either reproduce them, sharpen them, or explain why it disagrees.

## Method Notes

### SCEPTRE low-MOI

SCEPTRE tests association between perturbations and molecular outcomes. It is important because low-MOI Perturb-seq data can produce false positives when sparsity, confounding, and model misspecification are ignored.

Benchmark outputs:

- perturbation-gene p-values
- FDR-adjusted discoveries
- calibration checks with non-targeting controls
- runtime and memory use

### Perturbation-Response Score, PS

PS scores heterogeneous perturbation responses at single-cell level. It is useful when cells carrying the same guide do not respond uniformly.

Benchmark outputs:

- response score distribution
- partial-response rate
- strong-response rate
- agreement with target knockdown
- agreement with downstream state shifts

### GSFA

GSFA models perturbation effects through latent factors or gene modules. This is useful for microglia because perturbations may shift inflammatory, phagocytic, interferon, lipid, or SPP1-like programs without producing a simple one-gene signal.

Benchmark outputs:

- perturbation-factor associations
- enriched gene modules
- module-level effect size
- pathway agreement with known biology

### Mixscape

Mixscape estimates local perturbation signatures and classifies cells as perturbed or non-perturbed. This helps detect escapee cells that carry a guide but resemble controls.

Benchmark outputs:

- perturbed cell fraction
- non-perturbed fraction
- guide-level escapee rate
- corrected differential expression after removing non-perturbed cells

### pertpy Workflow

pertpy is useful as a modern engineering and analysis layer. It supports perturbation-analysis workflows inside the scverse ecosystem.

Benchmark outputs:

- perturbation distances
- metadata-aware summaries
- interoperable AnnData outputs
- reusable notebooks

## Compatibility Matrix

| Dataset | SCEPTRE | PS | GSFA | Mixscape | pertpy | Native analysis |
|---|---|---|---|---|---|---|
| Drager microglia CROP-seq | yes | yes | yes | yes | yes | yes |
| Yang AD microglia HyPr-seq | limited | limited | limited | limited | yes | yes |
| Replogle K562/RPE1 | yes | yes | yes | limited by scale | yes | yes |
| Frangieh Perturb-CITE-seq | yes | yes | yes | yes | yes | yes |
| Papalexi IFN-gamma Perturb-CITE-seq | yes | yes | yes | yes | yes | yes |

Limited means the method can be run only after adapting the readout or reducing the analysis question.

## Sources

- SCEPTRE low-MOI: https://pmc.ncbi.nlm.nih.gov/articles/PMC11100084/
- SCEPTRE manual: https://timothy-barry.github.io/sceptre-book/
- PS: https://www.nature.com/articles/s41556-025-01626-9
- GSFA: https://www.nature.com/articles/s41592-023-02017-4
- Mixscape workflow context: https://www.sc-best-practices.org/conditions/perturbation_modeling.html
- pertpy: https://www.nature.com/articles/s41592-025-02909-7

