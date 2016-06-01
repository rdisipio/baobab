#!/usr/bin/env python

# author: Riccardo Di Sipio <disipio@cern.ch>

import os, sys
import importlib
import argparse
import xmltodict

from ROOT import *
import numpy
from root_numpy import *

from baobab import *

parser = argparse.ArgumentParser(description='ttbar all-hadronic analyzer')
parser.add_argument( '-i', '--input_filelist', help="Input file list", default="" )
parser.add_argument( '-n', '--nevents',        help="Maximum number of events", type=int, default=-1 )
parser.add_argument( '-o', '--output_filename', help="Output file name", default="output/test/histograms.root" )
parser.add_argument( '-c', '--config',         help="Configuration file", default="config/analysis_params/nominal.xml" )
#parser.add_argument( '-s', '--systematic', help='systematic uncertainty', default="nominal" )
#parser.add_argument( '-a', '--analysis',       help="Analysis to run", default="TestAnalysis" )
#parser.add_argument( '-t', '--truth', action="store_true", help='Run in truth mode' )
args = parser.parse_args()


if __name__ == "__main__":
  print """\033[92m \033[1m
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
\033[0m
"""

  xmlconfig = open( args.config )
  xmldoc    = xmltodict.parse( xmlconfig.read() )
  analysis_params = xmldoc['analysis']

  analysis_name = analysis_params['@name']
  analysis_plugin = None
  analysis_handle = None
  print "INFO: Loading analysis plugin for", analysis_name
  analysis_file   = "%s/%s.py" % ( analysis_name, analysis_name )
  analysis_plugin = importlib.import_module( analysis_name )
  analysis_handle = analysis_plugin.AnalysisFactory()
  analysis_handle.Initialize()
  print "INFO: loaded analysis:", analysis_handle.name
  print "INFO:", analysis_handle.description

  treename = analysis_params['tree']
  syst     = analysis_params['systematic']

  isWeightSystematic = True
  if not syst in weight_systematics:
    isWeightSystematic = False

  print "INFO: systematic:", syst
  print "INFO: tree name", treename

  doTruth = False
  #@TODO: decode from xml file...
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
  hm.CreateOutputFile( args.output_filename )
  histograms = analysis_handle.BookHistograms()

  # Main event loop
  if args.nevents > 0:
     nentries_reco = args.nevents
  print "INFO: Looping over", nentries_reco, "events"

  for ientry in range( nentries_reco ):
    event_raw = np_tree_reco[ientry]

    eventNumber = event_raw['eventNumber']
    runNumber   = event_raw['runNumber']

    # printout progress %
    if ( nentries_reco < 10 ) or ( (ientry+1) % int(float(nentries_reco)/10.)  == 0 ):
      perc = 100. * ientry / float(nentries_reco)
      print "INFO: Event %-9i (en = %-10i rn = %-10i )       (%3.0f %%)" % ( ientry, eventNumber, runNumber, perc )


    analysis_handle.Execute( event_raw )     

  # Finalize
  analysis_handle.Finalize()

  hm.Save()

  print "INFO: Finished. Created file", args.output_filename

