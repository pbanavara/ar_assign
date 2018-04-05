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
        Helper method to parse the dicom and contour files

        :param dicom_file: DICOM file name
        :param contour_file: Contour file name
        :return: Numpy array represetatios of dicom file and label mask
        """
        np_d = parsing.parse_dicom_file(os.path.abspath(dicom_file))
        polys = parsing.parse_contour_file(contour_file)
        mask = parsing.poly_to_mask(polys, np_d.shape[0], np_d.shape[1])
        return np_d, mask

    def create_random_sample(self, data, epochs, sample_size):
        """
        For the given epoch and sample size, this function creates a random sample of sample_size images per epoch
        :param data: The original master dataset - A list of dict mappings between image -> mask
        :param epochs: No of epochs
        :param sample_size: Size of each sample per epoch
        :return:
        """
        final_numpy_data = []
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
            # Todo build the neural net from these images and masks
            final_numpy_data.append((images_np, masks_np))
        return final_numpy_data
