# Manuscript Revision Log

## Review 1: Biological Scope

Action taken:

- Kept Alzheimer microglia as the primary biological use case.
- Added regulatory validation so RNA perturbation hits can be checked against chromatin context.
- Separated causal perturbation evidence from observational atlas evidence.

## Review 2: Method Compatibility

Action taken:

- Added dataset-aware method routing.
- Added MOI classification before SCEPTRE selection.
- Marked targeted RNA and chromatin datasets as distinct analysis classes.

## Review 3: Statistical Interpretation

Action taken:

- Added control-aware benchmark questions.
- Added guide coverage, collision rate, and cells-per-perturbation checks.
- Kept pseudobulk analysis as a transparent baseline rather than a final method choice.

## Review 4: Software Reproducibility

Action taken:

- Added Nextflow processes for method selection and regulatory validation.
- Added output inspection.
- Added repository validation.
- Added GitHub Actions checks.

## Review 5: Scientific Communication

Action taken:

- Replaced broad claims with dataset- and method-specific language.
- Added concise report structure.
- Added a searchable Shiny result browser.
- Kept synthetic-demo results separate from real-data claims.

## Review 6: Alzheimer Microglia Evidence And Product Audit

- Replaced causal-sounding validation language with evidence-conditioned regulatory corroboration.
- Added typed evidence and result-product contracts, source provenance, explicit cell type/disease state, and conservative evidence tiers.
- Removed catalog-only external resources so the active scope contains only processed data and synthetic infrastructure fixtures.
- Added claim traceability and tests preventing synthetic fixtures or database overlap from receiving biological validation status.
- Added the future three-part blog editorial brief; no blog was published.
