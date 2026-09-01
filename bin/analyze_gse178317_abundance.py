#!/usr/bin/env python3
"""Summarize public GSE178317 iTF microglia RNA abundance context."""

from __future__ import annotations

import argparse
import csv
import gzip
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MICROGLIA_MARKERS = {"FGR", "AIF1", "TYROBP", "C1QA", "C1QB", "C1QC", "CX3CR1", "P2RY12", "TREM2", "APOE", "SPP1", "ITGAM"}


def sample_group(sample: str) -> str:
    if "Day0" in sample:
        return "iPSC_day0"
    if "LPS" in sample:
        return "iTF_microglia_day9_lps"
    if "PBS" in sample:
        return "iTF_microglia_day9_pbs"
    if "Day15" in sample:
        return "iTF_microglia_day15"
    return "other"


def replicate_number(sample: str) -> str:
    match = re.search(r"_(\d+)$", sample)
    return match.group(1) if match else ""


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
    parser.add_argument("--abundance-file", default="data/raw/GSE178317/GSE178317_iTF_Microglia_RNAseq_abundance.csv.gz")
    parser.add_argument("--outdir", default="results/real_public")
    args = parser.parse_args()

    path = ROOT / args.abundance_file
    with gzip.open(path, "rt", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)
        fieldnames = reader.fieldnames or []
    id_cols = ["ensembl_id", "gene"]
    sample_cols = [col for col in fieldnames if col not in id_cols]
    sample_values = {sample: [] for sample in sample_cols}
    gene_to_values = {}
    for row in rows:
        gene = str(row.get("gene", "")).upper()
        values = {}
        for sample in sample_cols:
            value = float(row.get(sample) or 0)
            values[sample] = value
            sample_values[sample].append(value)
        gene_to_values[gene] = values

    metadata_rows = [
        {
            "sample_id": sample,
            "sample_group": sample_group(sample),
            "replicate": replicate_number(sample),
            "n_detected_genes": sum(1 for value in sample_values[sample] if value > 0),
            "total_abundance": round(sum(sample_values[sample]), 4),
        }
        for sample in sample_cols
    ]

    marker_rows = []
    for marker in sorted(MICROGLIA_MARKERS):
        if marker not in gene_to_values:
            marker_rows.append({"gene": marker, "status": "missing_from_table", "max_group": "", "max_mean_abundance": ""})
            continue
        row_values = gene_to_values[marker]
        group_means = {}
        for group in sorted({sample_group(sample) for sample in sample_cols}):
            group_samples = [sample for sample in sample_cols if sample_group(sample) == group]
            group_means[group] = sum(row_values[sample] for sample in group_samples) / len(group_samples)
        max_group = max(group_means, key=group_means.get)
        marker_rows.append(
            {
                "gene": marker,
                "status": "present",
                "max_group": max_group,
                "max_mean_abundance": round(group_means[max_group], 4),
            }
        )

    summary_rows = [
        {
            "dataset_id": "drager_microglia_cropseq",
            "accession": "GSE178317",
            "analysis_level": "public_abundance_context",
            "n_genes": len(rows),
            "n_samples": len(sample_cols),
            "n_sample_groups": len({sample_group(sample) for sample in sample_cols}),
            "n_microglia_markers_present": sum(1 for row in marker_rows if row["status"] == "present"),
            "raw_cropseq_archive_status": "public_large_archive_not_bundled",
        }
    ]

    outdir = ROOT / args.outdir
    write_csv(outdir / "gse178317_abundance_summary.csv", summary_rows)
    write_csv(outdir / "gse178317_sample_qc.csv", metadata_rows)
    write_csv(outdir / "gse178317_microglia_marker_context.csv", marker_rows)
    print(f"Wrote GSE178317 summaries to {outdir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
