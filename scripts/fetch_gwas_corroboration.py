#!/usr/bin/env python3
"""Fetch Alzheimer disease gene-level corroboration from GWAS Catalog API v2."""

from __future__ import annotations

import argparse
import csv
import json
import time
import urllib.parse
import urllib.request
from pathlib import Path


BASE_URL = "https://www.ebi.ac.uk/gwas/rest/api/v2"
AD_EFO_ID = "MONDO_0004975"
GENOME_WIDE_THRESHOLD = 5e-8
USER_AGENT = "PerturbSeq_Benchmarking/1.0 (public reproducible research)"


def get_json(path: str, params: dict[str, object] | None = None) -> dict:
    url = f"{BASE_URL}/{path}"
    if params:
        url = f"{url}?{urllib.parse.urlencode(params)}"
    request = urllib.request.Request(url, headers={"Accept": "application/json", "User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=60) as response:
        return json.load(response)


def candidate_genes(effect_path: Path) -> list[str]:
    with effect_path.open(newline="") as handle:
        rows = list(csv.DictReader(handle))
    genes = {row["perturbation"] for row in rows}
    genes.update(row["gene"] for row in rows if row["effect_direction"] != "neutral")
    return sorted(genes)


def strongest_association(records: list[dict]) -> dict:
    return min(records, key=lambda row: float(row.get("p_value", 1.0))) if records else {}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--effects", type=Path, default=Path("results/method/simple_pseudobulk_effects.csv"))
    parser.add_argument("--outdir", type=Path, default=Path("results/external_corroboration"))
    args = parser.parse_args()
    args.outdir.mkdir(parents=True, exist_ok=True)

    metadata = get_json("metadata")
    rows = []
    for gene in candidate_genes(args.effects):
        payload = get_json(
            "associations",
            {
                "efo_id": AD_EFO_ID,
                "show_child_trait": "true",
                "mapped_gene": gene,
                "extended_geneset": "false",
                "sort": "p_value",
                "direction": "asc",
                "size": 20,
            },
        )
        records = payload.get("_embedded", {}).get("associations", [])
        best = strongest_association(records)
        best_p = best.get("p_value", "")
        genome_wide = bool(records) and float(best_p) <= GENOME_WIDE_THRESHOLD
        variants = ";".join(best.get("snp_effect_allele", []))
        rows.append(
            {
                "gene": gene,
                "ad_mapped_association_count": payload.get("page", {}).get("totalElements", 0),
                "genome_wide_corroboration": "YES" if genome_wide else "NO",
                "catalog_association_returned": "YES" if records else "NO",
                "representative_association_id": best.get("association_id", ""),
                "representative_variant": variants,
                "representative_p_value": best_p,
                "representative_study": best.get("accession_id", ""),
                "representative_pubmed_id": best.get("pubmed_id", ""),
                "efo_id": AD_EFO_ID,
                "evidence_scope": "disease_relevance_only",
                "effect_direction_validated": "NO",
                "genome_wide_threshold": GENOME_WIDE_THRESHOLD,
                "api_release_date": metadata.get("data_release_date", ""),
            }
        )
        time.sleep(0.08)

    output = args.outdir / "gwas_catalog_ad_corroboration.csv"
    with output.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    provenance = {
        "resource": "NHGRI-EBI GWAS Catalog",
        "endpoint": f"{BASE_URL}/associations",
        "trait": "Alzheimer disease",
        "efo_id": AD_EFO_ID,
        "data_release_date": metadata.get("data_release_date"),
        "gene_build": metadata.get("gene_build"),
        "dbsnp_build": metadata.get("dbsnp_build"),
        "query_rule": "Mapped-gene associations for MONDO_0004975 and child traits; extended gene set disabled.",
        "genome_wide_threshold": GENOME_WIDE_THRESHOLD,
        "interpretation": "Corroborates disease-locus relevance only. It does not validate perturbation effects, direction, or cell context.",
    }
    (args.outdir / "gwas_catalog_provenance.json").write_text(json.dumps(provenance, indent=2) + "\n")


if __name__ == "__main__":
    main()
