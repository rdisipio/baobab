import xmltodict 
from array import array
import ROOT


_ofile = None
histograms = {}


#########################################


def CreateOutputFile( ofilename, foption="RECREATE" ):
  global _ofile
  _ofile = ROOT.TFile.Open( ofilename, foption )

  print "INFO: HistogramManager: opened output file", ofilename


#########################################


def CreatePath( hname ):
  dirs = hname.split('/')[:-1]

  for dir in dirs:
    if dir == "": continue

    nextDir = ROOT.gDirectory.GetDirectory( dir )
    if nextDir == None: 
       ROOT.gDirectory.mkdir( dir ) 

    ROOT.gDirectory.cd( dir )

  return ROOT.gDirectory


#########################################


def Book( xmlfilename ):
  global _ofile, histograms

  if _ofile == None:
    print "ERROR: output file not opened"
    raise Exception('Output file not opened')

  _ofile.cd()

  f = open( xmlfilename )
  doc = xmltodict.parse( f.read() )
  histos = doc['histograms']

  print "INFO: HistogramManager: booking histograms defined in file", xmlfilename

  for h1 in histos['TH1']:
    path  = h1['@path']
    title = h1['@title'] 
    if histograms.has_key(path):
       print "WARNING: histogram with path", path, "was already booked"

    currentDir = CreatePath( path )

    name = path.split('/')[-1]

    if h1.has_key('@xmin'):
       nbins = int( h1['@nbins'] )
       xmin = float( h1['@xmin'] )
       xmax = float( h1['@xmax'] )
       histograms[path] = ROOT.TH1D( name, title, nbins, xmin, xmax )
    if h1.has_key( '@xedges' ):
       xedges = array( 'd', [ float(x) for x in h1['@xedges'].split(",") ] )
       nbins = len(xedges) - 1
       histograms[path]	= ROOT.TH1D( name, title, nbins, xedges )

    _ofile.cd()


#########################################


def Save():
  _ofile.Write()
#  _ofile.cd()
#  for hname, h in histograms.iteritems(): h.Write()
  _ofile.Close()
