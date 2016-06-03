from Defs import *
from ROOT import *

class FinalStateObjectsSelectorBase(object):

   def __init__( self ):
      self.el_pT_min   = 25.*GeV
      self.el_eta_max  = 2.5

      self.mu_pT_min   = 25.*GeV
      self.mu_eta_max  = 2.5

      self.jet_pT_min   = 25.*GeV
      self.jet_eta_max  = 2.5

      self.bjet_weight_min = -0.4434

      self.ljet_pT_min = 300.*GeV  
      self.ljet_eta_max = 2.0

      self._event_raw = None
      self.event      = None


   ######################################### 


   def MakeEventMET( self ): 
      if self._event_raw == None: return

      self.event['met_met'] = self._event_raw['met_met']


   ######################################### 


   def MakeElectrons( self ):
      if self._event_raw == None: return

      self.event['electrons'] = []
      electrons_n = len( self._event_raw['el_pt'] )
      for i in range( electrons_n ):
         if self._event_raw['el_pt'][i] < self.el_pT_min: continue
         if abs(self._event_raw['el_eta'][i]) > self.el_eta_max: continue
         self.event['electrons'] += [ TLorentzVector() ]
         el = self.event['electrons'][-1]
         el.SetPtEtaPhiE( self._event_raw['el_pt'][i], self._event_raw['el_eta'][i], self._event_raw['el_phi'][i], self._event_raw['el_e'][i] )
         el.index = i

   ######################################### 


   def MakeMuons( self ):
      if self._event_raw == None: return
 
      self.event['muons'] = []
      muons_n = len( self._event_raw['mu_pt'] )
      for i in range( muons_n ):
         if self._event_raw['mu_pt'][i] < self.mu_pT_min: continue
         if abs(self._event_raw['mu_eta'][i]) > self.mu_eta_max: continue
         self.event['muons'] += [ TLorentzVector() ]
         mu = self.event['muons'][-1]
         mu.SetPtEtaPhiE( self._event_raw['mu_pt'][i], self._event_raw['mu_eta'][i], self._event_raw['mu_phi'][i], self._event_raw['mu_e'][i] )
         mu.index = i

   ######################################### 


   def MakeJets( self ):
      if self._event_raw == None: return
 
      self.event['jets'] = []
      self.event['bjets'] = []
      jets_n = len( self._event_raw['jet_pt'] )
      for i in range( jets_n ):

         if self._event_raw['jet_pt'][i] < self.jet_pT_min: continue
         if abs(self._event_raw['jet_eta'][i]) > self.jet_eta_max: continue

         self.event['jets'] += [ TLorentzVector() ]
         jet = self.event['jets'][-1]
         jet.SetPtEtaPhiE( self._event_raw['jet_pt'][i], self._event_raw['jet_eta'][i], self._event_raw['jet_phi'][i], self._event_raw['jet_e'][i] )
         jet.bjet_weight = self._event_raw['jet_mv2c20'][i]
         jet.index = i

         is_btagged = False
         if jet.bjet_weight > self.bjet_weight_min: is_btagged = True
         if not is_btagged: continue

         self.event['bjets'] += [ TLorentzVector() ]
         bjet = self.event['bjets'][-1]
         bjet.SetPtEtaPhiE( self._event_raw['jet_pt'][i], self._event_raw['jet_eta'][i], self._event_raw['jet_phi'][i], self._event_raw['jet_e'][i] )
         bjet.bjet_weight = self._event_raw['jet_mv2c20'][i]
         bjet.index = i


   ######################################### 


   def MakeLargeRJets( self ):
      if self._event_raw == None: return

      self.event['ljets'] = []
      ljets_n = len( self._event_raw['ljet_pt'] )
      for i in range( ljets_n ):

         if self._event_raw['ljet_pt'][i] < self.ljet_pT_min: continue
         if abs(self._event_raw['ljet_eta'][i]) > self.ljet_eta_max: continue

         self.event['ljets'] += [ TLorentzVector() ]
         ljet = self.event['ljets'][-1]
         ljet.SetPtEtaPhiE( self._event_raw['ljet_pt'][i], self._event_raw['ljet_eta'][i], self._event_raw['ljet_phi'][i], self._event_raw['ljet_e'][i] )
         ljet.sd12  = self._event_raw['ljet_sd12'][i]
         ljet.tau21 = self._event_raw['ljet_tau21'][i]
         ljet.tau32 = self._event_raw['ljet_tau32'][i]
         ljet.has_bjet = None
         ljet.index = i

         ljet.topTag80 = self._event_raw['ljet_topTag80'][i]
         ljet.topTag50 = self._event_raw['ljet_topTag50'][i]

#         ljet.topTag80 = HelperFunctions.TopSubstructureTagger( ljet, "80" )
#         ljet.topTag50 = HelperFunctions.TopSubstructureTagger( ljet, "50" )

   ######################################### 


   def MakeEvent( self, event_raw ):
     self._event_raw = event_raw

     self.event = {}
     self.MakeElectrons()
     self.MakeMuons()
     self.MakeJets()
     self.MakeLargeRJets()
     self.MakeEventMET()

     return self.event
