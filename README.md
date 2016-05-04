# BlobFinder
Finds Red Cup and Red Bowl

## Installation
Make sure you have the latest scipy and matplotlib, and then just clone the
repo. If you want to use pictureTaker.py then you need to get fswebcam as well,
but it is only availble in \*nix systems.
This project was written in Python 2.7 with no promise of support on Python 3.

## Usage
To use the blob finder you need to have an image of just the background, plus
the image including the object you want to locate. All the tools can be called
from the command line.

### Images
You can use anything you want to take the background and target images so long
as it can be read by scipy.ndimage.imread(). It will be read in and then
converted to grayscale.

#### pictureTaker
There is a picture taking function. Make sure you have fswebcam installed.
##### Sample Usage
$ python pictureTaker.py filename

$ python pictureTaker.py filename -d /dev/video0 -r 1000x1000

$ python pictureTaker.py filename --device /dev/video0 -resolution 1000x1000

### blobFinder
The blobFinder takes as input the target and background images filepaths. It
 loads them up and grayscales them before subtracting the two (wrapped inside
 and absolute value function). A gaussian filter is then applied to get rid of
 any small movements/noise followed by a hard cutoff threshold.

Scipy.ndimage.label and then scipy.ndimage.center_of_mass are then used to find
the center of mass location of the labelled object. The coordinates returned
are from the top left corner, increasing x going rightward and increasing y
going downward.

#### Sample Usage
$ python blobFinder.py targetImageFilepath backgroundImageFilepath

$ python blobFinder.py targetImageFilepath backgroundImageFilepath --threshold 60 --filterSigma 39

## Issues

* The label function tends to lump shadows in with the object.
* Value of threshold and filterSigma have to be tuned (maybe each time?)
* Need to calibrate from pixel to milimeter somehow.
