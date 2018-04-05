import os
import pandas as pd

"""
This class encapsulates part 1 of the assignment

This class embodies the dataset creation process and also acts as a placeholder for the dataset
I am in two minds as to use this class as a datastore as opposed to just process and return the data.
Since this assignment asks for a two part pipeline, I've gone ahead to use this class also as a datastore

"""
class Dataset:
    def __init__(self):
        self.data = {}

    def create_dataset(self, csv_file_path, dicom_dir_path, contour_dir_path):
        """

        :param csv_file_path:
        :param dicom_dir_path:
        :param contour_dir_path:
        :return: A list of dictionary objects containing mapping from dicom file name to contour file name
        """
        df = pd.read_csv(csv_file_path)
        dataset = []
        for index, row in df.iterrows():
            dicom_dir = row[0]
            contour_dir = row[1]
            dicom_dir_files = self._read_dicom_files(os.path.join(dicom_dir_path, dicom_dir))
            contour_dir_files = self._read_contour_files(os.path.join(contour_dir_path, contour_dir))
            dataset.append(self._create_dicom_mask_map(dicom_dir_files, contour_dir_files))
        self.data = [item for sublist in dataset for item in sublist]

    def _read_dicom_files(self, dicom_dir):
        """
        Helper method to get all dicom files in a list
        :param dicom_dir: Dicom directory name
        :return: list of all dicom files
        """
        dicom_dir_iterator = os.scandir(dicom_dir)
        f_names = []
        for d in dicom_dir_iterator:
            f_names.append(d)
        return f_names

    def _read_contour_files(self, contour_dir):
        """
        Helper method to list all contour files in the specified directory
        :param contour_dir: Contour directory name
        :return: list of all contour files for that specific contour directory
        """
        contour_file_names = []
        # path = os.path.join('final_data/contourfiles/', contour_dir)
        contour_dir_iterator = os.scandir(contour_dir)
        for d in contour_dir_iterator:
            if d.name == 'i-contours':
                for file in os.scandir(d):
                    # contour_file_names.append(file.name.split(".")[0].split("-")[2].lstrip('0'))
                    contour_file_names.append(file)
        return contour_file_names

    def _split_contour_file(self, x):
        """

        :param x: contour file name containing the absolute path
        :return: just the filename without any extensions
        """
        head, tail = os.path.split(x)
        return tail.split(".")[0].split("-")[2].lstrip('0')

    def _split_dicom_file(self, x):
        """

        :param x:
        :return:
        """
        head, tail = os.path.split(x)
        return tail.split(".")[0]

    def _create_dicom_mask_map(self, d_files, c_files):
        """

        :param d_files:
        :param c_files:
        :return:
        """
        c_files_no_ext = list(map(self._split_contour_file, c_files))
        d_files_no_ext = list(map(self._split_dicom_file, d_files))
        commonalities = list(set(d_files_no_ext).intersection(c_files_no_ext))
        arr = []
        for c in commonalities:
            for x in set(c_files):
                if self._split_contour_file(x) == c:
                    for d in d_files:
                        if self._split_dicom_file(d) == c:
                            arr.append({d: x})
        return arr

    def get_data(self):
        """

        :return: The final dataset
        """
        return self.data


if __name__ == "__main__":
    c = Dataset()