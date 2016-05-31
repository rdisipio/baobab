# author: Riccardo Di Sipio <disipio@cern.ch>

from math import sqrt, pow, exp
import copy
import array

from ROOT import *

################################


def RemoveNegative( h ):
  Nbins = h.GetNbinsX()
  for i in range(Nbins):
    y = h.GetBinContent(i+1)
    if y < 0.: h.SetBinContent( i+1, 0. )


################################


def BMatching( event ):
   bjets = event['bjets']
   ljets = event['ljets']
   t1 = ljets[0]
   t2 = ljets[1]

   tb_match_n  = 0  
   dR_t1_b     = None
   dR_t2_b     = None 

   min_dR_1 = 1000.
   bj_index = -1
   for bj in bjets:
      dR = t1.DeltaR( bj )
      if dR > min_dR_1: continue
      min_dR_1 = dR
      bj_index = bj.index
   if min_dR_1 < 1.0:
      t1.has_bjet = bj_index
      tb_match_n += 1
   dR_t1_b = min_dR_1

   min_dR_2 = 1000.
   for bj in bjets:
      if bj.index == t1.has_bjet: continue #already matched
      dR = t2.DeltaR( bj )
      if dR > min_dR_2: continue
      min_dR_2 = dR
      bj_index = bj.index
   if min_dR_2 < 1.0:
      t2.has_bjet = bj_index
      tb_match_n += 1
   dR_t2_b = min_dR_2

   return tb_match_n, dR_t1_b, dR_t2_b


################################


def FinalObservables( t1, t2, tt ):
      y1 = t1.Rapidity()
      y2 = t2.Rapidity()
      pT1 = t1.Pt()
      pT2 = t2.Pt()

      observables = {}

      # baseline observables
      observables['mtt']  = tt.M()
      observables['pTtt'] = tt.Pt()
      observables['ytt']  = tt.Rapidity()

      observables['t1_pt'] = t1.Pt()
      observables['t1_y']  = t1.Rapidity()
      observables['t2_pt'] = t2.Pt()
      observables['t2_y']  = t2.Rapidity()

      # HT = pT1 + pT2
      HTtt = t1.Pt() + t2.Pt()
      observables['HTtt'] = HTtt

      # cosThetaStar
#      v_tt = tt.Vect()
      v_boost = -tt.BoostVector()
      t1_star = TLorentzVector( t1 )
      t1_star.Boost( 0., 0., v_boost.Z() )
#      t2_star = TLorentzVector( t2 )
#      t2_star.Boost( 0., 0., v_boost.Z() )
      cosThetaStar = t1_star.CosTheta()
      observables['cosThetaStar'] = cosThetaStar

      # y_boost
      observables['yboost'] = 0.5 * abs( y1 + y2 )

      # chi
      ystar = 0.5*(y1-y2) if ( pT1 > pT2 ) else 0.5*(y2-y1)
      observables['chi'] = exp( 2. * abs( ystar ) )

      # p_out
      v1 = t1.Vect()
      v2 = t2.Vect()
      zUnit = TVector3( 0., 0., 1. )
      vperp = zUnit.Cross( v1 )
      observables['pout'] = v2.Dot( vperp ) / vperp.Mag();

      # deltaPhi
      observables['dPhi'] = abs( t1.DeltaPhi( t2 ) )

      return observables


####################################################

def InterpolateEfficiency( x, xvalues, yvalues ):
  if x < xvalues[0]:  return yvalues[0]
  if x > xvalues[-1]: return yvalues[-1]
  i = 0
  while x > xvalues[i]: i += 1
  xlow = xvalues[i]
  xup  = xvalues[i+1]
  m = ( yvalues[i+1] - yvalues[i] ) / ( xup - xlow )
  b = yvalues[i] - m*xlow;  
  return m*x + b


####################################################

def GetMMEff( t_pt, t_y ):
  xbins_pt = xedges['t1_pt']
  xbins_y  = xedges['t1_y' ]
