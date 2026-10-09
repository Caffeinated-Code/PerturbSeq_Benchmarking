import csv
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


class ContractTests(unittest.TestCase):
    def test_app_contract_has_required_traceability(self):
        contract = yaml.safe_load((ROOT / "schemas/app_result_contract.yml").read_text())
        required = set(contract["required_result_identity"])
        self.assertTrue({"dataset_id", "method", "contrast", "n_samples", "n_cells", "provenance_id"} <= required)
        self.assertIn("skipped_inapplicable", contract["method_run_status_enum"])

    def test_resource_registry_has_provenance_and_limitations(self):
        resources = yaml.safe_load((ROOT / "configs/ad_validation_resources.yml").read_text())["resources"]
        self.assertGreaterEqual(len(resources), 4)
        for resource in resources:
            self.assertTrue(resource["access_url"].startswith("https://"))
            self.assertTrue(resource["limitations"])
            self.assertIn(resource["status"], {"registered_not_ingested", "ingested", "unavailable"})

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
