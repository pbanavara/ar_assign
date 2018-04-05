import argparse
from py_process_data.create_dataset import Dataset
import os
from py_process_data.process_dataset import ProcessDataset
import numpy as np
import matplotlib.pyplot as plt

SAMPLE_FILE_NAME = 'sample.png'
MASK_FILE_NAME = 'sample_mask.png'


def main(csv_file, dicom_dir, contour_dir, epochs, sample_size):
    """
    Main API to test both parts of the pipeline.
    Part 1 - Create the dataset with the desired format
    Part 2 - process the dataset and create the required numpy arrays
    :param csv_file: CSV file containing the mappings
    :param dicom_dir: Dicom directory location
    :param contour_dir: Contour directory location
    :param epochs: No of required training epochs
    :param sample_size: Sample size for each epoch
    :return: None
    """
    c = Dataset()
    csv_file = os.path.abspath(csv_file)
    dicom_dir = os.path.abspath(dicom_dir)
    contour_dir = os.path.abspath(contour_dir)
    c.create_dataset(csv_file, dicom_dir, contour_dir)
    data = c.get_data()
    process_data = ProcessDataset()
    image_mask_list = process_data.create_random_sample(data, epochs, sample_size)
    print("A sample shape from the image mask list {}".format(image_mask_list[0][0].shape))
    print("Sample batch images are stored in the current working directory {}, {}".format(
        SAMPLE_FILE_NAME, MASK_FILE_NAME))
    plt.imshow(np.hstack(image_mask_list[0][0]))
    plt.savefig(SAMPLE_FILE_NAME)
    plt.imshow(np.hstack(image_mask_list[0][1]))
    plt.savefig(MASK_FILE_NAME)




if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("csv_file")
    parser.add_argument("dicom_file")
    parser.add_argument("contour_file")
    parser.add_argument("epochs", type=int)
    parser.add_argument("sample_size", type=int)
    args = parser.parse_args()
    main(args.csv_file, args.dicom_file, args.contour_file, args.epochs, args.sample_size)
