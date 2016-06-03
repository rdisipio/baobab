# author: Riccardo Di Sipio <disipio@cern.ch>

from baobab import *

import pyximport; pyximport.install()
import Cutflow
import HistogramFiller

class TTbarDiffXsAllHadBoosted( AnalysisBase ):
   def __init__( self, name="TTbarDiffXsAllHadBoosted analysis", description="All-hadronic boosted ttbar cross-section sqrt(s) = 13 TeV" ):
      super( TTbarDiffXsAllHadBoosted, self ).__init__( name, description )

      self.__basedir = os.environ['PWD'] + "/"
      self.fso = FinalStateObjectsSelectorBase()

   ######################################################


   def Initialize( self ):
      super(TTbarDiffXsAllHadBoosted,self).Initialize()
      print "INFO: initializing", self.name, self.description


   ######################################################


   def BookHistograms( self, xmlfile="config/histograms.xml" ):
#     HistogramManager.Book( self.__basedir + "config/histograms.xml" )
     HistogramManager.Book( xmlfile )

   ######################################################
 
   def Execute( self, event_raw ):
      event = self.fso.MakeEvent( event_raw )
      event['eventNumber'] = event_raw['eventNumber']
      event['runNumber']   = event_raw['runNumber']
      event['mcChannelNumber'] = event_raw['mcChannelNumber']
 
      # Assign event weight
      w = 1.
      if not event['mcChannelNumber'] == 0:
         w = event_raw['weight_mc']
      event['weight'] = w

      passed_reco = Cutflow.DetectorLevelAnalysis( event )
      if not passed_reco:
         return 

      t1_reco = event['ljets'][0]
      t2_reco = event['ljets'][1]
      tt_reco = t1_reco + t2_reco
      observables_reco = PhysicsHelperFunctions.FinalObservables( t1_reco, t2_reco, tt_reco )

      top_tags_n = 0
      if t1_reco.topTag50: top_tags_n += 1
      if t1_reco.topTag50 and t2_reco.topTag50: top_tags_n += 1

      tb_match_n, dR_t1_b, dR_t2_b = PhysicsHelperFunctions.BMatching( event )  

      path = "reco/passed_%it%ib/" % ( top_tags_n, tb_match_n )

      HistogramFiller.FillControlPlots( event, path )
      HistogramFiller.FillObservables( observables_reco, w, path )


   ######################################################


   def Finalize( self ):
     print "INFO: Finalized", self.name


   ######################################################


def AnalysisFactory():
   return TTbarDiffXsAllHadBoosted()
