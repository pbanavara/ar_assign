### Readme file with the required explanations for the test

#### Usage
* The required files are bundled as a package/module
* Checkout the repository
* `cd src`
* `python setup.py install`

####How did you verify that you are parsing the contours correctly?
I visually verified that the contours were in accordance with the original image after applying the mask.
Especially the left ventricle contour/mask

####What changes did you make to the code, if any, in order to integrate it into our production code base? 
* I removed an unwanted try except block in the parse_dicom function
* I removed the dictionary with the hardcoded 'pixel-value' string. Instead I just returned the image pixcel array
    * One option could have been to return a dictionary with the filename as the key but that seemed an overkill

####Did you change anything from the pipelines built in Parts 1 to better streamline the pipeline built in Part 2? If so, what? If not, is there anything that you can imagine changing in the future?
I actually built part 1 and 2 as independent as possible. So part 1 is wholly contained in it's
own class. 
In part 1 I created a dataset which is nothing but a list of mapping from imagefile->maskfile
In part 2 I converted this mapping to a map of numpy arrays and did the required random sampling

So these two parts are completely de-coupled and somewhat immutable since the 
data contained in the class after processing part 1 is left unmodified in part 2

####How do you/did you verify that the pipeline was working correctly?

The most critical part of the pipeline was matching the dicom file with the contour file
I did this by matching the file names
IM-0001-0139-icontour-manual.txt and 139.dcm 
For example
This resulted in a lot of contour files not matching with the label masks as the label masks
were missing.
The other critical parts of the pipeline were the actual parsing of
Dicom and mask files.
I wrote tests to ensure that these aspects were covered.

####Given the pipeline you have built, can you see any deficiencies that you would change if you had more time? If not, can you think of any improvements/enhancements to the pipeline that you could build in?
Yes, the matching of DICOM and contour files is at least o(n^2) complexity
I did this in the following way:
* Get all the Dicom file names without extensions
* Find the matching Contour file names by using set intersection
* Then iterate through the common file name entities 129, 128 etc
* For each entity find a matching entity in the DICOM file name and contour file names

I think there is a better way of doing this.

* I have built this pipeline with somewhat of a message passing paradigm.
* I haven't tested this on parallel processing, especially the random sampling part
* Random sampling potentially has a bug - A set of random sample entities are taken repeatedly. 
Given the small size of the dataset, there are chances of collision

#### Notes
* Since the endpoint of the pipeline is to emit numpy arrays, I put a logical end by storing a sample
of the epoch in images. Have noted the TODO sections in the files accordingly