# Expert Gap Assessment

## Current strengths

The repository has a reproducible workflow scaffold, dataset-aware eligibility logic, public-file audit outputs, explicit synthetic fixtures, typed Alzheimer/microglia evidence and app contracts, conservative evidence-tier rules, and claim-traceability tests.

## Gaps blocking scientific conclusions

1. **No frozen real-data benchmark release.** Public dataset discovery/audits are not equivalent to normalized, QC-complete analysis objects.
2. **No completed head-to-head method matrix.** Eligibility is represented, but comparable methods have not all run with versioned parameters, failures, runtime, memory, and matched endpoints.
3. **No ingested external Alzheimer regulatory evidence.** The project therefore makes no chromatin, QTL, or population-genetic corroboration claim.
4. **No independent perturbation replication.** Observational chromatin, QTL, or GWAS support cannot substitute for a second perturbation experiment.
5. **Insufficient donor-aware inference.** Cell counts cannot replace biological replicate counts; pseudoreplication and donor/batch effects require dataset-specific models.
6. **Direction harmonization is incomplete.** Perturbation sign, allelic effect, disease contrast, and state-score direction need explicit comparable definitions before concordance testing.
7. **Clinical annotation is outside the current analysis.** No clinical-variant source is presented as analyzed evidence.
8. **Deployment provenance is incomplete.** A public release needs checksums, immutable source versions, code commit, environment lock, and per-table generation timestamps.

## Minimum next release gate

Complete one AD/microglia perturbation dataset end-to-end; ingest at least two independent human regulatory resources; emit contract-complete result/evidence/provenance tables; run appropriate negative controls; document every method as completed, failed, skipped, or planned; and pass scientific review of claim traceability. Until then, public language should describe a prototype and infrastructure demonstration.
