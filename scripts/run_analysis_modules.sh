#!/usr/bin/env bash
set -euo pipefail

MODULE="${1:-help}"
OUTDIR="${OUTDIR:-results/demo}"
DEMO_OUTDIR="${DEMO_OUTDIR:-demo_data}"
PROFILE="${PROFILE:-local}"
DATASET_MANIFEST="${DATASET_MANIFEST:-configs/datasets.yml}"
METHOD_MANIFEST="${METHOD_MANIFEST:-configs/methods.yml}"
METHOD="${METHOD:-simple_pseudobulk}"

usage() {
  cat <<'EOF'
Run PerturbSeq_Benchmarking analysis modules.

Usage:
  bash scripts/run_analysis_modules.sh <module>

Modules:
  demo        Create small demo expression, cell metadata, and regulatory inputs.
  nextflow    Run the reproducible Nextflow benchmark scaffold.
  public      Download and summarize lightweight public dataset files.
  bundle      Copy current result tables into the Shiny app bundle.
  validate    Run repository, output, and Shiny source checks.
  all         Run demo, nextflow, public, bundle, and validate.

Optional environment variables:
  OUTDIR=results/demo
  DEMO_OUTDIR=demo_data
  PROFILE=local
  DATASET_MANIFEST=configs/datasets.yml
  METHOD_MANIFEST=configs/methods.yml
  METHOD=simple_pseudobulk

Examples:
  bash scripts/run_analysis_modules.sh demo
  OUTDIR=results/demo bash scripts/run_analysis_modules.sh nextflow
  PROFILE=aws OUTDIR=s3://your-bucket/perturbseq/demo bash scripts/run_analysis_modules.sh nextflow
  bash scripts/run_analysis_modules.sh all
EOF
}

run_demo() {
  python scripts/make_demo_dataset.py --outdir "${DEMO_OUTDIR}"
  python scripts/make_demo_regulatory_data.py --outdir "${DEMO_OUTDIR}"
}

run_nextflow() {
  nextflow run main.nf \
    -profile "${PROFILE}" \
    --dataset_manifest "${DATASET_MANIFEST}" \
    --method_manifest "${METHOD_MANIFEST}" \
    --method "${METHOD}" \
    --outdir "${OUTDIR}"
}

run_public() {
  python scripts/procure_public_datasets.py --outdir results/real_public
  mkdir -p data/raw/GSE207628/extracted
  tar -xf data/raw/GSE207628/GSE207628_RAW.tar -C data/raw/GSE207628/extracted
  python bin/analyze_gse207628_hyprseq.py --outdir results/real_public
  python bin/analyze_gse178317_abundance.py --outdir results/real_public
}

run_bundle() {
  python scripts/prepare_shiny_bundle.py
}

run_validate() {
  python scripts/validate_repo.py
  python scripts/inspect_outputs.py
  Rscript -e 'source("shiny/app.R", local=TRUE); cat("shiny app source ok\n")'
}

case "${MODULE}" in
  demo)
    run_demo
    ;;
  nextflow)
    run_nextflow
    ;;
  public)
    run_public
    ;;
  bundle)
    run_bundle
    ;;
  validate)
    run_validate
    ;;
  all)
    run_demo
    run_nextflow
    run_public
    run_bundle
    run_validate
    ;;
  help|--help|-h)
    usage
    ;;
  *)
    echo "Unknown module: ${MODULE}" >&2
    usage >&2
    exit 2
    ;;
esac
