from scipy.ndimage import imread, label, center_of_mass, gaussian_filter, sobel
from numpy import nonzero, argmax, arctan2
from argparse import ArgumentParser
from matplotlib import pyplot as plt

class Blob:
    def __init__(self, x, y, farX, farY):
        self.x, self.y = x, y
        self._fx, self._fy = farX, farY

        self.orientationVector = farX - x, farY - y
        self.orientation = arctan2(farY-y, farX-x)

    def getLocation(self):
        return self.x, self.y

    def getOrientation(self):
        return self.orientation

    def __str__(self):
        return 'Center: {}, Orientation: {}'.format(self.getLocation(),self.getOrientation())

class BlobFinder:
    def __init__(self, tgtFname, refFname):
        tgtImg = self._imLoad(tgtFname)
        refImg = self._imLoad(refFname)
        self.image = abs(tgtImg - refImg)

    def _imLoad(self, fname):
        """
        Given the filename of an image, the function will load it into memory and
        grayscale it.
        """
        img = imread(fname)
        r, g, b = img[:,:,0], img[:,:,1], img[:,:,2]
        gray = 0.2989*r + 0.5870*g + 0.1140*b
        return gray

    def findBlob(self, cutoff=100, sigma=3):
        self.highPassImage = self._highPass(self.image, cutoff)
        self.filterImage   = self._filter(self.highPassImage, sigma)
        self.labeledImage, numFeatures = self._label(self.filterImage)

        assert 0<numFeatures<2, "There are {} recognized objects, there can only be one".format(numFeatures)
        y, x = self._findCenter(self.labeledImage)
        farY, farX  = self._findFarEdge(self.labeledImage)
        blob = Blob(x, y, farX, farY)
        return blob

    def _highPass(self, image, cutoff):
        hpImage = image.copy()
        hpImage[hpImage<cutoff] = 0
        return hpImage

    def _filter(self, image, sigma):
        gfImage = gaussian_filter(image, sigma)
        return gfImage

    def _label(self, image):
        return label(image)

    def _findCenter(self, labeledImage):
        return center_of_mass(labeledImage)

    def _findEdges(self, image):
        simg = sobel(image)
        simg[simg!=0] = 1
        return simg

    def _2dNorm(self, x0, y0, x1, y1):
        return ((x0 - x1)**2 + (y0 - y1)**2)**0.5

    def _findFarEdge(self, labeledImage):
        center = self._findCenter(labeledImage)
        edgeImg= self._findEdges(labeledImage)

        ys, xs = nonzero(edgeImg)
        distancesFromCenter= self._2dNorm(center[1], center[0], ys, xs)

        indFarthest = argmax(distancesFromCenter)
        farY, farX = ys[indFarthest], xs[indFarthest]
        return farY, farX


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('tgtFname', help='Filepath to target image')
    parser.add_argument('refFname', help='Filepath to reference image')
    parser.add_argument('--sigma', default=3, type=int, help='Value of Sigma in gaussian_filter')
    parser.add_argument('--cutoff', default=100, type=int, help='Truncation Threshold')

    args = parser.parse_args()
    finder = BlobFinder(args.tgtFname, args.refFname)
    blob = finder.findBlob(cutoff=args.cutoff, sigma=args.sigma)
    print blob
