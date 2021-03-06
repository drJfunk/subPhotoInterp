

import astropy.io.fits as fits
from astropy.table import Table
import scipy.interpolate
import numpy
import copy
from IPython.display import display


class subPhotoInterp(object):

    def __init__(self,tableFile,silent=False):

        
        self._fitsFile = fits.open(tableFile)


        
        # Extract the evaluation energies
        self._ExtractEvalEnergies()
        
        # Extract the parameters
        self._ExtractParameters()
        
        # Extract the fluxes and reshape them
        # For the interpolator
        shape = self._numParamValues
        shape.append(self._numEvalEnergies)
        
        self._tableFluxes =  self._fitsFile[3].data['INTPSPEC'].reshape(*shape) / self._binWidths #convert!


        self._CreateInterpolation()

        if not silent:
            self.PrintParameters()


    def PrintParameters(self):

        
        info = numpy.array([self._fitsFile[1].data["NAME"],\
                                   self._fitsFile[1].data["MINIMUM"],\
                                   self._fitsFile[1].data["MAXIMUM"] ])
        tab = Table(info.T, names = ("Parameter","Min","Max"),dtype=["S25",float,float])
        display(tab)

    def _ExtractEvalEnergies(self):
    
        self._evalEnergies =  numpy.array(map(numpy.mean,self._fitsFile[2].data))
        self._binWidths = self._fitsFile[2].data["ENERG_HI"] - self._fitsFile[2].data["ENERG_LO"]
        
        self._numEvalEnergies = len(self._evalEnergies)
        
    def _ExtractParameters(self):
        
        self._numParamValues = (self._fitsFile[1].data["NUMBVALS"]).tolist()
        self._tableParams    = (self._fitsFile[1].data["VALUE"]).tolist()

        for i in range(len(self._numParamValues)):
            self._tableParams[i] = self._tableParams[i][:self._numParamValues[i]] 


    def _CreateInterpolation(self):

               # Create the interpolation grid
        # 
        tmp = copy.deepcopy(self._tableParams)
        
        tmp.append(self._evalEnergies.tolist())
        tmp = map(lambda x: numpy.array(x,dtype=numpy.float32),tmp)
        interpGrid = tuple(tmp)
        self._tableFluxes.dtype = numpy.float32
        zero = numpy.float32(0.)
        
        self._interpFunc = scipy.interpolate.RegularGridInterpolator(interpGrid,self._tableFluxes,method="linear",fill_value=zero,bounds_error=False)


    def __call__(self,energy,*args):

        args = list(args)
        args.append(energy) 
        args = tuple(args)


        return self._interpFunc(args)
