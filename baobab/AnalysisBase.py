# author: Riccardo Di Sipio <disipio@cern.ch>

import os, sys

class AnalysisBase(object):

   def __init__( self, name="Base analysis", description="Baseline analysis", runArgs=None, opts=None):
      self.name        = name
      self.description = description

      self.__basedir = os.environ['PWD']
      self.__n_cores = 1

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

   def Initialize( self ):
      pass

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

   def Finalize( self ):
      pass

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

   def Execute( self, event_raw ):
      print "WARNING: you should override the Execute function!"
  
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
