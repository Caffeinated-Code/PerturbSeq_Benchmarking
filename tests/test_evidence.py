import unittest

from perturbseq_benchmark.evidence import assign_evidence_tier, validate_evidence_record


def record(evidence_id, evidence_type, source_id, synthetic=False, consistency="consistent"):
    return {
        "result_id": "r1", "evidence_id": evidence_id, "evidence_type": evidence_type,
        "source_id": source_id, "source_url": "https://example.org/source",
        "source_version": "2026-01", "dataset_id": "d1", "method": "m1",
        "contrast": "target_vs_control", "n_samples": 3, "n_cells": 100,
        "cell_type": "microglia", "disease_state": "AD", "direction": "up",
        "direction_consistency": consistency, "evidence_status": "observed",
        "is_perturbational": evidence_type == "perturbation", "is_synthetic": synthetic,
        "retrieved_at": "2026-10-09",
    }


class EvidenceTests(unittest.TestCase):
    def test_synthetic_records_never_receive_biological_tier(self):
        self.assertEqual(assign_evidence_tier([record("e1", "perturbation", "demo", True)])["tier"], "D")

    def test_database_overlap_alone_is_observational_only(self):
        rows = [record("e1", "disease_association", "gwas"), record("e2", "clinical_annotation", "clinvar")]
        self.assertEqual(assign_evidence_tier(rows)["tier"], "D")

    def test_tier_b_requires_perturbation_regulatory_link_and_independent_sources(self):
        rows = [record("e1", "perturbation", "screen"), record("e2", "peak_to_gene", "regulome"), record("e3", "accessible_chromatin", "sea_ad")]
        self.assertEqual(assign_evidence_tier(rows)["tier"], "B")

    def test_direction_conflict_caps_tier(self):
        rows = [record("e1", "perturbation", "screen"), record("e2", "peak_to_gene", "regulome"), record("e3", "accessible_chromatin", "sea_ad", consistency="inconsistent")]
        self.assertEqual(assign_evidence_tier(rows)["tier"], "C")

    def test_type_boolean_cannot_disagree(self):
        row = record("e1", "qtl", "regulome")
        row["is_perturbational"] = True
        with self.assertRaises(ValueError):
            validate_evidence_record(row)


if __name__ == "__main__":
    unittest.main()

