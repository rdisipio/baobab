from ROOT import *
from baobab import *

def DetectorLevelAnalysis( event ):
   passed = True

   if len( event['ljets'] ) < 3: return not passed

   J1 = event['ljets'][0]
   J2 = event['ljets'][1]
   J3 = event['ljets'][2]

   # Lorentz Boost: dR ~ 2*m / pT
   # Higgs-candidate pT > 250 GeV 
   # Top candidates  pT > 350 GeV

   if J3.Pt() < 250*GeV: return not passed

   event['tjets'] = [ ]
   event['hjets'] = [ ]

   for ljet in event['ljets']:
     if ljet.Pt() > 350*GeV and ljet.topTag50 and abs(ljet.M()-mtop) < 50*GeV:
        event['tjets'] += [ ljet ]
        continue
     if ljet.Pt() > 250*GeV and abs(ljet.M()-mH)<30*GeV:
        event['hjets'] += [ ljet ]
        continue

   if len( event['tjets'] ) < 2: return not passed
   if len( event['hjets'] ) < 1: return not passed

   return passed


###############################################
