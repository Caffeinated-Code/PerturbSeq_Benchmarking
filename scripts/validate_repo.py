#!/usr/bin/env python3
"""Validate repository structure and public-facing style."""

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "README.md",
    "PROJECT_SUMMARY.md",
    "configs/datasets.yml",
    "configs/methods.yml",
    "configs/benchmark.yml",
    "schemas/perturbseq_anndata_schema.yml",
    "main.nf",
    "nextflow.config",
    "docs/01_perturbseq_primer.md",
    "docs/02_alzheimers_microglia_primer.md",
    "docs/03_dataset_catalog.md",
    "docs/04_methods.md",
    "docs/05_benchmark_design.md",
    "docs/06_interpretation_guide.md",
    "docs/07_aws_scaling.md",
    "docs/08_dataset_procurement.md",
    "docs/09_outputs.md",
    "docs/10_roadmap.md",
    "docs/11_paper_native_baselines.md",
    "docs/12_regulatory_validation_track.md",
    "docs/13_method_routing.md",
    "docs/14_external_validation.md",
    "docs/15_concise_analysis_report.md",
    "docs/16_real_public_data_audit.md",
    "docs/17_app_data_contract.md",
    "docs/18_blog_series_outline.md",
    "docs/19_expert_gap_assessment.md",
    "schemas/regulatory_evidence_schema.yml",
    "schemas/app_result_contract.yml",
    "manuscript/claim_traceability.yml",
    "docs/17_real_data_engineering.md",
    "manuscript/review_paper_draft.md",
    "manuscript/revision_log.md",
    "scripts/prepare_shiny_bundle.py",
    "scripts/deploy_shinyapps.R",
    "scripts/procure_public_datasets.py",
    "scripts/process_real_datasets.py",
    "scripts/validate_real_products.py",
    "workflows/real_data.nf",
    "configs/real_datasets.yml",
    "scripts/run_analysis_modules.sh",
    "bin/analyze_gse207628_hyprseq.py",
    "bin/analyze_gse178317_abundance.py",
    "shiny/app.R",
    "shiny/README.md",
]

BLOCKED_PHRASES = [
    "not " + "only",
    "but " + "also",
    "not " + "just",
    "a strong " + "analysis",
]


def read_text(path):
    return path.read_text(encoding="utf-8", errors="ignore")


def main():
    errors = []
    for rel in REQUIRED_FILES:
        if not (ROOT / rel).exists():
            errors.append(f"Missing required file: {rel}")

    text_files = [
        path for path in ROOT.rglob("*")
        if path.is_file()
        and ".git" not in path.parts
        and path.name != "validate_repo.py"
        and path.suffix.lower() in {".md", ".yml", ".yaml", ".py", ".nf", ".txt", ".cff"}
    ]
    for path in text_files:
        rel = path.relative_to(ROOT)
        text = read_text(path).lower()
        for phrase in BLOCKED_PHRASES:
            if phrase in text:
                errors.append(f"Blocked phrase '{phrase}' found in {rel}")

    readme = read_text(ROOT / "README.md")
    for doc in [
        "docs/01_perturbseq_primer.md",
        "docs/02_alzheimers_microglia_primer.md",
        "docs/03_dataset_catalog.md",
        "docs/04_methods.md",
        "docs/05_benchmark_design.md",
        "docs/06_interpretation_guide.md",
        "docs/07_aws_scaling.md",
        "docs/08_dataset_procurement.md",
        "docs/09_outputs.md",
        "docs/10_roadmap.md",
        "docs/11_paper_native_baselines.md",
        "docs/12_regulatory_validation_track.md",
        "docs/13_method_routing.md",
        "docs/14_external_validation.md",
        "docs/15_concise_analysis_report.md",
        "docs/16_real_public_data_audit.md",
        "docs/17_app_data_contract.md",
        "docs/18_blog_series_outline.md",
        "docs/19_expert_gap_assessment.md",
        "docs/17_real_data_engineering.md",
    ]:
        if doc not in readme:
            errors.append(f"README does not link {doc}")

    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    print("Repository validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
