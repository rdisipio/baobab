import xmltodict 
from array import array
import ROOT

histograms = {}

def Book( filename ):

  f = open( filename )
  doc = xmltodict.parse( f.read() )
  histos = doc['histograms']

  print "INFO: HistogramManager"

  for h1 in histos['TH1']:
    name  = h1['@name']
    title = h1['@title'] 
    if h1.has_key('@xmin'):
       nbins = int( h1['@nbins'] )
       xmin = float( h1['@xmin'] )
       xmax = float( h1['@xmax'] )
       histograms[name] = ROOT.TH1D( name, title, nbins, xmin, xmax )
    if h1.has_key( '@xedges' ):
       xedges = array( 'd', [ float(x) for x in h1['@xedges'].split(",") ] )
       nbins = len(xedges) - 1
       histograms[name]	= ROOT.TH1D( name, title, nbins, xedges )

  return histograms

#########################################

def Save():
  for hname, h in histograms.iteritems(): h.Write()
