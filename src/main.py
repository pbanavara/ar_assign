import argparse
from py_process_data.create_dataset import Dataset
import os
from py_process_data.process_dataset import ProcessDataset


def main(csv_file, dicom_file, contour_file, epochs, sample_size):
    c = Dataset()
    csv_file = os.path.abspath(csv_file)
    dicom_file = os.path.abspath(dicom_file)
    contour_file = os.path.abspath(contour_file)
    c.create_dataset(csv_file, dicom_file, contour_file)
    data = c.get_data()
    p = ProcessDataset()
    images_np, masks_np = p.create_random_sample(data, epochs, sample_size)
    print(images_np.shape, masks_np.shape)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("csv_file")
    parser.add_argument("dicom_file")
    parser.add_argument("contour_file")
    parser.add_argument("epochs", type=int)
    parser.add_argument("sample_size", type=int)
    args = parser.parse_args()
    main(args.csv_file, args.dicom_file, args.contour_file, args.epochs, args.sample_size)
