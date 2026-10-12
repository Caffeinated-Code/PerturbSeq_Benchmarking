# Evidence-Type Tests

The project keeps perturbation, expression, chromatin, genetic, and clinical evidence in separate fields. Generated records test these rules. They are not biological findings.

## Rules Tested

- Generated records cannot receive a biological evidence tier.
- Database overlap alone is not validation.
- Conflicting effect directions reduce evidence strength.
- Each result records its dataset, method, contrast, sample or cell count, and provenance.
- Association evidence stays separate from causal perturbation evidence.

## Generated Outputs

| Output | Purpose |
|---|---|
| `regulatory_validation.csv` | tests typed evidence fields; every row has `is_synthetic=true` |
| `regulatory_validation_summary.csv` | tests support-status counts in the app |
| `validated_ad_microglia_hits.csv` | legacy filename; contains generated examples, not validated hits |

The formal schemas are `schemas/regulatory_evidence_schema.yml` and `schemas/app_result_contract.yml`.

## Real External Evidence

GWAS Catalog is the only external evidence source analyzed in this release. Its output is stored under `results/external_corroboration/`. It supports Alzheimer disease locus relevance. It does not validate perturbation direction or causality.
