import importlib.util
import tempfile
import unittest
from pathlib import Path

import h5py
import numpy as np
from scipy import sparse


MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts/process_real_datasets.py"
SPEC = importlib.util.spec_from_file_location("real_data", MODULE_PATH)
real_data = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(real_data)


class RealDataProcessingTests(unittest.TestCase):
    def test_deterministic_rows_is_reproducible_and_bounded(self):
        np.testing.assert_array_equal(real_data.deterministic_rows(10, 4), [0, 3, 6, 9])
        np.testing.assert_array_equal(real_data.deterministic_rows(3, 4), [0, 1, 2])
        np.testing.assert_array_equal(real_data.deterministic_rows(3, 0), [0, 1, 2])

    def test_replogle_label_parser_preserves_controls(self):
        self.assertEqual(
            real_data.parse_replogle_label("10753_non-targeting_non-targeting_non-targeting"),
            ("10753", "non-targeting", "unknown"),
        )
        self.assertEqual(
            real_data.parse_replogle_label("10023_ZC3H18_P1P2_ENSG00000158545"),
            ("10023", "ZC3H18", "ENSG00000158545"),
        )

    def test_read_10x_h5_orientation(self):
        matrix = sparse.csc_matrix(np.array([[1, 0, 2], [0, 3, 0]], dtype=np.int32))
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "tiny.h5"
            with h5py.File(path, "w") as handle:
                group = handle.create_group("matrix")
                group.create_dataset("data", data=matrix.data)
                group.create_dataset("indices", data=matrix.indices)
                group.create_dataset("indptr", data=matrix.indptr)
                group.create_dataset("shape", data=matrix.shape)
                group.create_dataset("barcodes", data=np.array([b"c1", b"c2", b"c3"]))
                features = group.create_group("features")
                features.create_dataset("id", data=np.array([b"g1", b"g2"]))
                features.create_dataset("name", data=np.array([b"A", b"MT-B"]))
            loaded, barcodes, ids, names = real_data.read_10x_h5(path)
            self.assertEqual(loaded.shape, (3, 2))
            np.testing.assert_array_equal(loaded.toarray(), matrix.toarray().T)
            self.assertEqual(barcodes.tolist(), ["c1", "c2", "c3"])
            self.assertEqual(ids.tolist(), ["g1", "g2"])
            self.assertEqual(names.tolist(), ["A", "MT-B"])


if __name__ == "__main__":
    unittest.main()
