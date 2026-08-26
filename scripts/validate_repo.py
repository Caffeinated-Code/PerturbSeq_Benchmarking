#!/usr/bin/env python3
"""Validate repository structure and visible text hygiene."""

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "README.md",
    "PROJECT_SUMMARY.md",
    "configs/datasets.yml",
    "configs/methods.yml",
    "configs/benchmark.yml",
    "schemas/perturbseq_anndata_schema.yml",
    "main.nf",
    "nextflow.config",
    "docs/01_perturbseq_primer.md",
    "docs/02_alzheimers_microglia_primer.md",
    "docs/03_dataset_catalog.md",
    "docs/04_methods.md",
    "docs/05_benchmark_design.md",
    "docs/06_interpretation_guide.md",
    "docs/07_aws_scaling.md",
    "docs/08_dataset_procurement.md",
    "docs/09_outputs.md",
    "docs/10_roadmap.md",
    "docs/11_paper_native_baselines.md",
]

BLOCKED_PHRASES = [
    "prompt leakage",
    "ai trace",
    "no ai",
    "chatgpt",
    "codex",
    "resume",
    "interview",
    "arc institute team",
    "guardrails",
    "not only, but also",
]


def read_text(path):
    return path.read_text(encoding="utf-8", errors="ignore")


def main():
    errors = []
    for rel in REQUIRED_FILES:
        if not (ROOT / rel).exists():
            errors.append(f"Missing required file: {rel}")

    text_files = [
        path for path in ROOT.rglob("*")
        if path.is_file()
        and ".git" not in path.parts
        and path.name != "validate_repo.py"
        and path.suffix.lower() in {".md", ".yml", ".yaml", ".py", ".nf", ".txt", ".cff"}
    ]
    for path in text_files:
        rel = path.relative_to(ROOT)
        text = read_text(path).lower()
        for phrase in BLOCKED_PHRASES:
            if phrase in text:
                errors.append(f"Blocked phrase '{phrase}' found in {rel}")

    readme = read_text(ROOT / "README.md")
    for doc in [
        "docs/01_perturbseq_primer.md",
        "docs/02_alzheimers_microglia_primer.md",
        "docs/03_dataset_catalog.md",
        "docs/04_methods.md",
        "docs/05_benchmark_design.md",
        "docs/06_interpretation_guide.md",
        "docs/07_aws_scaling.md",
        "docs/08_dataset_procurement.md",
        "docs/09_outputs.md",
        "docs/10_roadmap.md",
        "docs/11_paper_native_baselines.md",
    ]:
        if doc not in readme:
            errors.append(f"README does not link {doc}")

    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    print("Repository validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
