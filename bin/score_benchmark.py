#!/usr/bin/env python3
"""Summarize benchmark outputs."""

import argparse
import csv
from pathlib import Path


AD_GENES = {"TREM2", "APOE", "INPP5D", "BIN1", "PICALM", "CD33", "ABCA7", "CR1", "SORL1"}
MICROGLIA_STATE_GENES = {"SPP1", "CST7", "LPL", "P2RY12", "CX3CR1", "TMEM119", "CSF1R", "ISG15", "IFIT1"}


def read_csv(path):
    with open(path, newline="") as handle:
        return list(csv.DictReader(handle))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--effects", required=True)
    parser.add_argument("--outdir", required=True)
    args = parser.parse_args()

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    effects = read_csv(args.effects)
    hits = [row for row in effects if row["effect_direction"] != "neutral"]
    ad_hits = [row for row in hits if row["gene"] in AD_GENES]
    microglia_hits = [row for row in hits if row["gene"] in MICROGLIA_STATE_GENES]

    rows = [{
        "method": effects[0]["method"] if effects else "unknown",
        "n_effects": len(effects),
        "n_non_neutral_effects": len(hits),
        "n_ad_gene_effects": len(ad_hits),
        "n_microglia_state_gene_effects": len(microglia_hits),
    }]
    with open(outdir / "benchmark_summary.csv", "w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    main()

