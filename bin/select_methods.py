#!/usr/bin/env python3
"""Profile a perturbation dataset and recommend compatible analyses."""

import argparse
import csv
from collections import Counter
from pathlib import Path


def read_csv(path):
    with open(path, newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path, rows, fields):
    with open(path, "w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def number(value, default=0.0):
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def status(enabled, reason):
    return "RUN" if enabled else "SKIP", reason


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--cells", required=True)
    parser.add_argument("--expression", required=True)
    parser.add_argument("--modality", default="RNA")
    parser.add_argument("--outdir", required=True)
    args = parser.parse_args()

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    cells = read_csv(args.cells)
    expression = read_csv(args.expression)

    n_cells = len(cells)
    n_genes = len(expression[0]) - 1 if expression else 0
    guide_counts = [number(row.get("guide_count", 1), 1) for row in cells]
    mean_guides_per_cell = sum(guide_counts) / len(guide_counts) if guide_counts else 0
    collision_rate = sum(count > 1 for count in guide_counts) / len(guide_counts) if guide_counts else 0
    perturbation_counts = Counter(row.get("perturbation", "unknown") for row in cells)
    min_cells_per_perturbation = min(perturbation_counts.values()) if perturbation_counts else 0
    modalities = {args.modality.lower()}
    if any("protein" in key.lower() for key in cells[0].keys()) if cells else False:
        modalities.add("protein")

    is_low_moi = mean_guides_per_cell <= 1.2 and collision_rate <= 0.15
    is_high_moi = mean_guides_per_cell > 1.2 or collision_rate > 0.15
    is_targeted = n_genes < 500
    has_rna = "rna" in args.modality.lower() or "targeted" in args.modality.lower()
    has_chromatin = "atac" in args.modality.lower() or "chromatin" in args.modality.lower()

    profile = [{
        "n_cells": n_cells,
        "n_features": n_genes,
        "n_perturbations": len(perturbation_counts),
        "min_cells_per_perturbation": min_cells_per_perturbation,
        "mean_guides_per_cell": round(mean_guides_per_cell, 4),
        "guide_collision_rate": round(collision_rate, 4),
        "moi_class": "low_moi" if is_low_moi else "high_or_mixed_moi",
        "readout_class": "targeted" if is_targeted else "whole_transcriptome",
        "modality": args.modality,
    }]
    write_csv(outdir / "dataset_profile.csv", profile, list(profile[0].keys()))

    decisions = []
    decision, reason = status(True, "Run the dataset-specific baseline when source-study design is available.")
    decisions.append({"method_id": "native_paper", "decision": decision, "reason": reason})
    decision, reason = status(has_rna and min_cells_per_perturbation >= 20, "Requires RNA features and enough cells per perturbation.")
    decisions.append({"method_id": "simple_pseudobulk", "decision": decision, "reason": reason})
    decision, reason = status(has_rna and is_low_moi and min_cells_per_perturbation >= 20, "Run only for low-MOI designs with limited guide collisions.")
    decisions.append({"method_id": "sceptre_low_moi", "decision": decision, "reason": reason})
    decision, reason = status(has_rna and is_high_moi and min_cells_per_perturbation >= 20, "Use high-MOI or mixed-MOI association models when guide collisions are frequent.")
    decisions.append({"method_id": "sceptre_high_moi_or_mixed_moi", "decision": decision, "reason": reason})
    decision, reason = status(has_rna and not is_targeted and min_cells_per_perturbation >= 20, "Perturbed-cell classification is best supported by whole-transcriptome signatures.")
    decisions.append({"method_id": "mixscape", "decision": decision, "reason": reason})
    decision, reason = status(has_rna and not is_targeted and min_cells_per_perturbation >= 20, "Latent-factor models need enough transcriptome-wide signal.")
    decisions.append({"method_id": "gsfa", "decision": decision, "reason": reason})
    decision, reason = status(has_rna and min_cells_per_perturbation >= 20, "Response scoring can be used for RNA or targeted RNA with careful interpretation.")
    decisions.append({"method_id": "ps", "decision": decision, "reason": reason})
    decision, reason = status(True, "Use as the scverse-compatible organizing workflow for compatible objects.")
    decisions.append({"method_id": "pertpy_distance", "decision": decision, "reason": reason})
    decision, reason = status(has_chromatin, "Run chromatin methods only for scATAC, multiome, or peak-linked validation resources.")
    decisions.append({"method_id": "signac_archr_chromvar_track", "decision": decision, "reason": reason})

    write_csv(outdir / "method_decisions.csv", decisions, ["method_id", "decision", "reason"])


if __name__ == "__main__":
    main()
