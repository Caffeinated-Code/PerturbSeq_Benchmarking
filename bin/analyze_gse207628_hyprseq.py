#!/usr/bin/env python3
"""Summarize public GSE207628 targeted HYPR-seq matrices."""

from __future__ import annotations

import argparse
import csv
import gzip
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def median(values: list[float]) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    mid = len(ordered) // 2
    if len(ordered) % 2:
        return ordered[mid]
    return (ordered[mid - 1] + ordered[mid]) / 2


def matrix_summary(path: Path) -> dict[str, object]:
    with gzip.open(path, "rt") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        count_cols = [col for col in (reader.fieldnames or []) if col != "cell"]
        totals = []
        detected = []
        cell_barcodes = []
        for row in reader:
            total = 0.0
            present = 0
            for col in count_cols:
                value = float(row.get(col) or 0)
                total += value
                if value > 0:
                    present += 1
            totals.append(total)
            detected.append(present)
            cell_barcodes.append(str(row.get("cell", "")))
    target_genes = [col.replace("exon", "") for col in count_cols if col.endswith("exon")]
    duplicate_count = len(cell_barcodes) - len(set(cell_barcodes))
    return {
        "sample_id": path.name.split("_collapsed")[0],
        "matrix_file": path.name,
        "n_cells": len(cell_barcodes),
        "n_features": len(count_cols),
        "n_exon_targets": len(target_genes),
        "n_barcode_features": len([col for col in count_cols if "bar" in col.lower()]),
        "median_counts_per_cell": round(median(totals), 4),
        "mean_counts_per_cell": round(sum(totals) / len(totals), 4) if totals else 0,
        "median_detected_features": round(median([float(x) for x in detected]), 4),
        "low_depth_cell_fraction_lt_50_counts": round(sum(1 for x in totals if x < 50) / len(totals), 4) if totals else 0,
        "duplicate_cell_barcodes": duplicate_count,
        "target_genes": ";".join(sorted(target_genes)),
    }


def probe_summary(path: Path) -> tuple[dict[str, object], list[dict[str, object]]]:
    with gzip.open(path, "rt", encoding="utf-8-sig", errors="replace") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        rows = list(reader)
    probe_rows = []
    five_prime_col = next((col for col in (reader.fieldnames or []) if "5" in col and "Probe" in col), "")
    for row in rows:
        name = str(row.get("Name", ""))
        probe_rows.append(
            {
                "probe_name": name,
                "probe_class": "cell_or_sample_barcode" if "bar" in name.lower() else "target_probe",
                "has_umi_stretch": "NNNNNNNNNN" in str(row.get(five_prime_col, "")),
            }
        )
    return (
        {
            "n_probe_rows": len(rows),
            "n_barcode_probe_rows": sum(1 for row in probe_rows if row["probe_class"] == "cell_or_sample_barcode"),
            "n_target_probe_rows": sum(1 for row in probe_rows if row["probe_class"] == "target_probe"),
        },
        probe_rows,
    )


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        return
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--matrix-dir", default="data/raw/GSE207628/extracted")
    parser.add_argument("--probe-file", default="data/raw/GSE207628/GSE207628_probes_hyprseq.tsv.gz")
    parser.add_argument("--outdir", default="results/real_public")
    args = parser.parse_args()

    matrix_dir = ROOT / args.matrix_dir
    probe_file = ROOT / args.probe_file
    outdir = ROOT / args.outdir

    matrix_rows = [matrix_summary(path) for path in sorted(matrix_dir.glob("*.count_matrix.txt.gz"))]
    probe_stats, probe_rows = probe_summary(probe_file)
    for row in matrix_rows:
        row.update(probe_stats)
        row["dataset_id"] = "yang_ad_microglia_hyprseq"
        row["accession"] = "GSE207628"
        row["analysis_level"] = "public_targeted_matrix_audit"

    write_csv(outdir / "gse207628_hyprseq_matrix_summary.csv", matrix_rows)
    write_csv(outdir / "gse207628_hyprseq_probe_panel.csv", probe_rows)
    print(f"Wrote GSE207628 summaries to {outdir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
