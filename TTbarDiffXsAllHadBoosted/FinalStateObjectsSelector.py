from baobab import *

class FinalStateObjectsSelector(object):
   def __init__( self ):
      self.jet_pT_min   = 25.*GeV
      self.jet_eta_max  = 2.5
      self.ljets_pT_min = 300.*GeV  
      self.ljet_eta_max = 2.0
      self._event_raw = None

   ######################################### 

   def MakeJets( self ):
      if self._event_raw == None: return
 
      good_jets = []
      all_jets_n = len( self._event_raw['jet_pt'] )
      for i in range( all_jets_n ):
         if self._event_raw['jet_pt'][i] < self.jet_pT_min: continue
         if abs(self._event_raw['jet_eta'][i]) > self.jet_eta_max: continue
         good_jets += [ TLorentzVector() ]
         jet = good_jets[-1]
         jet.SetPtEtaPhiE( self._event_raw['jet_pt'][i], self._event_raw['jet_eta'][i], self._event_raw['jet_phi'][i], self._event_raw['jet_e'][i] )

      return good_jets

   ######################################### 

   def MakeEvent( self, event_raw ):
      event = {}
      event['jets'] = MakeJets()
