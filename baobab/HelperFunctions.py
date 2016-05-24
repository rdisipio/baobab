# author: Riccardo Di Sipio <disipio@cern.ch>

from math import sqrt, pow, exp
import copy
import array

################################


def RemoveNegative( h ):
  Nbins = h.GetNbinsX()
  for i in range(Nbins):
    y = h.GetBinContent(i+1)
    if y < 0.: h.SetBinContent( i+1, 0. )


################################


def EventVariables( t1, t2, ttbar ):
      y1 = t1.Rapidity()
      y2 = t2.Rapidity()
      pT1 = t1.Pt()
      pT2 = t2.Pt()

      event_variables = {}

      # baseline observables
      event_variables['mtt']  = ttbar.M()
      event_variables['pTtt'] = ttbar.Pt()
      event_variables['ytt']  = ttbar.Rapidity()

      event_variables['t1_pt'] = t1.Pt()
      event_variables['t1_y']  = t1.Rapidity()
      event_variables['t2_pt'] = t2.Pt()
      event_variables['t2_y']  = t2.Rapidity()

      # HT = pT1 + pT2
      HTtt = t1.Pt() + t2.Pt()
      event_variables['HTtt'] = HTtt

      # cosThetaStar
#      v_tt = ttbar.Vect()
      v_boost = -ttbar.BoostVector()
      t1_star = TLorentzVector( t1 )
      t1_star.Boost( 0., 0., v_boost.Z() )
#      t2_star = TLorentzVector( t2 )
#      t2_star.Boost( 0., 0., v_boost.Z() )
      cosThetaStar = t1_star.CosTheta()
      event_variables['cosThetaStar'] = cosThetaStar

      # y_boost
      event_variables['yboost'] = 0.5 * abs( y1 + y2 )

      # chi
      ystar = 0.5*(y1-y2) if ( pT1 > pT2 ) else 0.5*(y2-y1)
      event_variables['chi'] = exp( 2. * abs( ystar ) )

      # p_out
      v1 = t1.Vect()
      v2 = t2.Vect()
      zUnit = TVector3( 0., 0., 1. )
      vperp = zUnit.Cross( v1 )
      event_variables['pout'] = v2.Dot( vperp ) / vperp.Mag();

      # deltaPhi
      event_variables['dPhi'] = abs( t1.DeltaPhi( t2 ) )

      return event_variables


####################################################


