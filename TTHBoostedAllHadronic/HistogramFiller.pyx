from baobab.Defs import *
from baobab import HistogramManager as hm

def FillControlPlots(  event, path ):
      path += "control/"

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
      hm.Fill1D( path +	"jets_HT",    jets_HT/GeV, w )

      if jets_n >= 1: hm.Fill1D( path + "jets_j1_pt", event['jets'][0].Pt()/GeV, w )
      if jets_n	>= 2: hm.Fill1D( path + "jets_j2_pt", event['jets'][1].Pt()/GeV, w )
      if jets_n	>= 3: hm.Fill1D( path + "jets_j3_pt", event['jets'][2].Pt()/GeV, w )
      if jets_n	>= 4: hm.Fill1D( path + "jets_j4_pt", event['jets'][3].Pt()/GeV, w )


      bjets = event['bjets']
      bjets_n = len( bjets )
      hm.Fill1D( path + "bjets_n", bjets_n, w )
      for i in range( bjets_n ):
        pt  = bjets[i].Pt()
        eta = abs( bjets[i].Eta() )
        hm.Fill1D( path + "bjets_pt",  pt/GeV,  w )
        hm.Fill1D( path + "bjets_eta", eta, w )
      if bjets_n >= 1: hm.Fill1D( path + "bjets_j1_pt", event['bjets'][0].Pt()/GeV, w )
      if bjets_n >= 2:
         hm.Fill1D( path + "bjets_j1_pt", event['bjets'][1].Pt()/GeV, w )
         dR_bb = event['bjets'][0].DeltaR( event['bjets'][1] )
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
      hm.Fill1D( path + "ljets_j1_tau21", lj1.tau21,    w )
      hm.Fill1D( path + "ljets_j1_tau32", lj1.tau32,    w )
      hm.Fill1D( path + "ljets_j1_sd12",  lj1.sd12/GeV, w )
      lj2 = event['ljets'][1]
      hm.Fill1D( path + "ljets_j2_pt",    lj2.Pt()/GeV, w )
      hm.Fill1D( path + "ljets_j2_m",     lj2.M()/GeV,  w )
      hm.Fill1D( path + "ljets_j2_tau21", lj2.tau21,    w )
      hm.Fill1D( path + "ljets_j2_tau32", lj2.tau32,    w )
      hm.Fill1D( path + "ljets_j2_sd12",  lj2.sd12/GeV, w )
      lj3 = event['ljets'][2]
      hm.Fill1D( path + "ljets_j3_pt",    lj3.Pt()/GeV, w )
      hm.Fill1D( path + "ljets_j3_m",     lj3.M()/GeV,  w )
      hm.Fill1D( path + "ljets_j3_tau21", lj3.tau21,    w ) 
      hm.Fill1D( path + "ljets_j3_tau32", lj3.tau32,    w )
      hm.Fill1D( path + "ljets_j3_sd12",  lj3.sd12/GeV, w )

      hm.Fill1D( path + "ljets_HT",       ljets_HT/GeV, w )

      met_met = event['met_met']
      met_sig = met_met / jets_HT
      hm.Fill1D( path + "met_met", met_met/GeV,  w )
      hm.Fill1D( path + "met_sig", met_sig, w )


######################################################


def FillObservables( observables, w, path ):
      path += "observables/"

      hm.Fill1D( path + "H_m",      observables['H_m']/GeV,   w )
      hm.Fill1D( path + "H_pt",     observables['H_pt']/GeV,  w )
      hm.Fill1D( path + "H_absy",   abs(observables['H_y']),  w )

      hm.Fill1D( path + "t1_m",     observables['t1_m']/GeV,  w ) 
      hm.Fill1D( path + "t1_pt",    observables['t1_pt']/GeV,  w )
      hm.Fill1D( path + "t1_absy",  abs(observables['t1_y']),  w )
      hm.Fill1D( path + "t2_m",     observables['t2_m']/GeV,  w )
      hm.Fill1D( path + "t2_pt",    observables['t2_pt']/GeV,  w )
      hm.Fill1D( path + "t2_absy",  abs(observables['t2_y']),  w )

      hm.Fill1D( path + "tt_m",     observables['tt_m']/TeV,   w )
      hm.Fill1D( path + "tt_pt",    observables['tt_pt']/GeV,  w )
      hm.Fill1D( path + "tt_absy",  abs(observables['tt_y']),  w )

#      hm.Fill1D( path + "tt_pout",    observables['tt_pout']/GeV,  w )
#      hm.Fill1D( path + "tt_dPhi",    observables['tt_dPhi'],  w )
#      hm.Fill1D( path + "tt_yboost",  observables['tt_yboost'],  w )
#      hm.Fill1D( path + "tt_chi",     observables['tt_chi'],  w )
      hm.Fill1D( path + "tt_HT",      observables['tt_HT']/GeV,  w )
#      hm.Fill1D( path + "tt_cosThetaStar",  observables['tt_cosThetaStar'],  w )


######################################################

