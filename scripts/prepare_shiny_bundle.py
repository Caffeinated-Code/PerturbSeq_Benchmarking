#!/usr/bin/env python3
"""Copy current benchmark outputs into the Shiny app bundle."""

from pathlib import Path
import shutil


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "results"
TARGET = ROOT / "shiny" / "results"

FILES = [
    "qc/dataset_qc.csv",
    "qc/guide_qc.csv",
    "qc/cell_state_summary.csv",
    "method_selection/dataset_profile.csv",
    "method_selection/method_decisions.csv",
    "method/simple_pseudobulk_effects.csv",
    "benchmark/benchmark_summary.csv",
    "regulatory_validation/regulatory_validation.csv",
    "regulatory_validation/regulatory_validation_summary.csv",
    "regulatory_validation/validated_ad_microglia_hits.csv",
    "report/demo_report.md",
    "real_public/download_manifest.csv",
    "real_public/public_dataset_provenance.csv",
    "real_public/gse207628_hyprseq_matrix_summary.csv",
    "real_public/gse207628_hyprseq_probe_panel.csv",
    "real_public/gse178317_abundance_summary.csv",
    "real_public/gse178317_sample_qc.csv",
    "real_public/gse178317_microglia_marker_context.csv",
]

REAL_DATA_FILES = [
    "real_dataset_status.csv",
    "gse178317_lane_qc.csv",
    "gse178317_guide_archive_audit.csv",
    "gse178317_state_baseline.csv",
    "gse207628_cell_qc.csv",
    "gse207628_targeted_replicate_baseline.csv",
    "replogle_k562_pseudobulk_qc.csv",
    "replogle_k562_paper_native_baseline.csv",
    "input_manifest.csv",
]


def main():
    if TARGET.exists():
        shutil.rmtree(TARGET)
    for rel in FILES:
        src = SOURCE / rel
        dst = TARGET / rel
        if not src.exists():
            raise FileNotFoundError(f"Missing benchmark output: {src}")
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
    for name in REAL_DATA_FILES:
        src = ROOT / "artifacts" / "real_data" / name
        dst = TARGET / "real_data" / name
        if not src.exists():
            raise FileNotFoundError(f"Missing real-data artifact: {src}")
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
    print(f"Prepared Shiny bundle results in {TARGET}")


if __name__ == "__main__":
    main()
