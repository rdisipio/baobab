# author: Riccardo Di Sipio <disipio@cern.ch>

from baobab import *

import FinalStateObjectsSelector

class TTbarDiffXsAllHadBoosted( AnalysisBase ):
   def __init__( self, name="TTbarDiffXsAllHadBoosted analysis", description="All-hadronic boosted ttbar cross-section sqrt(s) = 13 TeV" ):
      super( TTbarDiffXsAllHadBoosted, self ).__init__( name, description )

      self.__basedir = os.environ['PWD'] + "/TTbarDiffXsAllHadBoosted/"

   ######################################################


   def Initialize( self ):
      super(TTbarDiffXsAllHadBoosted,self).Initialize()
      print "INFO: initializing", self.name, self.description


   ######################################################


   def BookHistograms( self ):
     HistogramManager.Book( self.__basedir + "histograms.xml" )


   ######################################################
 
   def Execute( self, event_raw ):
      w = 1.

      event = FinalStateObjectsSelector.MakeEvent( event_raw )


   ######################################################


   def Finalize( self ):
     print "INFO: Finalized", self.name


def AnalysisFactory():
   return TTbarDiffXsAllHadBoosted()
