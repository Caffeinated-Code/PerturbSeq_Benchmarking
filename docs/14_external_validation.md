# External Validation Plan

## Purpose

External validation checks whether perturbation findings are supported by independent biological resources.

## Resources

| Resource | Use |
|---|---|
| SEA-AD | Alzheimer brain cell states, microglia RNA, microglia chromatin |
| AD Knowledge Portal | human Alzheimer multi-omic studies and metadata |
| GWAS Catalog | Alzheimer risk loci and trait associations |
| ClinVar | clinically interpreted variants near candidate genes |
| Open Targets | gene-disease support and therapeutic context |
| scPerturb | prior perturbation datasets and harmonized metadata |
| PerturBase | perturbation database context and precedent |

ClinVar and GWAS Catalog are variant-level resources. Open Targets is a gene-disease and therapeutic-evidence resource. These resources should support interpretation, not replace perturbation evidence.

## Validation Questions

- Is the candidate gene expressed in disease-relevant microglia?
- Is the candidate gene linked to accessible microglial chromatin?
- Does the gene overlap Alzheimer genetic evidence?
- Are linked regulatory elements active in Alzheimer-relevant cell states?
- Has a similar perturbation been observed in another single-cell perturbation dataset?
- Does clinical or population genetics support caution or relevance?

## Output

Planned table:

| Column | Meaning |
|---|---|
| perturbation | perturbed gene or element |
| gene | affected gene |
| source | validation resource |
| evidence_type | expression, chromatin, variant, disease association, perturbation precedent |
| evidence_score | normalized score when available |
| interpretation | concise evidence summary |
| caveat | limitation of the evidence |

## Scoring Plan

External evidence should be reported by source rather than collapsed into a single universal score. A compact summary score can be added later for presentation, but the source-level evidence table should remain primary.

Recommended evidence classes:

- expression support
- chromatin support
- perturbation precedent
- population-genetic support
- clinical variant support
- therapeutic target support