#   't1_pt' : array( 'd', [ 450, 550, 650, 750, 1200 ] ),
 
  # fakes come from data outside the top mass window and tau32 cut only.

  eff_real_pt = [ 0.660, 0.623, 0.593, 0.577, 0.878 ]
  eff_fake_pt = [ 0.287, 0.240, 0.274, 0.318, 0.368 ]
  eff_real_y  = [ 0.645, 0.636, 0.593, 0.570 ]
  eff_fake_y  = [ 0.284, 0.306, 0.222, 0.263 ]  

  r_pt = InterpolateEfficiency( t_pt/GeV, xbins_pt, eff_real_pt )
  f_pt = InterpolateEfficiency( t_pt/GeV, xbins_pt, eff_fake_pt )
  r_y  = InterpolateEfficiency( t_y,      xbins_y,  eff_real_y )
  f_y  = InterpolateEfficiency( t_y,      xbins_y,  eff_fake_y )

#  r = r_pt * r_y / sqrt( r_pt * r_y )
#  f = f_pt * f_y / sqrt( f_pt * f_y ) 
  r = sqrt( r_pt * r_y )
  f = sqrt( f_pt * f_y ) 

  return ( r, f )

#~~~~~~~~~~~~~~~~~~~~~~

def GetMMWeight( l1, r1, f1, l2, r2, f2 ):
   '''algebraic inversion of the efficiency matrix'''

   ntt = 1. if (not l1) and (not l2) else 0.
   ntl = 1. if (not l1) and l2       else 0.
   nlt = 1. if l1       and (not l2) else 0.
   nll = 1. if l1       and l2       else 0.
  
   if r1==f1: print "WARNING: r1 = f1 =", r1
   if r2==f2: print "WARNING: r2 = f2 =", r2

   a = 1. / ( (r1-f1) * (r2-f2) )

   nrf = a*r1*f2*(   -(1.-f1)*(1.-r2)*ntt    +    (1.-f1)*r2*ntl    +    f1*(1.-r2)*nlt    -    f1*r2*nll    )

   nfr = a*f1*r2*(   -(1.-r1)*(1.-f2)*ntt    +    (1.-r1)*f2*ntl    +    r1*(1.-f2)*nlt    -    r1*f2*nll    )
  
   nff = a*f1*f2*(   +(1.-r1)*(1.-r2)*ntt    -    (1.-r1)*r2*ntl    -    r1*(1.-r2)*nlt    +    r1*r2*nll    )

   if nrf != nrf: nrf = 0.
   if nfr != nfr: nfr = 0.
   if nff != nff: nff = 0.

   nrr = nrf + nfr + nff

   return nrr

#######################

def Interpolate( x, xvalues, yvalues ):
   if x < xvalues[0]:  return yvalues[0]
   if x > xvalues[-1]: return yvalues[-1]

   i = 0
   while xvalues[i+1] < x: i += 1
#   i = sum([ int(i<x) for i in xvalues ]) - 1
   xlow = xvalues[i]
   xup  = xvalues[i+1]
   a    = ( yvalues[i+1] - yvalues[i] ) / ( xup - xlow )
   b    = yvalues[i] - a*xlow
   return a*x + b
#   return yvalues[i] + ( yvalues[i+1] - yvalues[i] ) * ( x - xlow ) / ( xup - xlow )


#~~~~~~~~~~~~~~~~~~~~~~~
 

def TopSubstructureTagger( jet, wp="50", cut="full" ):
   pt_bins = array( 'd', [ 250000.000,325000.000,375000.000,425000.000,475000.000,525000.000,575000.000,625000.000,675000.000,725000.000,775000.000,850000.000,950000.000,1100000.000,1300000.000,1680000.000 ] )

   if wp == "50":
