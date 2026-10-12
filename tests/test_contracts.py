import csv
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


class ContractTests(unittest.TestCase):
    def test_gwas_corroboration_is_scoped(self):
        path = ROOT / "results/external_corroboration/gwas_catalog_ad_corroboration.csv"
        with path.open(newline="") as handle:
            rows = list(csv.DictReader(handle))
        self.assertGreater(len(rows), 0)
        self.assertTrue(all(row["evidence_scope"] == "disease_relevance_only" for row in rows))
        self.assertTrue(all(row["effect_direction_validated"] == "NO" for row in rows))
        supported = {row["gene"] for row in rows if row["genome_wide_corroboration"] == "YES"}
        self.assertEqual(supported, {"APOE", "INPP5D", "SPI1", "TREM2"})

    def test_app_contract_has_required_traceability(self):
        contract = yaml.safe_load((ROOT / "schemas/app_result_contract.yml").read_text())
        required = set(contract["required_result_identity"])
        self.assertTrue({"dataset_id", "method", "contrast", "n_samples", "n_cells", "provenance_id"} <= required)
        self.assertIn("skipped_inapplicable", contract["method_run_status_enum"])

    def test_active_dataset_catalog_contains_only_implemented_inputs(self):
        datasets = yaml.safe_load((ROOT / "configs/datasets.yml").read_text())["datasets"]
        self.assertEqual(
            {dataset["id"] for dataset in datasets},
            {"demo_synthetic", "drager_microglia_cropseq", "yang_ad_microglia_hyprseq", "replogle_k562_gwps"},
        )

    def test_bundled_regulatory_data_is_explicitly_synthetic(self):
        path = ROOT / "shiny/results/regulatory_validation/regulatory_validation.csv"
        with path.open(newline="") as handle:
            rows = list(csv.DictReader(handle))
        self.assertTrue(rows)
        self.assertIn("is_synthetic", rows[0])
        self.assertTrue(all(row["is_synthetic"].lower() == "true" for row in rows))

    def test_manuscript_claims_point_to_evidence_requirements(self):
        text = (ROOT / "manuscript/review_paper_draft.md").read_text()
        self.assertIn("Evidence-conditioned interpretation", text)
        self.assertIn("dataset, method, contrast, sample count, cell count, and provenance", text)


if __name__ == "__main__":
    unittest.main()
