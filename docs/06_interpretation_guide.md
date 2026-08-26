# Interpretation Guide

## How To Read A Perturb-seq Result

A perturbation result has three layers.

| Layer | Question |
|---|---|
| Perturbation quality | Did the guide produce the expected molecular change? |
| Cellular response | Did the cell move into a different transcriptional state? |
| Biological meaning | Does the response explain a pathway, disease state, or target hypothesis? |

## Common Patterns

### Strong On-target And Strong Downstream Response

This is the cleanest case.

Expected signs:

- target gene decreases after CRISPRi or increases after CRISPRa
- multiple guides agree
- perturbed cells separate from controls
- downstream genes or pathways are coherent
- effect is reproducible across batches or donors

### Weak On-target But Strong Downstream Response

This needs caution.

Possible explanations:

- target expression is poorly captured
- the perturbation affects a regulatory element rather than a transcript
- the response is driven by an off-target guide
- the response is batch-confounded
- the target acts through a small early change amplified downstream

### Strong On-target But Weak Downstream Response

This may still be biologically meaningful.

Possible explanations:

- the gene is not active in that cell state
- the pathway is buffered
- the readout time point is wrong
- the perturbation affects function rather than transcription
- the effect requires stimulation or co-culture context

### Cell-State Redistribution

Some perturbations do not change every cell in the same way. They change the frequency of states.

For microglia, this is central. A perturbation may increase or deplete:

- homeostatic states
- interferon-responsive states
- inflammatory states
- phagocytic states
- SPP1-like states

This should be evaluated with cluster/state proportion models and marker-gene programs.

## Alzheimer Microglia Interpretation

A strong Alzheimer-focused finding should connect at least two of these:

- AD genetic locus or candidate gene
- direct perturbation evidence
- target-gene effect
- microglial state shift
- disease-relevant pathway
- consistency with human brain single-cell data
- plausible therapeutic direction

Example interpretation:

```text
CSF1R perturbation changes the abundance of SPP1-like microglia and shifts phagocytic/lysosomal programs. This supports a role for survival and state-control signaling in disease-relevant microglial heterogeneity.
```

## Red Flags

- one guide drives the entire effect
- non-targeting controls are unbalanced by batch
- the target gene is not expressed or not captured
- perturbation has too few cells
- guide collision rate is high
- batch explains more variance than perturbation
- only highly abundant genes are detected in a targeted panel
- method reports many discoveries from negative controls

## What To Report

For every hit, report:

- perturbation target
- guide count
- cells per guide
- target knockdown or activation
- effect size
- FDR or confidence score
- affected genes or modules
- affected cell state
- method agreement
- paper-native agreement
- caveats

