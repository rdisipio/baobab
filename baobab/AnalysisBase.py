# author: Riccardo Di Sipio <disipio@cern.ch>

import os, sys

class AnalysisBase(object):

   def __init__( self, runArgs=None, opts=None ):
      self.name        = "Base analysis"
      self.description = "Baseline analysis"

      self.__basedir = os.environ['PWD']
      self.__n_cores = 1


   def Initialize( self ):
      pass

   def Finalize( self ):
      pass

   def Execute( self ):
      pass
