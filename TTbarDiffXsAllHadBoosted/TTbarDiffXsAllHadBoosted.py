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
      event['weight']      = event_raw['weight_mc']

      jets_n  = len( event['jets'] )
      bjets_n = len( event['bjets'] )
      ljets_n = len( event['ljets'] )

      passed_reco = Cutflow.DetectorLevelAnalysis( event )
      if not passed_reco:
         return 

      t1_reco = event['ljets'][0]
      t2_reco = event['ljets'][1]
      tt_reco = t1_reco + t2_reco
      observables_reco = PhysicsHelperFunctions.FinalObservables( t1_reco, t2_reco, tt_reco )

      tb_match_n, dR_t1_b, dR_t2_b = PhysicsHelperFunctions.BMatching( event )  

      top_tags_n = 0
      if t1_reco.topTag50: top_tags_n += 1
      if t2_reco.topTag50: top_tags_n += 1

      path = "reco/passed_%it%ib/" % ( top_tags_n, tb_match_n )

      self.FillControlPlots( event, path )
      self.FillObservables( observables_reco, path )


   ######################################################


   def Finalize( self ):
     print "INFO: Finalized", self.name


   ######################################################


   def FillControlPlots( self, event, path ):
      path += "control/"
#      hm.cd( path )

      w = event['weight']

      jets = event['jets']
      jets_n = len( jets )      
      hm.Fill1D( path + "jets_n", jets_n, w )
      for i in range( jets_n ):
        pt  = jets[i].Pt() / GeV
        eta = abs( jets[i].Eta() )
        hm.Fill1D( path + "jets_pt",  pt,  w )
        hm.Fill1D( path + "jets_eta", eta, w )
      j1 = event['jets'][0]
      hm.Fill1D( path + "jets_j1_pt", j1.Pt()/GeV, w )

      bjets = event['bjets']
      bjets_n = len( bjets )
      hm.Fill1D( path + "bjets_n", bjets_n, w )
      for i in range( bjets_n ):
        pt  = bjets[i].Pt() / GeV
        eta = abs( bjets[i].Eta() )
        hm.Fill1D( path + "bjets_pt",  pt,  w )
        hm.Fill1D( path + "bjets_eta", eta, w )
      if bjets_n >= 1:
        bj1 = event['bjets'][0]
        hm.Fill1D( path + "bjets_j1_pt", bj1.Pt()/GeV, w )
      if bjets_n >= 2:
        bj2 = event['bjets'][1] 
        hm.Fill1D( path + "bjets_j2_pt", bj2.Pt()/GeV, w )

      ljets = event['ljets']
      ljet_n = len( ljets )
      hm.Fill1D( path + "ljets_n", ljet_n, w )
      for i in range( ljet_n ):
        pt  = ljets[i].Pt() / GeV
        eta = abs( ljets[i].Eta() )
        hm.Fill1D( path + "ljets_pt",  pt,  w )
        hm.Fill1D( path + "ljets_eta", eta, w )
      lj1 = event['ljets'][0] 
      hm.Fill1D( path + "ljets_j1_pt",    lj1.Pt()/GeV, w )
      hm.Fill1D( path + "ljets_j1_m",     lj1.M()/GeV,  w )
      hm.Fill1D( path + "ljets_j1_tau32", lj1.tau32,    w )
      hm.Fill1D( path + "ljets_j1_sd12",  lj1.sd12/GeV, w )
      lj2 = event['ljets'][1]
      hm.Fill1D( path + "ljets_j2_pt",    lj2.Pt()/GeV, w )
      hm.Fill1D( path + "ljets_j2_m",     lj2.M()/GeV,  w )
      hm.Fill1D( path + "ljets_j2_tau32", lj2.tau32,    w )
      hm.Fill1D( path + "ljets_j2_sd12",  lj2.sd12/GeV, w )


   ######################################################


   def FillObservables( self, observables_reco, path ):
      pass


def AnalysisFactory():
   return TTbarDiffXsAllHadBoosted()
