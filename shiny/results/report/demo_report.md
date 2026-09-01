# Perturb-seq Benchmark Demo Report

## Dataset QC

- cells: 360
- genes: 20
- perturbations: 6
- design status: PASS

## Benchmark Summary

- method: simple_pseudobulk
- tested effects: 100
- non-neutral effects: 14
- Alzheimer gene effects: 4
- microglia-state gene effects: 10

## Method Selection

| Method | Decision | Reason |
|---|---|---|
| native_paper | RUN | Run the dataset-specific baseline when source-study design is available. |
| simple_pseudobulk | RUN | Requires RNA features and enough cells per perturbation. |
| sceptre_low_moi | RUN | Run only for low-MOI designs with limited guide collisions. |
| sceptre_high_moi_or_mixed_moi | SKIP | Use high-MOI or mixed-MOI association models when guide collisions are frequent. |
| mixscape | SKIP | Perturbed-cell classification is best supported by whole-transcriptome signatures. |
| gsfa | SKIP | Latent-factor models need enough transcriptome-wide signal. |
| ps | RUN | Response scoring can be used for RNA or targeted RNA with careful interpretation. |
| pertpy_distance | RUN | Use as the scverse-compatible organizing workflow for compatible objects. |
| signac_archr_chromvar_track | SKIP | Run chromatin methods only for scATAC, multiome, or peak-linked validation resources. |

## Regulatory Validation

- tested effects: 14
- PASS: 7
- WARN: 0
- LOW_SUPPORT: 7

This demo validates the benchmark scaffold. Full runs should use public datasets listed in the dataset manifest.
