# Regulatory Evidence Infrastructure

The repository contains a typed evidence model and synthetic fixtures for testing how perturbation, expression, chromatin, genetic, and clinical evidence should remain separate. It does not currently contain analyzed external Alzheimer regulatory data.

## Why The Infrastructure Remains

The synthetic track tests several safeguards:

- synthetic records cannot receive a biological evidence tier
- database overlap alone cannot be called validation
- directional conflict limits evidence strength
- perturbation, association, chromatin, QTL, motif, pathway, and clinical evidence remain distinct types
- every result requires dataset, method, contrast, sample or cell count, and provenance

## Current Outputs

| Output | Scope |
|---|---|
| `regulatory_validation.csv` | synthetic infrastructure fixture with explicit `is_synthetic=true` |
| `regulatory_validation_summary.csv` | synthetic support-status counts used to test the app |
| `validated_ad_microglia_hits.csv` | legacy filename retained for compatibility; contains synthetic examples, not validated hits |

The canonical contracts are `schemas/regulatory_evidence_schema.yml` and `schemas/app_result_contract.yml`.

## Interpretation Rule

No synthetic support score is a biological finding. No external resource is named as analyzed evidence until its records are ingested and reproducibly linked to a committed output.
