import numpy as np
from scipy.interpolate import bisplrep, bisplev
from glob import glob
from blobFinder import BlobFinder

class Calibrate:
    def __init__(self, fname, grid_size):
        """
        fname: Filepath to directory with calibration pictures
        
        The pictures names need to follow the convention:
        cal*.jpg, where * is an int starting from 0. Each picture increments
        the location of the object on the x-axis by one unit until grid_size, where
        the y-axis is increased and the x-axis resets.

        i.e. for grid_size 3 and 6 pictures
        cal0: 0,0
        cal1: 1,0
        cal2: 2,0
        cal3: 0,1
        cal4: 1,1
        cal5: 2,1

        There must also be an image called bg.jpg, which is the background image that will
        be used throughout.
        """
        imageFnames = glob(fname+'/cal*.jpg')
        tableCoords = []
        blobs = []
        for imgName in imageFnames:
            start = imgName.rfind('cal')
            number = int(imgName[start+3:-4])
            tableCoords.append((number%grid_size,number//grid_size))

            blob = BlobFinder(imgName,fname+'/bg.jpg').findBlob()
            blobs.append(blob)

        chart = Chart(tableCoords, blobs)

        return chart

class Chart:
    def __init__(self, tableCoords, blobs):
        """
        tableCoords: List of 2-tuples of x,y coordinates
        blobs: Matching list of initialized blob objects
        """
        tableXs = np.array([_[0] for _ in tableCoords])
        tableYs = np.array([_[1] for _ in tableCoords])

        blobXs = np.array([_.getLocation()[0] for _ in blobs])
        blobYs = np.array([_.getLocation()[1] for _ in blobs])

        self.tableToBlobTckX = bisplrep(tableXs,tableYs,blobXs)
        self.tableToBlobTckY = bisplrep(tableXs,tableYs,blobYs)

        self.blobToTableTckX = bisplrep(blobXs,blobYs,tableXs)
        self.blobToTableTckY = bisplrep(blobXs,blobYs,tableYs)

    def blobToTable(self, x, y):
        tableX = bisplev(x, y, self.blobToTableTckX)
        tableY = bisplev(x, y, self.blobToTableTckY)
        return tableX, tableY

    def tableToBlob(self, x, y):
        blobX = bisplev(x, y, self.tableToBlobTckX)
        blobY = bisplev(x, y, self.tableToBlobTckY)
        return blobX, blobY