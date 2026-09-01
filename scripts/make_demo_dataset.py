#!/usr/bin/env python3
"""Create a small Perturb-seq-like demo dataset."""

import argparse
import csv
import math
import random
from pathlib import Path


GENES = [
    "TREM2", "APOE", "INPP5D", "CSF1R", "SPP1", "CST7", "LPL", "P2RY12",
    "CX3CR1", "TMEM119", "ISG15", "IFIT1", "HLA-DRA", "CD74", "GAPDH",
    "ACTB", "RPLP0", "MALAT1", "LYZ", "CTSD"
]

PERTURBATIONS = [
    ("NTC", "non_targeting", "non_targeting"),
    ("TREM2", "sgTREM2", "targeting"),
    ("INPP5D", "sgINPP5D", "targeting"),
    ("CSF1R", "sgCSF1R", "targeting"),
    ("SPI1", "sgSPI1", "targeting"),
    ("APOE", "sgAPOE", "targeting"),
]


def poisson(lam):
    limit = math.exp(-lam)
    k = 0
    p = 1.0
    while p > limit:
        k += 1
        p *= random.random()
    return k - 1


def expression_for_cell(target, stimulated):
    base = {
        "TREM2": 3.0, "APOE": 5.0, "INPP5D": 4.0, "CSF1R": 5.0, "SPP1": 2.0,
        "CST7": 2.0, "LPL": 2.5, "P2RY12": 5.0, "CX3CR1": 4.5, "TMEM119": 4.0,
        "ISG15": 1.5, "IFIT1": 1.5, "HLA-DRA": 2.0, "CD74": 2.5, "GAPDH": 7.0,
        "ACTB": 7.0, "RPLP0": 6.0, "MALAT1": 8.0, "LYZ": 3.0, "CTSD": 3.0
    }
    signal = dict(base)
    if stimulated:
        for gene in ["ISG15", "IFIT1", "HLA-DRA", "CD74"]:
            signal[gene] += 3.0
    if target == "TREM2":
        signal["TREM2"] *= 0.45
        signal["APOE"] += 1.2
        signal["SPP1"] += 1.0
        signal["P2RY12"] -= 1.0
    elif target == "INPP5D":
        signal["INPP5D"] *= 0.45
        signal["ISG15"] += 1.0
        signal["IFIT1"] += 1.0
    elif target == "CSF1R":
        signal["CSF1R"] *= 0.40
        signal["SPP1"] -= 1.0
        signal["CST7"] -= 0.8
    elif target == "SPI1":
        signal["P2RY12"] -= 1.5
        signal["CX3CR1"] -= 1.0
        signal["TMEM119"] -= 1.0
    elif target == "APOE":
        signal["APOE"] *= 0.45
        signal["LPL"] -= 0.8
    return {gene: max(0, poisson(max(0.1, lam))) for gene, lam in signal.items()}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--outdir", default="demo_data")
    parser.add_argument("--cells-per-perturbation", type=int, default=60)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    random.seed(args.seed)
    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    cell_rows = []
    expression_rows = []
    for target, guide, control_type in PERTURBATIONS:
      for i in range(args.cells_per_perturbation):
        stimulated = i % 2 == 0
        cell_id = f"{guide}_{i:03d}"
        expr = expression_for_cell(target, stimulated)
        total_counts = sum(expr.values())
        detected_genes = sum(value > 0 for value in expr.values())
        state = "interferon" if stimulated else "homeostatic"
        if expr["SPP1"] >= 4:
            state = "SPP1_like"
        cell_rows.append({
            "cell_id": cell_id,
            "dataset_id": "demo_synthetic",
            "perturbation": target,
            "guide_id": guide,
            "target_gene": "" if target == "NTC" else target,
            "control_type": control_type,
            "batch": "batch_1" if i < args.cells_per_perturbation / 2 else "batch_2",
            "condition": "IFNB_stimulated" if stimulated else "resting",
            "cell_type": "microglia_like_demo",
            "cell_state": state,
            "guide_count": 1,
            "total_counts": total_counts,
            "n_genes": detected_genes,
            "pct_mito": round(random.uniform(0.01, 0.08), 4),
        })
        row = {"cell_id": cell_id}
        row.update(expr)
        expression_rows.append(row)

    with open(outdir / "demo_cells.csv", "w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(cell_rows[0].keys()))
        writer.writeheader()
        writer.writerows(cell_rows)

    with open(outdir / "demo_expression.csv", "w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["cell_id"] + GENES)
        writer.writeheader()
        writer.writerows(expression_rows)

    with open(outdir / "README.md", "w") as handle:
        handle.write("# Demo Dataset\n\n")
        handle.write("Synthetic Perturb-seq-like data for testing the benchmark scaffold.\n")


if __name__ == "__main__":
    main()
