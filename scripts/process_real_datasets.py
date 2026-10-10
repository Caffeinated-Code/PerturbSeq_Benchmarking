#!/usr/bin/env python3
"""Convert three public perturbation datasets and emit honest QC/baselines.

Large source files and h5ad products remain ignored. Small CSV/JSON summaries are
the auditable, version-controlled outputs. No guide identity is inferred when the
archive does not contain the source study's assignment table.
"""

from __future__ import annotations

import argparse
import csv
import gzip
import hashlib
import json
import re
from pathlib import Path

import anndata as ad
import h5py
import numpy as np
import pandas as pd
from scipy import sparse, stats


ROOT = Path(__file__).resolve().parents[1]
MITO_PREFIX = "MT-"
STATE_SETS = {
    "homeostatic": ["P2RY12", "CX3CR1", "TMEM119", "GPR34", "SALL1"],
    "chemokine": ["CCL2", "CCL3", "CCL4", "CXCL1", "CXCL2", "CXCL8"],
    "interferon": ["ISG15", "IFIT1", "IFIT2", "IFIT3", "MX1"],
    "spp1_disease": ["SPP1", "APOE", "LPL", "GPNMB", "TREM2"],
    "proliferation": ["MKI67", "TOP2A", "PCNA", "TYMS"],
}


def write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"refusing to write empty table: {path}")
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def sha256(path: Path, chunk: int = 1024 * 1024) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(chunk), b""):
            digest.update(block)
    return digest.hexdigest()


def display_path(path: Path) -> str:
    resolved = path.resolve()
    return str(resolved.relative_to(ROOT)) if resolved.is_relative_to(ROOT) else resolved.name


def read_10x_h5(path: Path) -> tuple[sparse.csr_matrix, np.ndarray, np.ndarray, np.ndarray]:
    with h5py.File(path, "r") as handle:
        group = handle["matrix"]
        shape = tuple(int(x) for x in group["shape"][:])
        matrix = sparse.csc_matrix(
            (group["data"][:], group["indices"][:], group["indptr"][:]), shape=shape
        ).T.tocsr()
        barcodes = group["barcodes"][:].astype(str)
        gene_ids = group["features"]["id"][:].astype(str)
        gene_names = group["features"]["name"][:].astype(str)
    return matrix, barcodes, gene_ids, gene_names


def deterministic_rows(n: int, limit: int) -> np.ndarray:
    if limit <= 0 or n <= limit:
        return np.arange(n)
    return np.linspace(0, n - 1, num=limit, dtype=int)


