# Part 2: Choose Methods the Data Can Support

Single-cell CRISPR methods answer different questions. The assay design determines which questions are valid.

This project registered eight analysis strategies. Two produced results in the current release. Six more were checked against explicit data requirements.

## The Two Executed Strategies

### Paper-native summaries

Each source study used an analysis suited to its design. The repository reproduces compact summaries when the public files contain the required fields.

For the Replogle K562 product, 2,134 targeting guide-pair pseudobulks had a target-expression statistic. Median target-expression change was -82.7%. This supports a target-level audit. It is not a new differential-expression analysis.

### Transparent pseudobulk baseline

The generated test data contain 360 cells, five perturbations, one non-targeting control, and 20 genes. The baseline compares each perturbation with the control.

It tested 100 perturbation-gene pairs. Fourteen were non-neutral. Those pairs involved 11 response genes.

The effects were built into the generated data. Recovery shows that the code follows the expected path. It does not create an Alzheimer finding.

## Six Additional Adapters

The [methods guide](../docs/04_methods.md) documents each method and its requirements.

### SCEPTRE

SCEPTRE tests perturbation-feature associations. Low-MOI and high-MOI designs require different paths. Both need guide assignments, controls, and suitable covariates.

### Perturbation-response score

PS measures response strength in individual cells. It can identify partial responders. It requires cell-level guide labels and a usable RNA response signature.

### GSFA

GSFA estimates perturbation effects on latent gene programs. It needs broad RNA coverage and several perturbations. A 49-feature panel is too narrow for this use.

### Mixscape

Mixscape separates cells that show a perturbation signature from guide-positive cells that resemble controls. It needs cell-level data, controls, and enough genes to define a local signature.

### pertpy

pertpy provides perturbation distances and scverse-compatible data handling. The selected operation still needs groups, controls, and a defined readout.

### Dataset-specific high-MOI modeling

High- or mixed-MOI data need models that account for multiple guides per cell. This route remains separate from the low-MOI route.

## Use Execution States

The repository uses explicit states:

- `RUN`: the method completed and its output passed checks.
- `INCOMPATIBLE`: the assay cannot support the method.
- `FAILED`: execution started but did not complete.
- `NOT_AVAILABLE`: the required implementation or environment is absent.

“Eligible” is not the same as “executed.” A method may fit the assay design and still lack a frozen environment or complete input object.

## What a Fair Benchmark Needs

A fair comparison uses the same biological contrast and clear endpoints.

- false-positive control under null perturbations
- recovery of known positive controls
- target knockdown or activation
- agreement across guides for the same target
- replicate consistency
- calibrated false discovery rate
- runtime and memory use
- stability across random seeds or subsamples

Methods should not be ranked by one score. Association testing, response classification, pathway modeling, and distance analysis estimate different objects.

## Main Lesson

Method selection is part of the scientific analysis. A sophisticated model cannot recover missing guide assignments or turn a targeted panel into a transcriptome-wide assay.

The final article asks how perturbation candidates can be connected to Alzheimer disease evidence without overstating validation.
