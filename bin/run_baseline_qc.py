#!/usr/bin/env python3
"""Run baseline QC on demo Perturb-seq-like inputs."""

import argparse
import csv
from collections import Counter, defaultdict
from pathlib import Path


def read_csv(path):
    with open(path, newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path, rows, fieldnames):
    with open(path, "w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--cells", required=True)
    parser.add_argument("--expression", required=True)
    parser.add_argument("--outdir", required=True)
    parser.add_argument("--min-cells-per-target", type=int, default=50)
    args = parser.parse_args()

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    cells = read_csv(args.cells)
    expression = read_csv(args.expression)

    target_counts = Counter(row["perturbation"] for row in cells)
    guide_counts = Counter(row["guide_id"] for row in cells)
    batch_counts = Counter(row["batch"] for row in cells)
    control_counts = Counter(row["control_type"] for row in cells)

    dataset_qc = [{
        "dataset_id": cells[0]["dataset_id"] if cells else "unknown",
        "n_cells": len(cells),
        "n_genes": len(expression[0]) - 1 if expression else 0,
        "n_perturbations": len(target_counts),
        "n_guides": len(guide_counts),
        "n_batches": len(batch_counts),
        "n_non_targeting_cells": control_counts.get("non_targeting", 0),
        "min_cells_per_target": min(target_counts.values()) if target_counts else 0,
        "design_status": "PASS" if target_counts and min(target_counts.values()) >= args.min_cells_per_target else "WARN",
    }]
    write_csv(outdir / "dataset_qc.csv", dataset_qc, list(dataset_qc[0].keys()))

    guide_rows = []
    for guide, count in sorted(guide_counts.items()):
        guide_rows.append({
            "guide_id": guide,
            "cell_count": count,
            "status": "PASS" if count >= 20 else "WARN",
        })
    write_csv(outdir / "guide_qc.csv", guide_rows, ["guide_id", "cell_count", "status"])

    state_counts = defaultdict(Counter)
    for row in cells:
        state_counts[row["perturbation"]][row["cell_state"]] += 1
    state_rows = []
    for perturbation, counts in sorted(state_counts.items()):
        total = sum(counts.values())
        for state, count in sorted(counts.items()):
            state_rows.append({
                "perturbation": perturbation,
                "cell_state": state,
                "cell_count": count,
                "fraction": round(count / total, 4) if total else 0,
            })
    write_csv(outdir / "cell_state_summary.csv", state_rows, ["perturbation", "cell_state", "cell_count", "fraction"])


if __name__ == "__main__":
    main()