def process_drager(indir: Path, outdir: Path, product_dir: Path, cells_per_lane: int) -> dict:
    rna_files = sorted(indir.glob("GSM*_10X_Lane*_filtered_feature_bc_matrix.h5"))
    guide_files = sorted(indir.glob("GSM*_sgRNAenrichment_Lane*_filtered_feature_bc_matrix.h5"))
    if len(rna_files) != 4 or len(guide_files) != 4:
        raise FileNotFoundError("GSE178317 requires four filtered RNA and four sgRNA-enrichment H5 files")
    objects, lane_qc, state_rows = [], [], []
    for lane_no, path in enumerate(rna_files, start=1):
        matrix, barcodes, gene_ids, gene_names = read_10x_h5(path)
        total = np.asarray(matrix.sum(axis=1)).ravel()
        detected = np.diff(matrix.indptr)
        mito = np.flatnonzero(np.char.startswith(gene_names.astype(str), MITO_PREFIX))
        mito_counts = np.asarray(matrix[:, mito].sum(axis=1)).ravel() if len(mito) else np.zeros(matrix.shape[0])
        pct_mito = np.divide(mito_counts * 100, total, out=np.zeros_like(total, dtype=float), where=total > 0)
        keep = deterministic_rows(matrix.shape[0], cells_per_lane)
        obs = pd.DataFrame(index=[f"lane{lane_no}:{x}" for x in barcodes[keep]])
        obs["cell_id"] = obs.index
        obs["dataset_id"] = "gse178317_drager_cropseq"
        obs["perturbation"] = "unknown"
        obs["guide_id"] = "unknown"
        obs["target_gene"] = "unknown"
        obs["control_type"] = "unknown"
        obs["batch"] = f"10x_lane_{lane_no}"
        obs["donor"] = "WTC11"
        obs["condition"] = "day8_iTF_microglia"
        obs["cell_type"] = "iTF_microglia_unfiltered_state"
        obs["observation_type"] = "cell"
        obs["guide_count"] = np.nan
        obs["n_genes"] = detected[keep]
        obs["total_counts"] = total[keep]
        obs["pct_mito"] = pct_mito[keep]
        var = pd.DataFrame(index=gene_ids)
        var["gene_id"] = gene_ids
        var["gene_symbol"] = gene_names
        var["feature_type"] = "Gene Expression"
        obj = ad.AnnData(X=matrix[keep], obs=obs, var=var)
        obj.layers["counts"] = obj.X.copy()
        obj.uns["dataset_source"] = "GEO GSE178317 filtered Cell Ranger matrices"
        obj.uns["publication"] = "doi:10.1038/s41593-022-01131-4"
        obj.uns["benchmark_notes"] = (
            "Deterministic lane-balanced subset. Guide assignments are unknown because the GEO matrices "
            "do not contain the demuxEM/z-score consensus assignment table."
        )
        objects.append(obj)
        lane_qc.append({
            "dataset_id": "gse178317_drager_cropseq", "lane": lane_no, "n_cells": matrix.shape[0],
            "n_genes": matrix.shape[1], "median_counts": float(np.median(total)),
            "median_genes": float(np.median(detected)), "median_pct_mito": round(float(np.median(pct_mito)), 4),
            "cells_pct_mito_gt20": int((pct_mito > 20).sum()), "subset_cells_written": len(keep),
            "guide_assignment_status": "unknown_not_deposited",
        })
        libnorm = sparse.diags(np.divide(1e4, total, out=np.zeros_like(total, dtype=float), where=total > 0)) @ matrix
        lognorm = libnorm.copy(); lognorm.data = np.log1p(lognorm.data)
        index = {g: i for i, g in enumerate(gene_names)}
        for state, genes in STATE_SETS.items():
            cols = [index[g] for g in genes if g in index]
            scores = np.asarray(lognorm[:, cols].mean(axis=1)).ravel() if cols else np.zeros(matrix.shape[0])
            state_rows.append({"dataset_id": "gse178317_drager_cropseq", "lane": lane_no, "state": state,
                               "genes_found": len(cols), "median_score": round(float(np.median(scores)), 6),
                               "mean_score": round(float(np.mean(scores)), 6)})
    combined = ad.concat(objects, join="inner", merge="same", index_unique=None)
    product_dir.mkdir(parents=True, exist_ok=True)
    combined.write_h5ad(product_dir / "gse178317_drager_downsampled.h5ad", compression="gzip")

    guide_audit = []
    for lane_no, path in enumerate(guide_files, start=1):
        matrix, _, _, names = read_10x_h5(path)
        feature_types = set(names[np.asarray(matrix.sum(axis=0)).ravel() > 0])
        guide_named = [x for x in feature_types if re.search(r"sgRNA|guide|gRNA", x, re.I)]
        guide_audit.append({"dataset_id": "gse178317_drager_cropseq", "lane": lane_no,
                            "matrix_cells": matrix.shape[0], "matrix_features": matrix.shape[1],
                            "nonzero_features": len(feature_types), "explicit_guide_features": len(guide_named),
                            "assignment_usable": False})
    write_csv(outdir / "gse178317_lane_qc.csv", lane_qc)
    write_csv(outdir / "gse178317_state_baseline.csv", state_rows)
    write_csv(outdir / "gse178317_guide_archive_audit.csv", guide_audit)
    return {"dataset_id": "gse178317_drager_cropseq", "status": "processed_expression_guide_assignment_unavailable",
            "observations": int(sum(x["n_cells"] for x in lane_qc)), "features": int(objects[0].n_vars),
            "product_observations": int(combined.n_obs), "product_features": int(combined.n_vars)}


