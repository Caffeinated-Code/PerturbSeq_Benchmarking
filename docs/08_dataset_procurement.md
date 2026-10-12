# Dataset Procurement

The active workflow downloads only the three public resources used by the current analysis.

## Sources

| Dataset | Source | Local role |
|---|---|---|
| GSE178317 | GEO raw supplementary archive | four RNA lanes, four sgRNA-enrichment archives, expression QC and state baselines |
| GSE207628 | GEO raw matrices and HyPR-seq probe panel | targeted single-cell QC and replicate baseline |
| Replogle K562 essential | Figshare+ processed H5AD | guide-pair pseudobulk QC and author-statistic baseline |

## Reproducible Commands

```bash
python scripts/procure_public_datasets.py --include-large
python scripts/process_real_datasets.py --dataset all
python scripts/validate_real_products.py \
  --product-dir data/processed/real_data \
  --artifact-dir artifacts/real_data
```

Large raw and H5AD files remain outside Git. Compact checksums, dimensions, QC tables, status tables, and paper-native audit summaries are version controlled.

## Metadata Boundary

Downloading a matrix does not make every analysis possible. GSE178317 and GSE207628 are retained because their measured expression products support QC and biological context. Their missing guide mappings are recorded as unavailable. Replogle retains perturbation labels at pseudobulk level and therefore supports perturbation/control auditing.

## Adding A Dataset

A new source is added only after its files, checksum, conversion, QC, controls, assignment semantics, output tables, and app/report use are implemented. A citation or URL alone is not sufficient.
