import numpy as np
from py_process_data import parsing
import os

"""
This class encapsulates part 2 of the assignment. The dataset is converted into numpy arrays for the
specified epochs and sample size.
"""

class ProcessDataset:

    def _parse_files(self, dicom_file, contour_file):
        """

        :param dicom_file:
        :param contour_file:
        :return:
        """
        np_d = parsing.parse_dicom_file(os.path.abspath(dicom_file))['pixel_data']
        polys = parsing.parse_contour_file(contour_file)
        mask = parsing.poly_to_mask(polys, np_d.shape[0], np_d.shape[1])
        return np_d, mask

    def create_random_sample(self, data, epochs, sample_size):
        """

        :param data:
        :param epochs:
        :param sample_size:
        :return:
        """
        for e in range(epochs):
            sample = np.random.choice(data, sample_size)
            images = []
            masks = []
            for s in sample:
                for d, c in s.items():
                    np_d, mask = self._parse_files(d, c)
                    images.append(np_d)
                    masks.append(mask)
            images_np = np.asarray(images)
            masks_np = np.asarray(masks)
            return images_np, masks_np