#!/usr/bin/env python

# author: Riccardo Di Sipio <disipio@cern.ch>

import os, sys, imp
import argparse

from ROOT import *
import numpy
from root_numpy import *

from baobab import *

parser = argparse.ArgumentParser(description='ttbar all-hadronic analyzer')
parser.add_argument( '-i', '--input_filelist', help="Input file list", default="" )
parser.add_argument( '-a', '--analysis',       help="Analysis to run", default="TestAnalysis" )
parser.add_argument( '-n', '--nevents',        help="Maximum number of events", type=int, default=-1 )
parser.add_argument( '-o', '--output_filename', help="Output file name", default="output.histograms.root" )
parser.add_argument( '-s', '--systematic', help='systematic uncertainty', default="nominal" )
parser.add_argument( '-t', '--truth', action="store_true", help='Run in truth mode' )
args = parser.parse_args()


if __name__ == "__main__":
  print """
              v .   ._, |_  .,
           `-._\/  .  \ /    |/_
               \\  _\, y | \//
         _\_.___\\, \\/ -.\||
           `7-,--.`._||  / / ,
           /'     `-. `./ / |/_.'
                     |    |//
                     |_    /
                     |-   |
                     |   =|
                     |    |
--------------------/ ,  . \--------._
INFO: Running Baobab
"""

  analysis_plugin = None
  analysis_handle = None
  analysis_file   = "%s/%s.py" % ( args.analysis, args.analysis )
  try:
    analysis_plugin = imp.load_source( args.analysis, analysis_file )
  except:
    print "ERROR: unable to load analysis", args.analysis
    exit(1)
  analysis_handle = analysis_plugin.AnalysisFactory()
  analysis_handle.Initialize()
  print "INFO: loaded analysis:", analysis_handle.name
  print "INFO:", analysis_handle.description

  treename = "nominal"
  syst = args.systematic
  isWeightSystematic = True
  if not syst in weight_systematics:
    treename   = syst
    isWeightSystematic = False

  print "INFO: systematic:", syst
  print "INFO: tree name", treename

  doTruth = args.truth
  if doTruth:
    print "INFO: Truth analysis requested. Response matrices will be filled." 

  # Create ROOT trees
  root_tree_reco     = TChain( treename, treename )
  root_tree_parton   = None
  root_tree_particle = None
  if doTruth:
    root_tree_parton   = TChain( "truth", "truth" )
    root_tree_particle = TChain( "particleLevel", "Particle Level" )

  # open root files and get trees
  filelistname = args.input_filelist

  for fname in open( filelistname, 'r' ).readlines():
    fname = fname.strip()
    root_tree_reco.Add( fname )
    if doTruth: 
      root_tree_parton.Add( fname )
      root_tree_particle.Add( fname )

  np_tree_reco = tree2array( root_tree_reco )#.view(numpy.recarray)
  nentries_reco = len( np_tree_reco )
  print "INFO: entries found:", nentries_reco

  np_tree_parton   = None
  np_tree_particle = None
  if doTruth:
     np_tree_parton   = tree2array( root_tree_parton )#.view(numpy.recarray)
     np_tree_particle = tree2array( root_tree_particle )#.view(numpy.recarray)

  # Open output file
  ofile = TFile.Open( args.output_filename, "RECREATE" )

  # Main event loop
  if args.nevents > 0:
     nentries_reco = args.nevents
  print "INFO: Looping over", nentries_reco, "events"

  for ientry in range( nentries_reco ):
    event_raw = np_tree_reco[ientry] #.view(numpy.recarray)

    eventNumber = np_tree_reco['eventNumber'][0]
    runNumber   = np_tree_reco['runNumber'][0]

    # printout minimal stat - I'm alive
    if ( nentries_reco < 10 ) or ( (ientry+1) % int(float(nentries_reco)/10.)  == 0 ):
      perc = 100. * ientry / float(nentries_reco)
      print "INFO: Event %-9i (en = %-10i rn = %-10i )       (%3.0f %%)" % ( ientry, eventNumber, runNumber, perc )

    analysis_handle.Execute( event_raw )     

  # Finalize
  analysis_handle.Finalize()

  ofile.cd()
  ofile.Write()
  ofile.Close()

  print "INFO: Finished. Created file", args.output_filename