def JoinEdges( v1, v2 ):
   x1 = copy.copy( xedges[v1] )
   x2 = copy.copy( xedges[v2] )
   offset = xedges[v1][-1]
   x2[:] = array( 'd', [ a+offset for a in x2 ] )
   joint_edges = x1 + x2

   return joint_edges

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def ConcatenateHistograms( v1, v2, lvl, phspace ):
   nbins1 = len(xedges[v1]) - 1
   nbins2 = len(xedges[v2]) - 1
   nbins = nbins1 + nbins2 
   # one edge is shared, e.g. [ 0, 1, 2 ] [0, 1, 2 ] -> [ 0, 1, 2, 1, 2 ]

   hname_1d  = "multispectra_%s_%s_%s_%s" % ( phspace, v1, v2, lvl )
   htitle_1d = "%s + %s (%s)" % ( v1, v2, lvl )   
   h_1d      = TH1F( hname_1d, htitle_1d, nbins, 0.5, nbins+0.5 )

   hname_2d  = "response_multispectra_%s_%s_%s_%s" % ( phspace, v1, v2, lvl )
   htitle_2d = "Response matrix %s / detector %s + %s (%s)" % ( phspace, v1, v2, lvl )
   h_2d      = TH2F( hname_2d, htitle_2d, nbins, 0.5, nbins+0.5, nbins, 0.5, nbins+0.5 )

   ibin_global = 1
   for ibin_local in range( nbins1 ):
      h_1d.GetXaxis().SetBinLabel( ibin_global, "%i" % ( ibin_local+1 ) )
      h_2d.GetXaxis().SetBinLabel( ibin_global, "%i" % ( ibin_local+1 ) )
      h_2d.GetYaxis().SetBinLabel( ibin_global, "%i" % ( ibin_local+1 ) )
      ibin_global += 1

   for ibin_local in range( nbins2 ):
      h_1d.GetXaxis().SetBinLabel( ibin_global, "%i" % ( ibin_local+1 ) )
      h_2d.GetXaxis().SetBinLabel( ibin_global, "%i" % ( ibin_local+1 ) )
      h_2d.GetYaxis().SetBinLabel( ibin_global, "%i" % ( ibin_local+1 ) )
      ibin_global += 1

   return h_1d, h_2d

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def BookHistograms( levels, partonlvlonly=False):

   histograms = {}

   histograms["global"] = {
     'corr_J_m_preselection'      : TH2F( "corr_J_m_preselection", "Correlations m_{J} (preselection)", 20, 0., 400., 20, 0., 400. ),
     'corr_J_m_2b'                : TH2F( "corr_J_m_2b",           "Correlations m_{J} (N_{b}#geq 2)", 20, 0., 400., 20, 0., 400. ),
     'yields_ABCD9'  : TH2F( "yields_ABCD9",  "Yields ABCD9",  3, -0.5, 2.5, 3, -0.5, 2.5 ),
     'yields_ABCD16' : TH2F( "yields_ABCD16", "Yields ABCD16", 4, 1.5, 4.5, 4, 1.5, 4.5 )
   }
   histograms["global"]['yields_ABCD9'].GetXaxis().SetBinLabel( 1, "0t" )
   histograms["global"]['yields_ABCD9'].GetXaxis().SetBinLabel( 2, "1t"	)
   histograms["global"]['yields_ABCD9'].GetXaxis().SetBinLabel( 3, "2t"	)
   histograms["global"]['yields_ABCD9'].GetYaxis().SetBinLabel( 1, "0b" )
   histograms["global"]['yields_ABCD9'].GetYaxis().SetBinLabel( 2, "1b" )
   histograms["global"]['yields_ABCD9'].GetYaxis().SetBinLabel( 3, "2b"	)

   histograms["global"]['yields_ABCD16'].GetXaxis().SetBinLabel( 1, "0t0b" )
   histograms["global"]['yields_ABCD16'].GetXaxis().SetBinLabel( 2, "0t1b" )
   histograms["global"]['yields_ABCD16'].GetXaxis().SetBinLabel( 3, "1t0b" )
   histograms["global"]['yields_ABCD16'].GetXaxis().SetBinLabel( 4, "1t1b" )
   histograms["global"]['yields_ABCD16'].GetYaxis().SetBinLabel( 1, "0t0b" )
   histograms["global"]['yields_ABCD16'].GetYaxis().SetBinLabel( 2, "0t1b" )
   histograms["global"]['yields_ABCD16'].GetYaxis().SetBinLabel( 3, "1t0b" )
   histograms["global"]['yields_ABCD16'].GetYaxis().SetBinLabel( 4, "1t1b" )


   for lvl in levels:
      histograms[lvl] = {
        #uniform binning
        "jets25_n"    : TH1F( "jets25_n_%s"    % lvl, xtitle["jets25_n"],   12, -0.5, 11.5 ),
        "jets25_eta"  : TH1F( "jets25_eta_%s"  % lvl, xtitle["jets25_eta"], 15, 0, 3.0 ),
        "bjets_n"     : TH1F( "bjets_n_%s"     % lvl, xtitle["bjets_n"],    5, -0.5, 4.5 ),
        "bjets_eta"   : TH1F( "bjets_eta_%s"   % lvl, xtitle["bjets_eta"], 15, 0, 3.0 ),
        "J_n"         : TH1F( "J_n_%s"         % lvl, xtitle["J_n"], 5, -0.4, 4.5 ),
        "J_eta"       : TH1F( "J_eta_%s"       % lvl, xtitle["J_eta"], 15, 0, 3.0 ),
        "met_pt"      : TH1F( "met_pt_%s"      % lvl, "E_{T}^{miss}", 10, 0., 150. ),
        "met_sig"     : TH1F( "met_sig_%s"     % lvl, xtitle["met_sig"], 10, 0., 100. ),
        "mu"          : TH1F( "mu_%s"          % lvl, xtitle["mu"], 20, 0., 40 ),
        "J1_m"        : TH1F( "J1_m_%s"        % lvl, "m_{J1}", 6, 120., 240. ),
        "J1_pt"       : TH1F( "J1_pt_%s"       % lvl, "p_{T,J1}", 40, 0., 1200. ),
        "J1_sd12"     : TH1F( "J1_sd12_%s"     % lvl, "#sqrt{d_{12}}", 15, 0, 300 ),
        "J1_tau21"    : TH1F( "J1_tau21_%s"    % lvl, "#tau_{21}", 12, 0, 1.2 ),
        "J1_tau32"    : TH1F( "J1_tau32_%s"    % lvl, "#tau_{32}", 12, 0, 1.2 ),
        "J2_m"        : TH1F( "J2_m_%s"        % lvl, "m_{J2}", 6, 120., 240. ),
        "J2_pt"       : TH1F( "J2_pt_%s"       % lvl, "p_{T,J2}", 40, 0., 1200. ),
        "J2_sd12"     : TH1F( "J2_sd12_%s"     % lvl, "#sqrt{d_{12}}", 15, 0, 300 ),
        "J2_tau21"    : TH1F( "J2_tau21_%s"    % lvl, "#tau_{21}", 12, 0, 1.2 ),
        "J2_tau32"    : TH1F( "J2_tau32_%s"    % lvl, "#tau_{32}", 12, 0, 1.2 ),
        "min_dR_t1_b" : TH1F( "min_dR_t1_b_%s" % lvl, xtitle["min_dR_t1_b"], 10, 0., 1. ),
        "min_dR_t2_b" : TH1F( "min_dR_t2_b_%s" % lvl, xtitle["min_dR_t2_b"], 10, 0., 1. ),
        "dR_bb"       : TH1F( "dR_bb_%s"       % lvl, xtitle["dR_bb"], 5, 0., 5. ),
        "dPhi_met_tt" : TH1F( "dPhi_met_tt_%s" % lvl, xtitle["dPhi_met_tt"], 8, 0., 2*3.14 ),
        "min_dPhi_met_t" : TH1F( "min_dPhi_met_t_%s" % lvl, xtitle["min_dPhi_met_t"], 8, 0., 3.14 ),
        "dY_J1J2"     : TH1F( "dY_J1J2_%s"     % lvl, xtitle["dY_J1J2"], 6, 0., 3. ),
        "mtt_fine"    : TH1F( "mtt_fine_%s"    % lvl, "%s (%s)" % (pretty_names["mtt"],lvl), 40, 1., 3. )
      }

      if partonlvlonly:
            histograms[lvl].update({"pt_vs_mtt" : TH2F( "pt_vs_mtt_%s" % lvl, "pt_vs_mtt", 5, 0., 2.5, 12, 0., 1200)})
                 
      # optimized binning
      for obs in xedges.keys():
         histograms[lvl][obs] = TH1F( "%s_%s" % ( obs, lvl ), "%s (%s)" % (pretty_names[obs],lvl), len(xedges[obs])-1, xedges[obs] )

      # correlations
      histograms[lvl]["corr_J_m"] = TH2F( "corr_J_m_%s" % lvl, "Correlations m_{J} (%s)" % lvl, 20, 0., 400., 20, 0., 400. )

      # detector/truth migrations, optimized binning
      for obs in final_observables:
        for phspace in [ "parton", "particle" ]:
           hname = "response_singlespectrum_%s_%s_%s" % ( phspace, obs, lvl )
           histograms[lvl][hname] = TH2F( hname, "Response matrix %s / detector (%s)" % ( phspace, lvl ), len(xedges[obs])-1, xedges[obs], len(xedges[obs])-1, xedges[obs] )
           histograms[lvl][hname].GetXaxis().SetTitle( "Detector level %s" % pretty_names[obs] )
           histograms[lvl][hname].GetYaxis().SetTitle( "%s level %s"   % ( phspace, pretty_names[obs] ) )

      # detector/truth migrations, multi-observables matrices
      for phspace in [ "parton", "particle" ]:
         histograms[lvl]["multispectra_%s_t1_pt_t2_pt_%s" % (phspace,lvl)], histograms[lvl]["response_multispectra_%s_t1_pt_t2_pt_%s" % (phspace,lvl)] = ConcatenateHistograms( "t1_pt", "t2_pt", lvl, phspace )
         histograms[lvl]["multispectra_%s_t1_y_t2_y_%s"   % (phspace,lvl)], histograms[lvl]["response_multispectra_%s_t1_y_t2_y_%s" % (phspace,lvl)]   = ConcatenateHistograms( "t1_y", "t2_y", lvl, phspace )

      for obs in observables:
        try:
           histograms[lvl][obs].Sumw2()
        except: pass

   return histograms


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def BookCutflowHistograms( histograms, levels, cuts = [] ):

   print "INFO: cuts:", cuts
   ncuts = len( cuts )

   for lvl in levels:
      if not histograms.has_key(lvl): 
         print "ERROR: level", lvl, "is not defined in histogram dictionary"
         continue

      histograms[lvl]['cutflow_unweight'] = TH1F( "cutflow_%s_unweight" % lvl, "Cut flow %s (unweight)" % lvl, ncuts, -0.5, ncuts-0.5 ) 
      histograms[lvl]['cutflow_weighted'] = TH1F( "cutflow_%s_weighted" % lvl, "Cut flow %s (weighted)" % lvl, ncuts, -0.5, ncuts-0.5 )

      for icut in range(ncuts):
        histograms[lvl]['cutflow_unweight'].GetXaxis().SetBinLabel( icut+1, cuts[icut] )
        histograms[lvl]['cutflow_weighted'].GetXaxis().SetBinLabel( icut+1, cuts[icut] )


