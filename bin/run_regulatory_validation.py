#!/usr/bin/env python3
"""Score chromatin support for perturbation effects."""

import argparse
import csv
from collections import Counter, defaultdict
from pathlib import Path


MICROGLIA_MOTIFS = {"SPI1", "IRF8", "MAFB", "RUNX1", "CEBPB", "MEF2C"}
AD_TERMS = {"AD_risk_locus", "disease_state_marker", "microglia_survival_gene"}


def read_csv(path):
    with open(path, newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path, rows, fields):
    with open(path, "w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def status_from_score(score):
    if score >= 70:
        return "PASS"
    if score >= 40:
        return "WARN"
    return "LOW_SUPPORT"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--effects", required=True)
    parser.add_argument("--peaks", required=True)
    parser.add_argument("--peak-to-gene", required=True)
    parser.add_argument("--motifs", required=True)
    parser.add_argument("--outdir", required=True)
    args = parser.parse_args()

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    effects = [row for row in read_csv(args.effects) if row.get("effect_direction") != "neutral"]
    peaks = read_csv(args.peaks)
    peak_to_gene = read_csv(args.peak_to_gene)
    motifs = read_csv(args.motifs)

    peaks_by_gene = defaultdict(list)
    for peak in peaks:
        peaks_by_gene[peak["linked_gene"]].append(peak)

    links_by_gene = defaultdict(list)
    for link in peak_to_gene:
        links_by_gene[link["gene_symbol"]].append(link)

    motifs_by_peak = defaultdict(list)
    for motif in motifs:
        motifs_by_peak[motif["peak_id"]].append(motif)

    rows = []
    for effect in effects:
        gene = effect["gene"]
        linked_peaks = peaks_by_gene.get(gene, [])
        linked_links = links_by_gene.get(gene, [])
        best_peak = max(linked_peaks, key=lambda p: float(p["accessibility_score"]), default=None)
        best_link = max(linked_links, key=lambda p: float(p["link_score"]), default=None)
        peak_motifs = motifs_by_peak.get(best_peak["peak_id"], []) if best_peak else []
        best_microglia_motif = max(
            [m for m in peak_motifs if m["motif"] in MICROGLIA_MOTIFS],
            key=lambda m: float(m["motif_score"]),
            default=None,
        )

        score = 0
        evidence = []
        if best_peak and best_peak["cell_type"] == "microglia" and float(best_peak["accessibility_score"]) >= 0.05:
            score += 30
            evidence.append("accessible_microglia_peak")
        if best_link and float(best_link["link_score"]) >= 0.20:
            score += 25
            evidence.append("peak_to_gene_link")
        if best_peak and best_peak["ad_annotation"] in AD_TERMS:
            score += 20
            evidence.append("ad_or_microglia_annotation")
        if best_microglia_motif and float(best_microglia_motif["motif_score"]) >= 0.50:
            score += 15
            evidence.append("microglia_tf_motif")
        if best_peak and best_peak["cell_state_annotation"] not in {"", "none"}:
            score += 10
            evidence.append("cell_state_annotation")

        rows.append({
            "method": effect["method"],
            "perturbation": effect["perturbation"],
            "gene": gene,
            "effect_direction": effect["effect_direction"],
            "log2fc": effect["log2fc"],
            "best_peak_id": best_peak["peak_id"] if best_peak else "",
            "best_peak_accessibility": best_peak["accessibility_score"] if best_peak else "",
            "best_peak_to_gene_score": best_link["link_score"] if best_link else "",
            "best_microglia_motif": best_microglia_motif["motif"] if best_microglia_motif else "",
            "ad_annotation": best_peak["ad_annotation"] if best_peak else "",
            "cell_state_annotation": best_peak["cell_state_annotation"] if best_peak else "",
            "regulatory_validation_score": score,
            "regulatory_validation_status": status_from_score(score),
            "evidence": ";".join(evidence) if evidence else "none",
        })

    fields = [
        "method", "perturbation", "gene", "effect_direction", "log2fc",
        "best_peak_id", "best_peak_accessibility", "best_peak_to_gene_score",
        "best_microglia_motif", "ad_annotation", "cell_state_annotation",
        "regulatory_validation_score", "regulatory_validation_status", "evidence"
    ]
    write_csv(outdir / "regulatory_validation.csv", rows, fields)

    counts = Counter(row["regulatory_validation_status"] for row in rows)
    summary = [{
        "n_tested_effects": len(rows),
        "n_pass": counts.get("PASS", 0),
        "n_warn": counts.get("WARN", 0),
        "n_low_support": counts.get("LOW_SUPPORT", 0),
    }]
    write_csv(outdir / "regulatory_validation_summary.csv", summary, ["n_tested_effects", "n_pass", "n_warn", "n_low_support"])

    strong = [row for row in rows if row["regulatory_validation_status"] == "PASS"]
    write_csv(outdir / "validated_ad_microglia_hits.csv", strong, fields)


if __name__ == "__main__":
    main()

