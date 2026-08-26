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
    "results/method/simple_pseudobulk_effects.csv": ["method", "perturbation", "gene", "log2fc", "effect_direction"],
    "results/benchmark/benchmark_summary.csv": ["method", "n_effects", "n_ad_gene_effects", "n_microglia_state_gene_effects"],
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

