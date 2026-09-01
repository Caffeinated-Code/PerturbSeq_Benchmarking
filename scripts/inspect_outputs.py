#!/usr/bin/env python3
"""Check that demo outputs contain expected columns."""

import csv
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]

EXPECTED = {
    "results/qc/dataset_qc.csv": ["dataset_id", "n_cells", "n_genes", "design_status"],
    "results/qc/guide_qc.csv": ["guide_id", "cell_count", "status"],
    "results/qc/cell_state_summary.csv": ["perturbation", "cell_state", "fraction"],
    "results/method_selection/dataset_profile.csv": ["n_cells", "mean_guides_per_cell", "guide_collision_rate", "moi_class"],
    "results/method_selection/method_decisions.csv": ["method_id", "decision", "reason"],
    "results/method/simple_pseudobulk_effects.csv": ["method", "perturbation", "gene", "log2fc", "effect_direction"],
    "results/benchmark/benchmark_summary.csv": ["method", "n_effects", "n_ad_gene_effects", "n_microglia_state_gene_effects"],
    "results/regulatory_validation/regulatory_validation.csv": ["method", "perturbation", "gene", "regulatory_validation_score", "regulatory_validation_status"],
    "results/regulatory_validation/regulatory_validation_summary.csv": ["n_tested_effects", "n_pass", "n_warn", "n_low_support"],
    "results/regulatory_validation/validated_ad_microglia_hits.csv": ["method", "perturbation", "gene", "regulatory_validation_status"],
    "results/real_public/download_manifest.csv": ["dataset_id", "accession", "file_role", "status"],
    "results/real_public/public_dataset_provenance.csv": ["dataset_id", "accession", "biology", "readout"],
    "results/real_public/gse207628_hyprseq_matrix_summary.csv": ["dataset_id", "accession", "n_cells", "n_features"],
    "results/real_public/gse207628_hyprseq_probe_panel.csv": ["probe_name", "probe_class", "has_umi_stretch"],
    "results/real_public/gse178317_abundance_summary.csv": ["dataset_id", "accession", "n_genes", "n_samples"],
    "results/real_public/gse178317_sample_qc.csv": ["sample_id", "sample_group", "n_detected_genes"],
    "results/real_public/gse178317_microglia_marker_context.csv": ["gene", "status", "max_group"],
    "results/report/demo_report.md": [],
}


def main():
    errors = []
    for rel, columns in EXPECTED.items():
        path = ROOT / rel
        if not path.exists():
            errors.append(f"Missing output: {rel}")
            continue
        if columns:
            with open(path, newline="") as handle:
                reader = csv.DictReader(handle)
                missing = [col for col in columns if col not in (reader.fieldnames or [])]
                rows = list(reader)
            if missing:
                errors.append(f"{rel} missing columns: {', '.join(missing)}")
            if not rows:
                errors.append(f"{rel} has no rows")

    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    print("Demo output inspection passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