def process_hyprseq(indir: Path, outdir: Path, product_dir: Path) -> dict:
    files = sorted(indir.glob("*.count_matrix.txt.gz"))
    if len(files) != 2:
        raise FileNotFoundError("GSE207628 requires two count matrices")
    objects, qc_rows, replicate_means = [], [], []
    for rep, path in enumerate(files, start=1):
        frame = pd.read_csv(path, sep="\t", index_col="cell")
        frame = frame.apply(pd.to_numeric, errors="raise")
        feature_names = frame.columns.astype(str)
        is_barcode = feature_names.str.contains("bar", case=False)
        expression_names = feature_names[~is_barcode]
        counts = sparse.csr_matrix(frame.to_numpy(dtype=np.float32))
        total = np.asarray(counts.sum(axis=1)).ravel()
        detected = np.diff(counts.indptr)
        expression_total = frame.loc[:, expression_names].sum(axis=1).to_numpy()
        obs = pd.DataFrame(index=[f"rep{rep}:{x}" for x in frame.index.astype(str)])
        obs["cell_id"] = obs.index; obs["dataset_id"] = "gse207628_yang_hyprseq"
        obs["perturbation"] = "unknown"; obs["guide_id"] = "unknown"; obs["target_gene"] = "unknown"
        obs["control_type"] = "unknown"; obs["batch"] = f"biological_rep_{rep}"; obs["donor"] = "WTC11"
        obs["condition"] = "iPSC_microglia_CRISPRi"; obs["cell_type"] = "iPSC_derived_microglia"
        obs["observation_type"] = "cell"
        obs["guide_count"] = np.nan; obs["n_genes"] = detected; obs["total_counts"] = total
        obs["targeted_expression_counts"] = expression_total
        var = pd.DataFrame(index=feature_names)
        var["gene_id"] = feature_names; var["gene_symbol"] = feature_names.str.replace("exon$", "", regex=True)
        var["feature_type"] = np.where(is_barcode, "assay_barcode_probe", "targeted_RNA_probe")
        obj = ad.AnnData(X=counts, obs=obs, var=var); obj.layers["counts"] = obj.X.copy()
        obj.uns["dataset_source"] = "GEO GSE207628 cell-by-probe count table"
        obj.uns["publication"] = "doi:10.1038/s41588-023-01506-8"
        obj.uns["benchmark_notes"] = "Targeted HyPR-seq; no whole-transcriptome QC or guide labels are asserted."
        objects.append(obj)
        qc_rows.append({"dataset_id": "gse207628_yang_hyprseq", "replicate": rep, "n_cells": len(frame),
                        "n_features": frame.shape[1], "n_targeted_rna_features": len(expression_names),
                        "n_barcode_probe_features": int(is_barcode.sum()), "median_total_counts": float(np.median(total)),
                        "median_targeted_expression_counts": float(np.median(expression_total)),
                        "zero_targeted_expression_cells": int((expression_total == 0).sum()),
                        "guide_assignment_status": "unknown_mapping_not_deposited"})
        replicate_means.append(frame.loc[:, expression_names].mean(axis=0))
    common = replicate_means[0].index.intersection(replicate_means[1].index)
    rho, pvalue = stats.spearmanr(replicate_means[0][common], replicate_means[1][common])
    baseline_rows = []
    for feature in common:
        baseline_rows.append({"dataset_id": "gse207628_yang_hyprseq", "feature": feature,
                              "rep1_mean": round(float(replicate_means[0][feature]), 6),
                              "rep2_mean": round(float(replicate_means[1][feature]), 6),
                              "replicate_spearman_rho": round(float(rho), 6),
                              "replicate_spearman_p": float(pvalue)})
    combined = ad.concat(objects, join="inner", merge="same", index_unique=None)
    product_dir.mkdir(parents=True, exist_ok=True)
    combined.write_h5ad(product_dir / "gse207628_hyprseq.h5ad", compression="gzip")
    write_csv(outdir / "gse207628_cell_qc.csv", qc_rows)
    write_csv(outdir / "gse207628_targeted_replicate_baseline.csv", baseline_rows)
    return {"dataset_id": "gse207628_yang_hyprseq", "status": "processed_targeted_readout_guide_assignment_unavailable",
            "observations": int(combined.n_obs), "features": int(combined.n_vars),
            "product_observations": int(combined.n_obs), "product_features": int(combined.n_vars)}


