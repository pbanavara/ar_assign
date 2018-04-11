##### Adding o-contours
Using your code from Phase 1, add the parsing of the o-contours into your pipeline. Note that there are only half the number of o-contour files as there are i-contour files, so not every i-contour will have a corresponding o-contour.

After building the pipeline, please discuss any changes that you made to the pipeline you built in Phase 1, and why you made those changes.
#####Solution
* Choose the o-contour file names from the directory.
* Match these with the i-contour names
* Add both the i-contour and matching o-contour names in the dictionary

    * `def _create_dicom_contour_map(self, d_files, i_c_files, o_c_files):`
    * This method now returns a dict of Tuples
    * `{<dicom_file>: (i_contour_file, o_contour_file)`
* Process the additional contour file name in the dictionary accordingly in the pipeline
    * For instance, In `Process_dataset.py._parse_files` Add the additional masks method for the o_contours
* Change the Tests for `create_dicom_contour_map` accordingly
* Both the contour masks are saved in the sample_masks.png file

####Let’s assume that you want to create a system to outline the boundary of the blood pool (i-contours), and you already know the outer border of the heart muscle (o-contours). Compare the differences in pixel intensities inside the blood pool (inside the i-contour) to those inside the heart muscle (between the i-contours and o-contours)

##### Proposed solution in file main.ipynb

* I used the masks and the contours to determine the differences
    * Get the outside contour masks
    * Get the inside contour masks
    * Take the difference between them
    * This gives the masks in between i_contours and o_contours
    * Obtain the pixel intensities using np.argwhere - provides the indices of True pixel masks 
    * Now I have the pixel intensities of pixels inside the contour and 
    the pixels in-between
    * The means of the intensities show an enormous variation. The distribution is also different
      as seen in the histogram.
    * However the standard deviation for both the pixel intensities indicate that most of the
    pixels are centered around the mean. This shows that the pixels are not distributed widely.
    * The histogram re-iterates this as well.

####could you use a simple thresholding scheme to automatically create the i-contours, given the o-contours? Why or why not? Show figures that help justify your answer.

##### Proposed solution.
* Based on the above analysis I manually found out some thresholds.
* From the above analysis we know the pixel intensities of pixels inside the contour
  (We are not taking the boundary into consideration here, our goal is to estimate the boundary)
* We know the boundary of the outside contour.
* we threshold the pixels inside this boundary with the pixel intensities obtained above by using a
euclidean distance measure
* If this distance or the difference in intensities should be around the mean difference, we get a
  reasonable inside boundary.
* So with just the outside boundary and the pixel intensities we can get a range of inside contours.
* However, if just the outside contours are given, without any other information, I don't know how to determine
the inside contours

####Do you think that any other heuristic (non-machine learning)-based approaches, besides simple thresholding, would work in this case

##### Some thoughts around this.

* Given the polygon shape of the contour, we can potentially crop only that portion of the image.
* We can get the top left and bottom right corners and use this information to crop the image
* Then we could use a background/foreground segmentation based on pixel intensities since we are dealing
only with a binary intensity variation here.
* We can't employ this technique without cropping since the dark intensities and light intensities are spread
all over the image.



    

