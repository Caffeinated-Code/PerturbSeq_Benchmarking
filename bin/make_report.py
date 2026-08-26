#!/usr/bin/env python3
"""Create a compact Markdown report."""

import argparse
import csv
from pathlib import Path


def read_first(path):
    with open(path, newline="") as handle:
        rows = list(csv.DictReader(handle))
    return rows[0] if rows else {}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset-qc", required=True)
    parser.add_argument("--benchmark-summary", required=True)
    parser.add_argument("--regulatory-summary", default=None)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    qc = read_first(args.dataset_qc)
    summary = read_first(args.benchmark_summary)
    regulatory = read_first(args.regulatory_summary) if args.regulatory_summary else {}
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Perturb-seq Benchmark Demo Report",
        "",
        "## Dataset QC",
        "",
        f"- cells: {qc.get('n_cells', 'NA')}",
        f"- genes: {qc.get('n_genes', 'NA')}",
        f"- perturbations: {qc.get('n_perturbations', 'NA')}",
        f"- design status: {qc.get('design_status', 'NA')}",
        "",
        "## Benchmark Summary",
        "",
        f"- method: {summary.get('method', 'NA')}",
        f"- tested effects: {summary.get('n_effects', 'NA')}",
        f"- non-neutral effects: {summary.get('n_non_neutral_effects', 'NA')}",
        f"- Alzheimer gene effects: {summary.get('n_ad_gene_effects', 'NA')}",
        f"- microglia-state gene effects: {summary.get('n_microglia_state_gene_effects', 'NA')}",
        "",
        "## Regulatory Validation",
        "",
        f"- tested effects: {regulatory.get('n_tested_effects', 'NA')}",
        f"- PASS: {regulatory.get('n_pass', 'NA')}",
        f"- WARN: {regulatory.get('n_warn', 'NA')}",
        f"- LOW_SUPPORT: {regulatory.get('n_low_support', 'NA')}",
        "",
        "This demo validates the benchmark scaffold. Full runs should use public datasets listed in the dataset manifest.",
    ]
    out.write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
