from scipy.ndimage import imread, label, center_of_mass, gaussian_filter
from argparse import ArgumentParser
from matplotlib import pyplot as plt

def imLoad(fname):
    """
    Given the filename of an image, the function will load it into memory and
    grayscale it.
    """
    img = imread(fname)
    r, g, b = img[:,:,0], img[:,:,1], img[:,:,2]
    gray = 0.2989*r + 0.5870*g + 0.1140*b
    return gray

def findBlob(tgtImg, refImg, filterSigma=39, threshold=60):
    """
    Given a target Image and a reference Image (background), finds the center
    of mass of a the one blob in the image.
    Returns the coordinates of the blob's center of mass
    """
    img = abs(tgtImg - refImg)              # Remove background
    img = gaussian_filter(img,filterSigma)  # Filter out some noise
    img[img<threshold] = 0                  # Truncate low intensities to zero

    labeledArray, numFeatures = label(img)
    plt.subplot(221)
    plt.imshow(img)
    plt.subplot(223)
    plt.imshow(labeledArray)
    plt.show()
    assert 0<numFeatures<2, "There are {} recognized objects, there can only be one".format(numFeatures)

    coord = center_of_mass(labeledArray)
    return coord

def blobCoord(fnameTgt, fnameRef):
    tgtImg = imLoad(fnameTgt)
    refImg = imLoad(fnameRef)
    coord = findBlob(tgtImg,refImg)
    return coord

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('tgtFname', help='Filepath to target image')
    parser.add_argument('refFname', help='Filepath to reference image')
    args = parser.parse_args()
    print blobCoord(args.tgtFname, args.refFname)
