# Result Product Data Contract

The app is a view over auditable result tables, not evidence that a method ran. Each numerical result must carry `result_id`, dataset, method, completed run status, contrast, sample count, cell count, provenance identifier, and synthetic flag. Planned, failed, and inapplicable methods are status records without numerical results.

The product navigation covers dataset selection, QC, design/MOI, method applicability, method comparison, biological findings, regulatory support, limitations, provenance, and downloads. A view may render only when its required columns are present. Downloaded tables preserve the same identity and provenance fields shown on screen.

For beginner readers, [Perturb-seq primer](01_perturbseq_primer.md) and [Alzheimer microglia primer](02_alzheimers_microglia_primer.md) remain clickable. Expert interpretation follows [the evidence track](12_regulatory_validation_track.md).

## Provenance record

A provenance row records source URL/accession, source version or release date, retrieval date, checksum where a file was downloaded, genome build where relevant, transformation/code version, and license/access constraints. “Unknown” is an explicit value; it is not silently inferred.

## Display safety

- Synthetic results display a persistent “infrastructure testing only” banner.
- A method with `planned`, `failed`, or `skipped_inapplicable` status cannot appear in result rankings.
- Clinical annotations remain separate from AD association and functional evidence.
- Empty evidence is displayed as “not tested” or “unavailable,” never as a negative finding.