def parse_replogle_label(label: str) -> tuple[str, str, str]:
    parts = label.split("_")
    guide_id = parts[0]
    target = parts[1] if len(parts) > 1 else "unknown"
    gene_id = parts[-1] if parts and parts[-1].startswith("ENSG") else "unknown"
    return guide_id, target, gene_id


def process_replogle(path: Path, outdir: Path, product_dir: Path) -> dict:
    source = ad.read_h5ad(path)
    parsed = [parse_replogle_label(x) for x in source.obs_names.astype(str)]
    obs = source.obs.copy()
    obs["pseudobulk_id"] = source.obs_names.astype(str); obs["cell_id"] = source.obs_names.astype(str)
    obs["dataset_id"] = "replogle_k562_essential"; obs["perturbation"] = [x[1] for x in parsed]
    obs["guide_id"] = source.obs_names.astype(str); obs["target_gene"] = [x[1] for x in parsed]
    obs["control_type"] = np.where(obs["target_gene"].eq("non-targeting"), "non_targeting", "targeting")
    obs["batch"] = "source_pseudobulk_gemgroups_aggregated"; obs["donor"] = "K562_cell_line"
    obs["condition"] = "day6_post_transduction"; obs["cell_type"] = "K562"
    obs["guide_count"] = 2; obs["observation_type"] = "guide_pair_pseudobulk"
    obs["benchmark_control"] = obs["core_control"].astype(bool)
    obs["n_cells"] = obs["num_cells_filtered"]
    var = source.var.copy(); var["gene_id"] = source.var_names.astype(str); var["gene_symbol"] = var["gene_name"].astype(str)
    var["feature_type"] = "Gene Expression"
    converted = ad.AnnData(X=source.X.copy(), obs=obs, var=var)
    converted.layers["counts"] = converted.X.copy()
    converted.uns["dataset_source"] = "Figshare+ article 20029387, file 35773070"
    converted.uns["publication"] = "doi:10.1016/j.cell.2022.05.013"
    converted.uns["benchmark_notes"] = (
        "Author-deposited raw guide-pair pseudobulk, not a cell-level matrix. The counts layer "
        "contains the author's raw pseudobulk expression values and is not asserted to be integer UMI counts."
    )
    product_dir.mkdir(parents=True, exist_ok=True)
    converted.write_h5ad(product_dir / "replogle_k562_essential_raw_pseudobulk_schema.h5ad", compression="gzip")
    qc = [{"dataset_id": "replogle_k562_essential", "n_guide_pair_pseudobulks": converted.n_obs,
           "n_expression_features": converted.n_vars, "n_targeting_pseudobulks": int((obs.control_type == "targeting").sum()),
           "n_non_targeting_pseudobulks": int((obs.control_type == "non_targeting").sum()),
           "source_cells_unfiltered": int(obs.num_cells_unfiltered.sum()),
           "source_cells_filtered": int(obs.num_cells_filtered.sum()),
           "median_cells_per_pseudobulk": float(obs.num_cells_filtered.median()),
           "median_mito_fraction": round(float(obs.mitopercent.median()), 6)}]
    targeting = obs[obs.control_type == "targeting"].copy()
    baseline = [{"dataset_id": "replogle_k562_essential", "metric": "median_target_pct_expression_change",
                 "value": round(float(targeting.pct_expr.median()), 6), "n": int(targeting.pct_expr.notna().sum())},
                {"dataset_id": "replogle_k562_essential", "metric": "fraction_energy_test_fdr_proxy_p_lt_0.05",
                 "value": round(float((targeting.energy_test_p_value < 0.05).mean()), 6), "n": len(targeting)},
                {"dataset_id": "replogle_k562_essential", "metric": "median_filtered_cells_per_targeting_pair",
                 "value": float(targeting.num_cells_filtered.median()), "n": len(targeting)}]
    write_csv(outdir / "replogle_k562_pseudobulk_qc.csv", qc)
    write_csv(outdir / "replogle_k562_paper_native_baseline.csv", baseline)
    return {"dataset_id": "replogle_k562_essential", "status": "processed_author_pseudobulk",
            "observations": int(converted.n_obs), "features": int(converted.n_vars),
            "product_observations": int(converted.n_obs), "product_features": int(converted.n_vars)}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", choices=["all", "gse178317", "gse207628", "replogle"], default="all")
    parser.add_argument("--outdir", type=Path, default=ROOT / "artifacts/real_data")
    parser.add_argument("--product-dir", type=Path, default=ROOT / "data/processed/real_data")
    parser.add_argument("--drager-cells-per-lane", type=int, default=2000)
    parser.add_argument("--gse178317-dir", type=Path, default=ROOT / "data/raw/GSE178317/extracted")
    parser.add_argument("--gse207628-dir", type=Path, default=ROOT / "data/raw/GSE207628/extracted")
    parser.add_argument("--replogle-file", type=Path,
                        default=ROOT / "data/raw/replogle_k562_essential/K562_essential_raw_bulk_01.h5ad")
    args = parser.parse_args()
    args.outdir.mkdir(parents=True, exist_ok=True)
    summaries = []
    if args.dataset in {"all", "gse178317"}:
        summaries.append(process_drager(args.gse178317_dir, args.outdir, args.product_dir,
                                        args.drager_cells_per_lane))
    if args.dataset in {"all", "gse207628"}:
        summaries.append(process_hyprseq(args.gse207628_dir, args.outdir, args.product_dir))
    if args.dataset in {"all", "replogle"}:
        summaries.append(process_replogle(args.replogle_file, args.outdir, args.product_dir))
    write_csv(args.outdir / "real_dataset_status.csv", summaries)
    input_paths = []
    if args.dataset in {"all", "gse178317"}:
        input_paths.extend(sorted(args.gse178317_dir.glob("*.h5")))
    if args.dataset in {"all", "gse207628"}:
        input_paths.extend(sorted(args.gse207628_dir.glob("*.gz")))
    if args.dataset in {"all", "replogle"}:
        input_paths.append(args.replogle_file)
    write_csv(args.outdir / "input_manifest.csv", [
        {"path": display_path(path),
         "bytes": path.stat().st_size, "sha256": sha256(path)}
        for path in input_paths
    ])
    run_parameters = {
        "dataset": args.dataset,
        "outdir": display_path(args.outdir),
        "product_dir": display_path(args.product_dir),
        "drager_cells_per_lane": args.drager_cells_per_lane,
        "gse178317_dir": display_path(args.gse178317_dir),
        "gse207628_dir": display_path(args.gse207628_dir),
        "replogle_file": display_path(args.replogle_file),
    }
    (args.outdir / "run_parameters.json").write_text(json.dumps(run_parameters, indent=2) + "\n")
    manifest = []
    for path in sorted(args.outdir.glob("*")) + sorted(args.product_dir.glob("*.h5ad")):
        if path.name == "output_manifest.csv":
            continue
        manifest.append({"path": display_path(path), "bytes": path.stat().st_size, "sha256": sha256(path)})
    write_csv(args.outdir / "output_manifest.csv", manifest)
    print(json.dumps(summaries, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
