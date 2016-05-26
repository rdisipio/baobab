# author: Riccardo Di Sipio <disipio@cern.ch>

from math import sqrt, pow, exp
import copy
import array

################################

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

