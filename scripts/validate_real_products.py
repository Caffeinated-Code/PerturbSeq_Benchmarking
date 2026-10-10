#!/usr/bin/env python3
"""Validate generated real-data products against the shared schema and source semantics."""

from __future__ import annotations

import argparse
from pathlib import Path

import anndata as ad
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
REQUIRED_OBS = ["cell_id", "dataset_id", "perturbation", "guide_id", "target_gene", "control_type", "batch"]
REQUIRED_VAR = ["gene_id", "gene_symbol"]
EXPECTED = {
    "gse178317_drager_downsampled.h5ad": (8000, 33538, "cell"),
    "gse207628_hyprseq.h5ad": (10463, 49, "cell"),
    "replogle_k562_essential_raw_pseudobulk_schema.h5ad": (2285, 8563, "guide_pair_pseudobulk"),
}


def validate_product(path: Path, expected: tuple[int, int, str]) -> list[str]:
    errors = []
    obj = ad.read_h5ad(path, backed="r")
    n_obs, n_vars, observation_type = expected
    if obj.shape != (n_obs, n_vars):
        errors.append(f"{path.name}: expected {(n_obs, n_vars)}, found {obj.shape}")
    missing_obs = sorted(set(REQUIRED_OBS) - set(obj.obs.columns))
    missing_var = sorted(set(REQUIRED_VAR) - set(obj.var.columns))
    if missing_obs:
        errors.append(f"{path.name}: missing obs {missing_obs}")
    if missing_var:
        errors.append(f"{path.name}: missing var {missing_var}")
    if "counts" not in obj.layers:
        errors.append(f"{path.name}: missing counts layer")
    if set(obj.obs["observation_type"].astype(str)) != {observation_type}:
        errors.append(f"{path.name}: unexpected observation_type")
    if path.name.startswith(("gse178317", "gse207628")):
        for column in ["guide_id", "perturbation", "target_gene", "control_type"]:
            if set(obj.obs[column].astype(str)) != {"unknown"}:
                errors.append(f"{path.name}: {column} must remain unknown without a public assignment mapping")
    if path.name.startswith("replogle"):
        if int((obj.obs["control_type"].astype(str) == "non_targeting").sum()) != 109:
            errors.append(f"{path.name}: expected 109 source-labeled non-targeting rows")
        if int(obj.obs["benchmark_control"].astype(bool).sum()) != 97:
            errors.append(f"{path.name}: expected 97 author core controls")
        note = str(obj.uns.get("benchmark_notes", ""))
        if "not asserted to be integer UMI counts" not in note:
            errors.append(f"{path.name}: missing pseudobulk counts-layer caveat")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--product-dir", type=Path, default=ROOT / "data/processed/real_data")
    parser.add_argument("--artifact-dir", type=Path, default=ROOT / "artifacts/real_data")
    args = parser.parse_args()
    errors = []
    for filename, expected in EXPECTED.items():
        path = args.product_dir / filename
        if not path.exists():
            errors.append(f"missing product: {path}")
        else:
            errors.extend(validate_product(path, expected))
    status_path = args.artifact_dir / "real_dataset_status.csv"
    if not status_path.exists():
        errors.append(f"missing artifact: {status_path}")
    else:
        status = pd.read_csv(status_path)
        if len(status) != 3 or status.dataset_id.nunique() != 3:
            errors.append("real_dataset_status.csv must contain exactly three unique datasets")
        if status.status.astype(str).str.contains("complete|fully_analyzed", case=False).any():
            errors.append("status table contains an inflated completion claim")
    if errors:
        raise SystemExit("\n".join(errors))
    print("Real-data products passed schema, dimension, and missing-guide validation.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
