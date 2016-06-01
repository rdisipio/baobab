# author: Riccardo Di Sipio <disipio@cern.ch>

from baobab import *
import Cutflow

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

      self.FillControlPlots( event, path )
      self.FillObservables( observables_reco, w, path )


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
      jets_HT = 0.
      for i in range( jets_n ):
        pt  = jets[i].Pt()
        eta = abs( jets[i].Eta() )
        hm.Fill1D( path + "jets_pt",  pt/GeV,  w )
        hm.Fill1D( path + "jets_eta", eta, w )
        jets_HT += pt
      j1 = event['jets'][0]
      hm.Fill1D( path + "jets_j1_pt", j1.Pt()/GeV, w )
      hm.Fill1D( path +	"jets_HT",    jets_HT/GeV, w )

      bjets = event['bjets']
      bjets_n = len( bjets )
      hm.Fill1D( path + "bjets_n", bjets_n, w )
      for i in range( bjets_n ):
        pt  = bjets[i].Pt()
        eta = abs( bjets[i].Eta() )
        hm.Fill1D( path + "bjets_pt",  pt/GeV,  w )
        hm.Fill1D( path + "bjets_eta", eta, w )
      if bjets_n >= 1:
        bj1 = event['bjets'][0]
        hm.Fill1D( path + "bjets_j1_pt", bj1.Pt()/GeV, w )
      if bjets_n >= 2:
        bj2 = event['bjets'][1] 
        hm.Fill1D( path + "bjets_j2_pt", bj2.Pt()/GeV, w )

        dR_bb = bj1.DeltaR( bj2 )
        hm.Fill1D( path + "dR_bb", dR_bb, w )

      ljets = event['ljets']
      ljet_n = len( ljets )
      ljets_HT = 0.
      hm.Fill1D( path + "ljets_n", ljet_n, w )
      for i in range( ljet_n ):
        pt  = ljets[i].Pt()
        eta = abs( ljets[i].Eta() )
        ljets_HT += pt
        hm.Fill1D( path + "ljets_pt",  pt/GeV,  w )
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
      hm.Fill1D( path + "ljets_HT",       ljets_HT/GeV, w )

      met_met = event['met_met']
      met_sig = met_met / jets_HT
      hm.Fill1D( path + "met_met", met_met/GeV,  w )
      hm.Fill1D( path + "met_sig", met_sig, w )


   ######################################################


   def FillObservables( self, observables, w, path ):
      path += "observables/"
 
      hm.Fill1D( path + "t1_pt",    observables['t1_pt']/GeV, w )
      hm.Fill1D( path + "t1_absy",  abs(observables['t1_y']),   w )
      hm.Fill1D( path + "t2_pt",    observables['t2_pt']/GeV, w )
      hm.Fill1D( path + "t2_absy",  abs(observables['t2_y']),   w )

      hm.Fill1D( path + "tt_m",     observables['tt_m']/TeV,  w )
      hm.Fill1D( path + "tt_pt",    observables['tt_pt']/GeV, w )
      hm.Fill1D( path + "tt_absy",  abs(observables['tt_y']),   w )

      hm.Fill1D( path + "tt_pout",    observables['tt_pout']/GeV,  w )
      hm.Fill1D( path + "tt_dPhi",    observables['tt_dPhi'],  w )
      hm.Fill1D( path + "tt_yboost",  observables['tt_yboost'],  w )
      hm.Fill1D( path + "tt_chi",     observables['tt_chi'],  w )
      hm.Fill1D( path + "tt_HT",      observables['tt_HT']/GeV,  w )
      hm.Fill1D( path + "tt_cosThetaStar",  observables['tt_cosThetaStar'],  w )


   ######################################################


def AnalysisFactory():
   return TTbarDiffXsAllHadBoosted()