def PassedCut( histograms, levels, lastCut, w ):
#   if not hasattr( PassedCut, "lastCut"): PassedCut.lastCut = 0

   for lvl in levels:
     histograms[lvl]['cutflow_unweight'].Fill( lastCut, 1. )
     histograms[lvl]['cutflow_weighted'].Fill( lastCut, w )

   return lastCut + 1 

#######################

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


def FillMultispectra( histograms, value, rank, hname_single, hname_conc, phspace, lvl, w, overflow='ignore' ):
   hname    = "multispectra_%s_%s_%s" % ( phspace, hname_conc, lvl )
   h        = histograms[lvl][hname]
   nbins    = h.GetNbinsX()

   h_1d     = histograms[lvl][hname_single]
   nbins_1d = h_1d.GetNbinsX()

   offset   = ( rank - 1 ) * nbins_1d

   bin_1d = min( [ nbins_1d, h_1d.FindBin( value ) ] )
   bin_2d = offset + bin_1d 

   h.Fill( bin_2d, w )

#   print "DEBUG: FillMultispectra():", hname, value, rank, bin_1d, offset, bin_2d

#~~~~~~~~~~~~~~~~~~~~~~~~~~~

def FillResponseMultispectra( histograms, match, phspace, lvl, w ):
   v1       = match[0][0]
   x1_reco  = match[0][1]
   x1_truth = match[0][2]
   rank1_reco  = match[0][3]
   rank1_truth = match[0][4]

   v2       = match[1][0]
   x2_reco  = match[1][1]
   x2_truth = match[1][2]
   rank2_reco  = match[1][3]
   rank2_truth = match[1][4]
   
   hname_2d = "response_multispectra_%s_%s_%s_%s" % ( phspace, v1, v2, lvl )
   h_2d = histograms[lvl][hname_2d]

   nbins = histograms[lvl][v1].GetNbinsX() # assume equal number of bins!

   offset1_reco  = ( rank1_reco  - 1 ) * nbins
   offset2_reco  = ( rank2_reco  - 1 ) * nbins
   offset1_truth = ( rank1_truth - 1 ) * nbins
   offset2_truth = ( rank2_truth - 1 ) * nbins

   # NB: we don't fill x values, but bin indices (avoid troubles with non-uniform binning)
   b1_reco  = offset1_reco  + min( [ histograms[lvl][v1].FindBin( x1_reco ), nbins ] )
   b1_truth = offset1_truth + min( [ histograms[lvl][v1].FindBin( x1_truth ), nbins ] )
   b2_reco  = offset2_reco  + min( [ histograms[lvl][v2].FindBin( x2_reco ), nbins ] )
   b2_truth = offset2_truth + min( [histograms[lvl][v2].FindBin( x2_truth ), nbins ] )

   h_2d.Fill( b1_reco, b1_truth, w )
   h_2d.Fill( b2_reco, b2_truth, w )


####################################

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
