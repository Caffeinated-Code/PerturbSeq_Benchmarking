"""Evidence typing and conservative tier assignment.

Tiers summarize independent corroboration around a completed perturbation result.
They are not causal grades and never upgrade observational evidence to perturbation evidence.
"""

REQUIRED_EVIDENCE_FIELDS = {
    "result_id", "evidence_id", "evidence_type", "source_id", "source_url",
    "source_version", "dataset_id", "method", "contrast", "n_samples", "n_cells",
    "cell_type", "disease_state", "direction", "direction_consistency",
    "evidence_status", "is_perturbational", "is_synthetic", "retrieved_at",
}

EVIDENCE_TYPES = {
    "perturbation", "expression_state", "accessible_chromatin", "disease_association",
    "qtl", "peak_to_gene", "tf_motif_regulon", "pathway_concordance",
    "clinical_annotation",
}


def validate_evidence_record(record):
    missing = sorted(REQUIRED_EVIDENCE_FIELDS - set(record))
    if missing:
        raise ValueError(f"missing evidence fields: {', '.join(missing)}")
    if record["evidence_type"] not in EVIDENCE_TYPES:
        raise ValueError(f"unknown evidence_type: {record['evidence_type']}")
    if bool(record["is_perturbational"]) != (record["evidence_type"] == "perturbation"):
        raise ValueError("is_perturbational must be true only for perturbation evidence")
    if record["evidence_status"] not in {"observed", "not_observed", "not_tested", "unavailable"}:
        raise ValueError("invalid evidence_status")
    return True


def assign_evidence_tier(records):
    """Return an evidence tier and auditable reasons for one result.

    Tier A requires replicated perturbation evidence plus independent human AD/microglia
    regulatory support. Tier B requires one completed perturbation result and at least
    two independent observational evidence classes, including a regulatory link.
    Tier C reports a completed perturbation result with limited corroboration. Tier D
    means no eligible biological tier (including all-synthetic inputs).
    """
    records = list(records)
    for record in records:
        validate_evidence_record(record)
    eligible = [r for r in records if not bool(r["is_synthetic"]) and r["evidence_status"] == "observed"]
    if not eligible:
        return {"tier": "D", "label": "not biologically assessed", "reasons": ["no eligible non-synthetic observed evidence"]}

    perturb = [r for r in eligible if r["evidence_type"] == "perturbation"]
    perturb_sources = {r["source_id"] for r in perturb}
    observational = {r["evidence_type"] for r in eligible if r["evidence_type"] != "perturbation"}
    sources = {r["source_id"] for r in eligible if r["evidence_type"] != "perturbation"}
    regulatory_link = bool(observational & {"peak_to_gene", "qtl"})
    human_context = any(r["cell_type"].lower() == "microglia" and r["disease_state"].lower() not in {"unknown", "not_applicable"} for r in eligible)
    inconsistent = any(r["direction_consistency"] == "inconsistent" for r in eligible)

    if len(perturb_sources) >= 2 and regulatory_link and human_context and len(sources) >= 2 and not inconsistent:
        return {"tier": "A", "label": "replicated perturbation with independent regulatory corroboration", "reasons": sorted(observational)}
    if perturb and regulatory_link and len(observational) >= 2 and len(sources) >= 2 and not inconsistent:
        return {"tier": "B", "label": "perturbation with multi-source observational corroboration", "reasons": sorted(observational)}
    if perturb:
        reasons = ["completed perturbation evidence"]
        if inconsistent:
            reasons.append("directional inconsistency prevents a higher tier")
        return {"tier": "C", "label": "perturbation result with limited or mixed corroboration", "reasons": reasons}
    return {"tier": "D", "label": "observational context only", "reasons": sorted(observational)}

