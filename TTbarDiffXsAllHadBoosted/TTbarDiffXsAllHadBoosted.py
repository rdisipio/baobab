# author: Riccardo Di Sipio <disipio@cern.ch>

from baobab import *

class TTbarDiffXsAllHadBoosted( AnalysisBase ):
   def __init__( self, name="TTbarDiffXsAllHadBoosted analysis", description="All-hadronic boosted ttbar cross-section sqrt(s) = 13 TeV" ):
      super( TTbarDiffXsAllHadBoosted, self ).__init__( name, description )

      self.__basedir = os.environ['PWD'] + "/TTbarDiffXsAllHadBoosted/"

   ######################################################


   def Initialize( self ):
      super(TTbarDiffXsAllHadBoosted,self).Initialize()
      print "INFO: initializing", self.name, self.description


   ######################################################


   def BookHistograms( self, rootfile ):
     rootfile.cd()

     HistogramManager.Book( self.__basedir + "histograms.xml" )

   ######################################################
 
   def Execute( self, event_raw ):
      w = 1.


   ######################################################


   def Finalize( self ):
     HistogramManager.Save()
     print "INFO: Finalized", self.name


def AnalysisFactory():
   return TTbarDiffXsAllHadBoosted()
