#!/usr/bin/env python3
"""Run a lightweight benchmark method placeholder on demo inputs."""

import argparse
import csv
import math
from pathlib import Path


def read_csv(path):
    with open(path, newline="") as handle:
        return list(csv.DictReader(handle))


def mean(values):
    values = [float(v) for v in values]
    return sum(values) / len(values) if values else float("nan")


def log2fc(target_mean, control_mean):
    return math.log2((target_mean + 1.0) / (control_mean + 1.0))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--cells", required=True)
    parser.add_argument("--expression", required=True)
    parser.add_argument("--method", default="simple_pseudobulk")
    parser.add_argument("--outdir", required=True)
    args = parser.parse_args()

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    cells = {row["cell_id"]: row for row in read_csv(args.cells)}
    expression = read_csv(args.expression)
    genes = [g for g in expression[0].keys() if g != "cell_id"]
    ntc_cells = [row for row in expression if cells[row["cell_id"]]["control_type"] == "non_targeting"]
    perturbations = sorted(set(row["perturbation"] for row in cells.values()) - {"NTC"})

    rows = []
    for perturbation in perturbations:
        pert_cells = [row for row in expression if cells[row["cell_id"]]["perturbation"] == perturbation]
        for gene in genes:
            fc = log2fc(mean(row[gene] for row in pert_cells), mean(row[gene] for row in ntc_cells))
            rows.append({
                "method": args.method,
                "perturbation": perturbation,
                "gene": gene,
                "log2fc": round(fc, 4),
                "effect_direction": "up" if fc > 0.25 else "down" if fc < -0.25 else "neutral",
            })

    with open(outdir / f"{args.method}_effects.csv", "w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["method", "perturbation", "gene", "log2fc", "effect_direction"])
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    main()

