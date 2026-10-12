#!/usr/bin/env python3
"""Create a measured dataset profile and auditable method-routing decisions."""
import argparse, csv
from collections import Counter
from pathlib import Path

METHODS = ("native_paper", "transparent_pseudobulk", "sceptre_low_moi", "sceptre_high_moi_or_mixed_moi", "mixscape", "ps", "gsfa", "pertpy_distance")

def read_csv(path):
    with open(path, newline="") as handle: return list(csv.DictReader(handle))

def write_csv(path, rows, fields):
    with open(path, "w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n"); writer.writeheader(); writer.writerows(rows)

def num(value, default=0.0):
    try: return float(value)
    except (TypeError, ValueError): return default

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--cells", required=True); p.add_argument("--expression", required=True)
    p.add_argument("--modality", default="RNA")
    p.add_argument("--readout-class", choices=("auto", "targeted", "whole_transcriptome"), default="auto")
    p.add_argument("--native-baseline", default=""); p.add_argument("--outdir", required=True)
    args = p.parse_args(); outdir = Path(args.outdir); outdir.mkdir(parents=True, exist_ok=True)
    cells, expression = read_csv(args.cells), read_csv(args.expression)
    fields = set(cells[0]) if cells else set(); n_features = max(0, len(expression[0]) - 1) if expression else 0
    guide_counts = [num(r.get("guide_count", 1), 1) for r in cells]
    mean_guides = sum(guide_counts) / len(guide_counts) if guide_counts else 0
    collision = sum(x > 1 for x in guide_counts) / len(guide_counts) if guide_counts else 0
    counts = Counter(r.get("perturbation", "unknown") for r in cells)
    targeting = [v for k, v in counts.items() if k not in {"NTC", "non_targeting", "control"}]
    min_coverage = min(targeting) if targeting else 0; modality = args.modality.lower()
    has_rna = "rna" in modality or "transcript" in modality
    targeted = args.readout_class == "targeted" or (args.readout_class == "auto" and n_features < 500)
    low_moi = mean_guides <= 1.2 and collision <= 0.15
    replicate_values = {r.get("replicate") or r.get("batch") for r in cells if r.get("replicate") or r.get("batch")}
    n_controls = sum(r.get("control_type") == "non_targeting" for r in cells)
    covariates = [x for x in ("batch", "replicate", "donor", "condition", "cell_type") if x in fields]
    profile = [{"n_cells": len(cells), "n_features": n_features, "n_perturbations": len(counts),
        "n_guides": len({r.get("guide_id") for r in cells if r.get("guide_id")}),
        "min_cells_per_perturbation": min_coverage, "mean_guides_per_cell": round(mean_guides, 4),
        "guide_collision_rate": round(collision, 4), "moi_class": "low_moi" if low_moi else "high_or_mixed_moi",
        "readout_class": "targeted" if targeted else "whole_transcriptome", "modality": args.modality,
        "n_replicates": len(replicate_values), "n_non_targeting_controls": n_controls, "covariates": ";".join(covariates)}]
    write_csv(outdir / "dataset_profile.csv", profile, list(profile[0]))
    rules = {
      "native_paper": (bool(args.native_baseline), "No dataset-specific native baseline adapter was declared.", f"Declared adapter: {args.native_baseline}"),
      "transparent_pseudobulk": (has_rna and min_coverage >= 20 and n_controls >= 20, "Needs RNA, >=20 cells/target, and >=20 non-targeting controls.", "Transparent RNA baseline with control comparison."),
      "sceptre_low_moi": (has_rna and low_moi and min_coverage >= 20 and n_controls >= 20, "Restricted to low-MOI RNA with adequate targets and controls.", "Measured low-MOI path; never substitute the high-MOI model."),
      "sceptre_high_moi_or_mixed_moi": (has_rna and not low_moi and min_coverage >= 20 and n_controls >= 20, "Restricted to high/mixed-MOI RNA with adequate targets and controls.", "Measured high/mixed-MOI path with guide-collision modeling."),
      "mixscape": (has_rna and not targeted and min_coverage >= 20 and n_controls >= 20, "Requires whole-transcriptome RNA; targeted panels are incompatible.", "Whole-transcriptome perturbation classification."),
      "ps": (has_rna and n_features >= 50 and min_coverage >= 20 and n_controls >= 20, "Requires an RNA response signature of >=50 genes, targets, and controls.", "Perturbation-response scoring on an RNA signature."),
      "gsfa": (has_rna and not targeted and len(counts) >= 3 and min_coverage >= 20, "Requires whole-transcriptome RNA and multiple perturbations; targeted panels are incompatible.", "Latent perturbation-program inference."),
      "pertpy_distance": (has_rna and min_coverage >= 2 and n_controls >= 2, "Requires RNA groups with controls and at least two cells per target.", "Group-wise perturbation distance analysis.")}
    rows = []
    for method in METHODS:
        ok, bad, good = rules[method]
        rows.append({"method_id": method, "decision": "RUN" if ok else "INCOMPATIBLE", "reason": good if ok else bad})
    write_csv(outdir / "method_decisions.csv", rows, ["method_id", "decision", "reason"])

if __name__ == "__main__": main()