#     print "DEBUG: tight tagging"
     tau32_cuts = array( 'd', [ 0.773,0.713,0.672,0.637,0.610,0.591,0.579,0.574,0.573,0.574,0.576,0.578,0.580,0.580,0.577,0.571 ] )
     mass_cuts  = array( 'd', [ 85052.983,98705.422,107807.048,115186.721,120365.410,123510.000,125010.000,125662.377,126075.960,126389.113,126537.840,126803.137,127322.903,128379.386,130241.032,133778.159 ] )
   elif wp == "80":
#     print "DEBUG: loose tagging"
     tau32_cuts = array( 'd', [ 0.879,0.831,0.799,0.770,0.746,0.727,0.714,0.706,0.701,0.698,0.698,0.699,0.700,0.701,0.699,0.696 ] )
     mass_cuts  = array( 'd', [ 67888.967,72014.026,74764.066,76769.667,78354.344,79170.000,79530.000,80158.525,81195.851,82779.245,84890.965,88747.162,94262.629,102710.787,113868.253,135067.438 ] )
   else:
     print "ERROR: TopSubstructureTagger: unknown working point", wp

   jet_pt    = jet.Pt()
   jet_m     = jet.M()
   jet_tau32 = jet.tau32

   cut_m     = Interpolate( jet_pt, pt_bins, mass_cuts )
   cut_tau32 = Interpolate( jet_pt, pt_bins, tau32_cuts )
   pass_mass_cut  = jet_m > cut_m
   pass_tau32_cut = jet_tau32 < cut_tau32

#   print "DEBUG: wp=%s : pT=%4.1f m=%4.1f tau32=%4.3f : cut_m=%4.1f cut_tau32=%4.3f : pass_mass_cut=%i pass_tau32_cut=%i" % ( wp, jet_pt/GeV, jet_m/GeV, jet_tau32, cut_m/GeV, cut_tau32, pass_mass_cut, pass_tau32_cut )
#   return pass_tau32_cut
   if cut == "full":
     return ( pass_mass_cut and pass_tau32_cut )
   elif cut == "tau32":
     return pass_tau32_cut
   elif cut == "mass":
     return pass_mass_cut
   else:
     return None



##########################################

def GetBTaggingWeight( tree, syst, isWeightSystematic ):
   if not isWeightSystematic: 
     return tree.weight_bTagSF_77

   weights_btagging = {
        'nominal'                                 : tree.weight_bTagSF_77,
        'bTagSF_77_extrapolation_up'              : tree.weight_bTagSF_77_extrapolation_up,
        'bTagSF_77_extrapolation_down'            : tree.weight_bTagSF_77_extrapolation_down,
        'bTagSF_77_extrapolation_from_charm_up'   : tree.weight_bTagSF_77_extrapolation_from_charm_up,
        'bTagSF_77_extrapolation_from_charm_down' : tree.weight_bTagSF_77_extrapolation_from_charm_down,
   }
   for i in range( 6 ):
      weights_btagging['bTagSF_77_eigenvars_B_up_%i' % i]    = tree.weight_bTagSF_77_eigenvars_B_up[i]
      weights_btagging['bTagSF_77_eigenvars_B_down_%i' % i]  = tree.weight_bTagSF_77_eigenvars_B_down[i]
   for i in range( 4  ):
      weights_btagging['bTagSF_77_eigenvars_C_up_%i' % i]    = tree.weight_bTagSF_77_eigenvars_C_up[i]
      weights_btagging['bTagSF_77_eigenvars_C_down_%i' % i]  = tree.weight_bTagSF_77_eigenvars_C_down[i]
   for i in range( 14 ):
      weights_btagging['bTagSF_77_eigenvars_Light_up_%i' % i]    = tree.weight_bTagSF_77_eigenvars_Light_up[i]
      weights_btagging['bTagSF_77_eigenvars_Light_down_%i' % i]  = tree.weight_bTagSF_77_eigenvars_Light_down[i]

   return weights_btagging[syst]
