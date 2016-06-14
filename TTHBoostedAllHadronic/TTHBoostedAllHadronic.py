# author: Riccardo Di Sipio <disipio@cern.ch>

from baobab import *

import pyximport; pyximport.install()
import Cutflow
import HistogramFiller

class TTHBoostedAllHadronic( AnalysisBase ):
   def __init__( self, name="TTHBoostedAllHadronic analysis", description="All-hadronic boosted ttH sqrt(s) = 13 TeV" ):
      super( TTHBoostedAllHadronic, self ).__init__( name, description )

      self.__basedir = os.environ['PWD'] + "/"
      self.fso = FinalStateObjectsSelectorBase()

   ######################################################


   def Initialize( self ):
      super(TTHBoostedAllHadronic,self).Initialize()
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

      H_reco  = event['hjets'][0]
      t1_reco = event['tjets'][0]
      t2_reco = event['tjets'][1]
      tt_reco = t1_reco + t2_reco

      observables_reco = PhysicsHelperFunctions.FinalObservables( t1_reco, t2_reco, tt_reco )

      observables_reco['t1_m'] = t1_reco.M()
      observables_reco['t2_m'] = t2_reco.M()

      observables_reco['H_m']  = H_reco.M()
      observables_reco['H_pt'] = H_reco.Pt()
      observables_reco['H_y']  = H_reco.Rapidity()

      top_tags_n = 0
      if t1_reco.topTag50: top_tags_n += 1
      if t2_reco.topTag50: top_tags_n += 1

      tb_match_n, dR_t1_b, dR_t2_b = PhysicsHelperFunctions.BMatching( event['bjets'], event['tjets'] )  

      path = "reco/passed_%it%ib/" % ( top_tags_n, tb_match_n )

      HistogramFiller.FillControlPlots( event, path )
      HistogramFiller.FillObservables( observables_reco, w, path )


   ######################################################


   def Finalize( self ):
     print "INFO: Finalized", self.name


   ######################################################


def AnalysisFactory():
   return TTHBoostedAllHadronic()
