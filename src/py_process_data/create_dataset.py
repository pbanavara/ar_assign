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
        Function to create the dataset in raw form. The goal is to create 1-1 mappings between image files and their
        respective masks. Uses the initial high level directory mapping provided by a CSV file.
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
            i_contour_files, o_contour_files = self._read_contour_files(os.path.join(contour_dir_path, contour_dir))
            dataset.append(self._create_dicom_contour_map(dicom_dir_files, i_contour_files, o_contour_files))
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
        :return: list of both inner and outer contour files for that specific contour directory
        """
        i_contour_file_names = []
        o_contour_file_names = []
        contour_dir_iterator = os.scandir(contour_dir)
        for d in contour_dir_iterator:
            if d.name == 'i-contours':
                for file in os.scandir(d):
                    i_contour_file_names.append(file)
            elif d.name == 'o-contours':
                for file in os.scandir(d):
                    o_contour_file_names.append(file)
        i_files_no_ext = list(map(self._split_contour_file, i_contour_file_names))
        o_files_no_ext = list(map(self._split_contour_file, o_contour_file_names))
        # Find the common file names between i_contour and o_contour
        commonalities = list(set(o_files_no_ext).intersection(i_files_no_ext))
        f_i_contour_file_names = [i for i in i_contour_file_names if self._split_contour_file(i) in commonalities]
        f_o_contour_file_names = [i for i in o_contour_file_names if self._split_contour_file(i) in commonalities]

        return f_i_contour_file_names, f_o_contour_file_names



    def _split_contour_file(self, x):
        """
        Helper method to test the splitting of contour file path to get the most relevant part of the file path

        :param x: contour file name containing the absolute path
        :return: just the filename without any extensions
        """
        head, tail = os.path.split(x)
        return tail.split(".")[0].split("-")[2].lstrip('0')

    def _split_dicom_file(self, x):
        """
        Helper method to split the dicom file path to extract the most relevant part of the filename

        :param x:
        :return:
        """
        head, tail = os.path.split(x)
        return tail.split(".")[0]

    def _create_dicom_contour_map(self, d_files, i_c_files, o_c_files):
        """
        Helper method to map the dicom file and the mask file. This is done by brute force looping
        which isn't the most ideal way, since the data volume is small this works.
        The matchig is done using the relevant parts of the filenames.
        :param d_files:
        :param c_files:
        :return: An array containing the dicom file -> (i_contour, o_contour) file maps
        """
        i_c_files_no_ext = list(map(self._split_contour_file, i_c_files))
        d_files_no_ext = list(map(self._split_dicom_file, d_files))
        commonalities = list(set(d_files_no_ext).intersection(i_c_files_no_ext))
        arr = []
        i_c_f_names = list(map(lambda x: x.name, i_c_files))
        o_c_f_names = list(map(lambda x: x.name, o_c_files))
        for c in commonalities:
            for i, o in zip(sorted(i_c_f_names), sorted(o_c_f_names)):
                if self._split_contour_file(i) == c:
                    for d in d_files:
                        if self._split_dicom_file(d) == c:
                            arr.append({d: (self._map_name_to_directory(i, i_c_files),
                                            self._map_name_to_directory(o, o_c_files))})
        return arr

    def _map_name_to_directory(self, x, files):
        for f in files:
            if x == f.name:
                return f

    def get_data(self):
        """

        :return: The final dataset
        """
        return self.data


if __name__ == "__main__":
    c = Dataset()