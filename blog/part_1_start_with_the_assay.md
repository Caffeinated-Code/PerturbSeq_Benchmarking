# Part 1: Start With the Assay, Not the Algorithm

Perturb-seq joins a genetic perturbation to a single-cell molecular readout. A guide RNA identifies the intended perturbation. RNA counts show how the cell responded. This sounds simple. The analysis depends on several design details that are easy to miss.

This project began with a practical question: which public datasets can support a fair comparison of single-cell CRISPR analysis methods?

## What a Perturb-seq Dataset Needs

A useful dataset needs four connected pieces:

1. A cell-by-feature matrix.
2. A cell-to-guide assignment table.
3. Control labels.
4. Experimental metadata, including replicate, batch, condition, and guide multiplicity.

The [Perturb-seq primer](../docs/01_perturbseq_primer.md) explains each component.

The cell-to-guide table is essential. Without it, the RNA profile cannot be linked to a perturbation. The matrix can still support expression QC, cell-state analysis, or replicate checks. It cannot support a guide-versus-control effect estimate.

## Three Public Data Products

The project processed three public resources.

### GSE178317: microglia CROP-seq

The deposit contains 58,302 RNA profiles across four lanes and 33,538 genes. It also contains guide-enrichment archives. The authors' final cell-to-guide assignments are not present.

The current workflow therefore measures lane quality, count depth, mitochondrial fraction, and microglial state programs. It does not estimate perturbation effects.

### GSE207628: AD microglia CRISPRi-HyPR-seq

This dataset contains 10,463 cells from two biological differentiations. The readout has 49 targeted features. The public files do not connect each cell to its guide or candidate regulatory element. Experimental MOI is also unavailable.

The workflow checks panel coverage and replicate agreement. It does not assign enhancer effects. A targeted panel also cannot support methods that require a whole-transcriptome response signature.

### Replogle K562 Perturb-seq

The compact product contains 2,285 guide-pair pseudobulks across 8,563 genes. These profiles summarize 310,385 filtered cells. Target and non-targeting labels are available.

A [pseudobulk profile](../docs/01_perturbseq_primer.md) aggregates cells within a group. It is useful for target-level summaries. It does not preserve cell-to-cell response variation.

## Why MOI Matters

[Multiplicity of infection](../docs/05_benchmark_design.md) describes how many viral particles reach each cell. Low-MOI experiments usually aim for one guide per cell. High-MOI experiments place several guides in the same cell.

The distinction changes the statistical model. A low-MOI method should not be applied to a high-MOI design without modeling guide collisions. Unknown MOI should remain unknown. It should not be inferred from the name of the assay.

## What the Data Audit Changed

The original project plan included more datasets and more methods. File inspection narrowed the valid scope.

- Two microglia resources support measured QC and biological context.
- One K562 resource supports perturbation-labeled pseudobulk analysis.
- A generated dataset tests software behavior.
- Missing guide assignments block real microglia perturbation inference.

This is a useful result. A good benchmark reports when a dataset cannot answer the planned question.

## Practical Checklist

Before choosing a method, ask:

- Are guide assignments available at cell level?
- Are non-targeting controls present?
- Are biological replicates identified?
- Is MOI measured?
- Is the readout targeted or transcriptome-wide?
- Are raw counts available?
- Can the published dimensions be reproduced?

The next article uses these answers to choose methods.
