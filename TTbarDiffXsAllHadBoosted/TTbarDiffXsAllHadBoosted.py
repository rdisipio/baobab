# author: Riccardo Di Sipio <disipio@cern.ch>

from baobab import *
import Cutflow

class TTbarDiffXsAllHadBoosted( AnalysisBase ):
   def __init__( self, name="TTbarDiffXsAllHadBoosted analysis", description="All-hadronic boosted ttbar cross-section sqrt(s) = 13 TeV" ):
      super( TTbarDiffXsAllHadBoosted, self ).__init__( name, description )

      self.__basedir = os.environ['PWD'] + "/TTbarDiffXsAllHadBoosted/"
      self.fso = FinalStateObjectsSelectorBase()

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

      event = self.fso.MakeEvent( event_raw )
      event['eventNumber'] = event_raw['eventNumber']
      event['runNumber']   = event_raw['runNumber']

      jets_n  = len( event['jets'] )
      bjets_n = len( event['bjets'] )
      ljets_n = len( event['ljets'] )
#      print "INFO: event", event['eventNumber'], "jets =", jets_n, "bjets =", bjets_n, "ljets =", ljets_n

      passed_reco = Cutflow.DetectorLevelAnalysis( event )
      if not passed_reco:
         return 

      t1_reco = event['ljets'][0]
      t2_reco = event['ljets'][1]
      tt_reco = t1_reco + t2_reco
      event_variables_reco = PhysicsHelperFunctions.EventVariables( t1_reco, t2_reco, tt_reco )

      tb_match_n, dR_t1_b, dR_t2_b = PhysicsHelperFunctions.BMatching( event )  


   ######################################################


   def Finalize( self ):
     print "INFO: Finalized", self.name


def AnalysisFactory():
   return TTbarDiffXsAllHadBoosted()
