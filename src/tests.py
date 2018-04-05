from py_process_data.create_dataset import Dataset
import os
from py_process_data.process_dataset import ProcessDataset
from py_process_data import parsing
import unittest
import numpy.testing as npt


class TestDatasetCreate(unittest.TestCase):
    def setUp(self):
        unittest.TestCase.setUp(self)
        self.dataset = Dataset()

    def test_parse_dicom_file(self):
        dicom_file = os.path.abspath('../final_data/dicoms/SCD0000101/1.dcm')
        npt.assert_almost_equal(parsing.parse_dicom_file(dicom_file)['pixel_data'].shape, (256, 256))

if __name__ == "__main__":
    unittest.main()