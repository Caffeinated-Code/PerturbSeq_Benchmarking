# Part 3: Move From Perturbation Results to Disease Evidence

Perturbation data can show that changing a gene alters a molecular phenotype. Disease databases answer a different question: is the gene or locus connected to human disease?

These evidence types should be combined carefully.

## Alzheimer Biology in This Project

Microglia regulate tissue surveillance, debris clearance, lipid handling, phagocytosis, and inflammatory responses. Human genetics has linked several microglial genes to Alzheimer disease.

The generated benchmark includes APOE, TREM2, INPP5D, SPI1, and CSF1R perturbations. It tracks homeostatic, interferon, lipid-handling, and SPP1-like response genes. The [Alzheimer microglia primer](../docs/02_alzheimers_microglia_primer.md) explains these programs.

The generated effects remain software controls. External evidence can establish disease relevance. It cannot convert generated effects into biological discoveries.

## The GWAS Catalog Query

The workflow queries the NHGRI-EBI GWAS Catalog API for associations mapped to benchmark candidate genes. The trait is Alzheimer disease (`MONDO_0004975`) with child traits included. The extended gene set is disabled.

Four candidates had mapped-gene associations at the prespecified genome-wide threshold of `p <= 5e-8`:

- **APOE**, a central Alzheimer risk and lipid-handling gene
- **TREM2**, a microglial lipid-sensing and phagocytic receptor
- **INPP5D**, an inhibitory regulator of myeloid signaling
- **SPI1**, a transcription factor that controls myeloid programs

SPP1 had a weaker catalogued association at `p = 4e-6`. It did not meet the project threshold.

The exact API release, genome build, dbSNP build, query rule, and representative associations are stored in the [corroboration output](../results/external_corroboration/gwas_catalog_ad_corroboration.csv).

## What GWAS Corroboration Means

A GWAS signal supports a relationship between a genomic region and disease risk. Mapping that signal to a gene creates a candidate mechanism. The nearest or overlapping gene is not always causal.

The current overlap supports prioritizing APOE, TREM2, INPP5D, and SPI1 for disease-focused perturbation work. It does not establish:

- the causal gene at each locus
- the direction of the causal effect
- a microglia-specific mechanism
- agreement with the generated fold changes
- therapeutic benefit from increasing or decreasing the target

The [external evidence guide](../docs/14_external_validation.md) records this boundary.

## A Stronger Disease-Research Path

The next study should start with guide-resolved human microglia data.

1. Select genes with human genetic support.
2. Use several guides per gene.
3. Include non-targeting and positive controls.
4. Record donor, differentiation, batch, MOI, and stimulation condition.
5. Measure target engagement before interpreting downstream states.
6. Test homeostatic, lipid, interferon, lysosomal, phagocytic, and SPP1-like programs.
7. Replicate leading effects in an independent perturbation experiment.
8. Add chromatin and QTL evidence in the correct cell context.

This sequence moves from association to mechanism. Genetics nominates a locus. Perturbation tests causality. Single-cell readouts identify the responding state. Independent data test reproducibility.

## What the Current Project Delivers

The repository now provides a traceable starting point:

- three processed public data products
- explicit limits for missing guide assignments
- assay-aware method routing
- reproducible QC and paper-native summaries
- generated positive and null tests
- a versioned GWAS corroboration table
- a public Shiny result browser
- local and AWS-ready workflow structure

The central lesson is simple. Disease relevance, perturbation response, and mechanistic validation are separate claims. A useful benchmark shows how they connect and where the evidence stops.
