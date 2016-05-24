# author: Riccardo Di Sipio <disipio@cern.ch>

from baobab import *

class TestAnalysis( AnalysisBase ):
   def __init__( self, runArgs=None, opts=None ):
      super( TestAnalysis, self).__init__( runArgs, opts )
      self.name        = "Test analysis"
      self.description = "A test analysis"

   def Initialize( self ):
      super(TestAnalysis,self).Initialize()
      print "INFO: initializing", self.name, ":", self.description

   def Execute( self ):
      pass

   def Finalize( self ):
      print "INFO: Finalized", self.name


def AnalysisFactory( runArgs=None, opts=None ):
   return TestAnalysis( runArgs, opts )
