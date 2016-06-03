from ROOT import *
from baobab import *

def DetectorLevelAnalysis( event ):
   passed = True

   t1 = event['ljets'][0]
   t2 = event['ljets'][1]

   if t2.Pt() < 450*GeV: return not passed
   if t1.Pt() < 500*GeV: return not passed
 
   if abs( t1.M() - mtop ) > 50*GeV: return not passed
   if abs( t2.M() - mtop ) > 50*GeV: return not	passed

#   if not t1.topTag50: return not passed
#   if not t2.topTag50: return not passed

   return passed


###############################################


def ParticleLevelAnalysis( event ):
   passed = True

   t1 = event['ljets_truth'][0]
   t2 = event['ljets_truth'][1]

   if not t1.topTag50: return not passed
   if not t2.topTag50: return not passed

   if abs( t1.M() - mtop ) > 50*GeV: return not passed
   if abs( t2.M() - mtop ) > 50*GeV: return not passed

   return passed

