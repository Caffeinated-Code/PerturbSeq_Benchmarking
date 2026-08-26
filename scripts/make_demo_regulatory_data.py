#!/usr/bin/env python3
"""Create small regulatory validation tables for the demo benchmark."""

import argparse
import csv
from pathlib import Path


PEAKS = [
    {
        "peak_id": "chr6_41160000_41160800",
        "chromosome": "chr6",
        "start": 41160000,
        "end": 41160800,
        "linked_gene": "TREM2",
        "cell_type": "microglia",
        "accessibility_score": 0.82,
        "ad_annotation": "AD_risk_locus",
        "cell_state_annotation": "lipid_phagocytic",
    },
    {
        "peak_id": "chr19_44905000_44906000",
        "chromosome": "chr19",
        "start": 44905000,
        "end": 44906000,
        "linked_gene": "APOE",
        "cell_type": "microglia",
        "accessibility_score": 0.78,
        "ad_annotation": "AD_risk_locus",
        "cell_state_annotation": "lipid_handling",
    },
    {
        "peak_id": "chr2_233930000_233931000",
        "chromosome": "chr2",
        "start": 233930000,
        "end": 233931000,
        "linked_gene": "INPP5D",
        "cell_type": "microglia",
        "accessibility_score": 0.74,
        "ad_annotation": "AD_risk_locus",
        "cell_state_annotation": "immune_regulatory",
    },
    {
        "peak_id": "chr5_149430000_149431000",
        "chromosome": "chr5",
        "start": 149430000,
        "end": 149431000,
        "linked_gene": "CSF1R",
        "cell_type": "microglia",
        "accessibility_score": 0.69,
        "ad_annotation": "microglia_survival_gene",
        "cell_state_annotation": "survival_state_control",
    },
    {
        "peak_id": "chr4_88900000_88901000",
        "chromosome": "chr4",
        "start": 88900000,
        "end": 88901000,
        "linked_gene": "SPP1",
        "cell_type": "microglia",
        "accessibility_score": 0.71,
        "ad_annotation": "disease_state_marker",
        "cell_state_annotation": "SPP1_like",
    },
    {
        "peak_id": "chr8_143800000_143801000",
        "chromosome": "chr8",
        "start": 143800000,
        "end": 143801000,
        "linked_gene": "GAPDH",
        "cell_type": "mixed",
        "accessibility_score": 0.35,
        "ad_annotation": "none",
        "cell_state_annotation": "none",
    },
]

MOTIFS = [
    ("chr6_41160000_41160800", "SPI1", 0.91),
    ("chr6_41160000_41160800", "IRF8", 0.72),
    ("chr19_44905000_44906000", "MAFB", 0.67),
    ("chr2_233930000_233931000", "RUNX1", 0.64),
    ("chr5_149430000_149431000", "SPI1", 0.70),
    ("chr4_88900000_88901000", "CEBPB", 0.66),
    ("chr8_143800000_143801000", "MYC", 0.41),
]


def write_csv(path, rows, fieldnames):
    with open(path, "w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--outdir", default="demo_data")
    args = parser.parse_args()

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    peak_fields = [
        "peak_id", "chromosome", "start", "end", "linked_gene", "cell_type",
        "accessibility_score", "ad_annotation", "cell_state_annotation"
    ]
    write_csv(outdir / "demo_regulatory_peaks.csv", PEAKS, peak_fields)

    peak_to_gene = [
        {
            "peak_id": peak["peak_id"],
            "gene_symbol": peak["linked_gene"],
            "link_score": round(float(peak["accessibility_score"]) * 0.9, 4),
            "evidence_type": "demo_peak_to_gene",
        }
        for peak in PEAKS
    ]
    write_csv(outdir / "demo_peak_to_gene.csv", peak_to_gene, ["peak_id", "gene_symbol", "link_score", "evidence_type"])

    motif_rows = [{"peak_id": p, "motif": m, "motif_score": s} for p, m, s in MOTIFS]
    write_csv(outdir / "demo_motifs.csv", motif_rows, ["peak_id", "motif", "motif_score"])


if __name__ == "__main__":
    main()

