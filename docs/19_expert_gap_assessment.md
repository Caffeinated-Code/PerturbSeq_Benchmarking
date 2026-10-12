# Expert Gap Assessment

## Current Strengths

- Three public data products have checksum-tracked inputs and measured dimensions.
- Dataset routing uses assay properties rather than dataset names.
- Generated positive and null effects test the executable baseline.
- Public outputs state whether data are measured or generated.
- The GWAS Catalog query is reproducible and versioned.
- The Shiny app exposes results, provenance, and limits.

## Gaps That Limit Biological Conclusions

1. **No guide-resolved microglia analysis.** Both microglia deposits lack public cell-to-guide assignments.
2. **No real-data head-to-head benchmark.** Comparable methods have not run on the same guide-resolved dataset with matched endpoints.
3. **No independent perturbation replication.** GWAS support cannot replace a second perturbation experiment.
4. **No donor-aware perturbation inference.** Cell counts do not replace biological replicates.
5. **No external chromatin or QTL analysis.** Cell context, genome build, and direction still need harmonization.
6. **No clinical interpretation.** The project does not analyze clinical variants or treatment response.

## Next Release Gate

The next release needs one guide-resolved AD or microglia dataset. It must include controls, biological replicates, MOI, and a suitable molecular readout. Compatible methods should run with frozen versions and shared contrasts. Leading effects should then be tested in an independent perturbation dataset.
