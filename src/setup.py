from setuptools import setup, find_packages
setup(
    name='py_process_data',
    version='0.1',
    description='A module for creating a dataset given a set of dicom files and their contours',
    packages=['py_process_data'],
    author='Pradeep Banavara',
    author_email='pradeepbs@gmail.com',
    keywords=['dicom, mask'],
    install_requires=[
                  'numpy','pydicom', 'pandas'
              ],
    url='https://github.com/pbanavara/ar_assign.git'
)
