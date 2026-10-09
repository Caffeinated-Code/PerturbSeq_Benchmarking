#!/usr/bin/env python3
"""Create a compact Markdown report."""

import argparse
import csv
from pathlib import Path


def read_first(path):
    with open(path, newline="") as handle:
        rows = list(csv.DictReader(handle))
    return rows[0] if rows else {}


def read_rows(path):
    with open(path, newline="") as handle:
        return list(csv.DictReader(handle))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset-qc", required=True)
    parser.add_argument("--benchmark-summary", required=True)
    parser.add_argument("--method-decisions", default=None)
    parser.add_argument("--regulatory-summary", default=None)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    qc = read_first(args.dataset_qc)
    benchmark_rows = read_rows(args.benchmark_summary)
    summary = {row.get("metric"): row.get("value") for row in benchmark_rows}
    method_id = benchmark_rows[0].get("method_id", "NA") if benchmark_rows else "NA"
    method_status = benchmark_rows[0].get("method_status", "NA") if benchmark_rows else "NA"
    method_decisions = read_rows(args.method_decisions) if args.method_decisions else []
    regulatory = read_first(args.regulatory_summary) if args.regulatory_summary else {}
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Perturb-seq Benchmark Demo Report",
        "",
        "> **Synthetic infrastructure test.** These values are not biological findings and do not establish that benchmark methods ran on public datasets.",
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
        f"- method: {method_id}",
        f"- execution status: {method_status}",
        f"- FDR discoveries: {summary.get('fdr_discoveries', 'NA')}",
        f"- target engagement rate: {summary.get('target_engagement_rate', 'NA')}",
        f"- runtime seconds: {summary.get('runtime_seconds', 'NA')}",
        f"- peak memory MB: {summary.get('peak_memory_mb', 'NA')}",
        "",
        "## Method Applicability",
        "",
    ]
    if method_decisions:
        lines.extend(["| Method | Decision | Reason |", "|---|---|---|"])
        for row in method_decisions:
            lines.append(f"| {row.get('method_id', '')} | {row.get('decision', '')} | {row.get('reason', '')} |")
        lines.append("")
    else:
        lines.extend(["No method-decision table was supplied.", ""])
    lines.extend([
        "## Legacy Regulatory Support Fixture",
        "",
        f"- tested effects: {regulatory.get('n_tested_effects', 'NA')}",
        f"- PASS: {regulatory.get('n_pass', 'NA')}",
        f"- WARN: {regulatory.get('n_warn', 'NA')}",
        f"- LOW_SUPPORT: {regulatory.get('n_low_support', 'NA')}",
        "",
        "These synthetic outputs test plumbing only. Observational chromatin overlap is not causal validation. Full runs must satisfy the result and evidence contracts before public display.",
    ])
    out.write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
