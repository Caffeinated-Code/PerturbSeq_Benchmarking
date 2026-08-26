# Paper-Native Baselines

Paper-native analysis means reproducing the analysis logic used by the dataset authors before comparing newer methods.

This prevents an unfair benchmark. A method should be compared against the question the dataset was built to answer.

## Native Baseline Matrix

| Dataset | Native analysis focus | Benchmark adaptation |
|---|---|---|
| Drager microglia CROP-seq | Seurat processing, microglia state clustering, CRISPRi knockdown differential expression, cluster proportion shifts | Reproduce state shifts and DE signatures. Compare newer methods against SPP1-like state and known regulator recovery. |
| Yang/Shen AD microglia HyPr-seq | CRISPRi of AD risk cCREs, targeted RNA response, resting versus IFN-beta stimulated microglia | Treat as targeted single-cell perturbation data. Compare compatible methods only. Prioritize enhancer-target and AD locus interpretation. |
| Replogle genome-scale Perturb-seq | pseudobulk perturbation profiles, effect-size matrices, genome-scale perturbation programs | Use as scale and effect-recovery benchmark. Run full methods on subsets if needed. |
| Frangieh Perturb-CITE-seq | multimodal RNA/protein response, context-specific immune-evasion effects | Compare RNA-only and RNA/protein summaries. Track condition-specific perturbation effects. |
| Papalexi IFN-gamma Perturb-CITE-seq | local perturbation signatures, perturbed-cell classification, IFN-gamma response | Reproduce Mixscape-style labels. Compare newer response-scoring methods against escapee detection. |

## What Counts As Reproduction

A native analysis is considered reproduced when the benchmark captures the original study's central claim at the right biological level.

Examples:

- a state-proportion result for a state-shift paper
- a target-gene response for a regulatory-element paper
- an RNA/protein effect for a multimodal paper
- a perturbation classification result for a Mixscape-style paper
- a pseudobulk effect matrix for a genome-scale paper

Exact figure recreation is useful, but it is not the main goal. The main goal is to preserve the biological question.

## Reporting Rule

Every dataset report should include:

- native analysis question
- native analysis method
- reproduced result
- agreement with benchmark methods
- disagreement and likely reason
- dataset-specific caveat

