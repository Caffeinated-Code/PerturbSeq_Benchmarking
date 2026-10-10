#!/usr/bin/env python3
"""Download lightweight public files and write a provenance manifest."""

from __future__ import annotations

import argparse
import csv
import hashlib
from pathlib import Path
from urllib.request import urlretrieve


ROOT = Path(__file__).resolve().parents[1]

PUBLIC_FILES = [
    {
        "dataset_id": "yang_ad_microglia_hyprseq",
        "accession": "GSE207628",
        "file_role": "raw_targeted_count_matrices",
        "url": "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE207nnn/GSE207628/suppl/GSE207628_RAW.tar",
        "local_path": "data/raw/GSE207628/GSE207628_RAW.tar",
        "download_policy": "included_small_public_file",
        "expected_sha256": "8144525b3d5e63ea6cc24ecde4c94a445343d996c1de797ab8dfb57c2f7ba90c",
    },
    {
        "dataset_id": "yang_ad_microglia_hyprseq",
        "accession": "GSE207628",
        "file_role": "hyprseq_probe_panel",
        "url": "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE207nnn/GSE207628/suppl/GSE207628_probes_hyprseq.tsv.gz",
        "local_path": "data/raw/GSE207628/GSE207628_probes_hyprseq.tsv.gz",
        "download_policy": "included_small_public_file",
        "expected_sha256": "92eee5cc6e241e01d68f4ad54b5069de753d6df83c0fa5a2d36dc9ac5c416205",
    },
    {
        "dataset_id": "drager_microglia_cropseq",
        "accession": "GSE178317",
        "file_role": "microglia_bulk_abundance_context",
        "url": "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE178nnn/GSE178317/suppl/GSE178317_iTF_Microglia_RNAseq_abundance.csv.gz",
        "local_path": "data/raw/GSE178317/GSE178317_iTF_Microglia_RNAseq_abundance.csv.gz",
        "download_policy": "included_small_public_file",
        "expected_sha256": "",
    },
]

LARGE_FILES = [
    {
        "dataset_id": "drager_microglia_cropseq",
        "accession": "GSE178317",
        "file_role": "cropseq_raw_archive",
        "url": "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE178nnn/GSE178317/suppl/GSE178317_RAW.tar",
        "local_path": "data/raw/GSE178317/GSE178317_RAW.tar",
        "download_policy": "large_file_skip_by_default",
        "expected_sha256": "1fedaf717380a7d858544be56d1253f4c5bc6f7738f85833c5c1209d32e8fde2",
    },
    {
        "dataset_id": "replogle_k562_essential",
        "accession": "figshare_plus_20029387",
        "file_role": "author_raw_guide_pair_pseudobulk",
        "url": "https://ndownloader.figshare.com/files/35773070",
        "local_path": "data/raw/replogle_k562_essential/K562_essential_raw_bulk_01.h5ad",
        "download_policy": "large_file_skip_by_default",
        "expected_sha256": "80de95e54fcbca0e0537d569b43ec92fde6bd0482801505504baebe3118dcadf",
    }
]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def write_manifest(rows: list[dict[str, str]], outdir: Path) -> None:
    outdir.mkdir(parents=True, exist_ok=True)
    fields = [
        "dataset_id",
        "accession",
        "file_role",
        "url",
        "local_path",
        "download_policy",
        "status",
        "bytes",
        "expected_sha256",
        "sha256",
    ]
    with (outdir / "download_manifest.csv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    provenance = [
        {
            "dataset_id": "yang_ad_microglia_hyprseq",
            "accession": "GSE207628",
            "biology": "Alzheimer risk-locus CRISPRi in human iPSC-derived microglia",
            "readout": "targeted single-cell HYPR-seq count panel",
            "public_source": "https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE207628",
            "current_use": "real targeted count-matrix audit and panel-level QC",
            "scaling_note": "suitable for local demo and AWS Batch conversion",
        },
        {
            "dataset_id": "drager_microglia_cropseq",
            "accession": "GSE178317",
            "biology": "human iPSC-derived microglia CRISPRi/a perturbation biology",
            "readout": "CROP-seq raw archive plus public RNA abundance context",
            "public_source": "https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE178317",
            "current_use": "real abundance-context audit; full CROP-seq archive is a scale-up input",
            "scaling_note": "process the raw archive with Nextflow on workstation, HPC, or AWS Batch",
        },
        {
            "dataset_id": "replogle_k562_essential",
            "accession": "figshare_plus_20029387",
            "biology": "K562 day-6 essential-scale dual-guide CRISPRi Perturb-seq",
            "readout": "author-deposited raw guide-pair pseudobulk expression",
            "public_source": "https://doi.org/10.25452/figshare.plus.20029387",
            "current_use": "real pseudobulk QC and author-statistic baseline",
            "scaling_note": "use the 10 GB single-cell object for cell-level analysis",
        },
    ]
    with (outdir / "public_dataset_provenance.csv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(provenance[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(provenance)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--outdir", default="results/real_public")
    parser.add_argument("--include-large", action="store_true")
    args = parser.parse_args()

    rows: list[dict[str, str]] = []
    files = PUBLIC_FILES + (LARGE_FILES if args.include_large else [])
    if not args.include_large:
        rows.extend([{**row, "status": "skipped", "bytes": "", "sha256": ""} for row in LARGE_FILES])

    for item in files:
        local_path = ROOT / item["local_path"]
        local_path.parent.mkdir(parents=True, exist_ok=True)
        status = "exists"
        if not local_path.exists():
            status = "downloaded"
            urlretrieve(item["url"], local_path)
        actual_sha256 = sha256(local_path)
        expected = item.get("expected_sha256", "")
        if expected and actual_sha256 != expected:
            raise ValueError(f"checksum mismatch for {local_path}: {actual_sha256} != {expected}")
        rows.append({**item, "status": f"{status}_verified" if expected else status,
                     "bytes": str(local_path.stat().st_size), "sha256": actual_sha256})

    write_manifest(rows, ROOT / args.outdir)
    print(f"Wrote public dataset manifest to {ROOT / args.outdir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
