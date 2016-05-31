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

  print "INFO: HistogramManager: booking histograms defined in file", xmlfilename

  f = open( xmlfilename )
  xmldoc = xmltodict.parse( f.read() )
  doc = xmldoc['document']

  # interpret folders structure
  xmlfolders = doc['folders']
  folders = {}
  for folder in xmlfolders['folder']:
    fname = folder['@name']
    fpath = folder['#text']
    folders[fname] = fpath
 
  xmlhistos  = doc['histograms']
  for xmlset in xmlhistos['set']:
    sname    = xmlset['@name']
    sfolders = xmlset['@folders'].split(',')

    for h1 in xmlset['TH1']:
      hname  = h1['@name']
      htitle = h1['@title']

      for sfolder in sfolders:
        hpath = folders[sfolder] + "/" + sname + "/" + hname 

        if histograms.has_key(hpath):
          print "WARNING: histogram with path", hpath, "was already booked"

        _ofile.cd()
        currentDir = CreatePath( hpath )

        if h1.has_key('@xmin'):
          nbins = int( h1['@nbins'] )
          xmin = float( h1['@xmin'] )
          xmax = float( h1['@xmax'] )
          histograms[hpath] = ROOT.TH1D( hname, htitle, nbins, xmin, xmax )
        if h1.has_key( '@xedges' ):
          xedges = array( 'd', [ float(x) for x in h1['@xedges'].split(",") ] )
          nbins = len(xedges) - 1
          histograms[hpath] = ROOT.TH1D( hname, htitle, nbins, xedges )


#########################################


def Save():
  for hpath, h in histograms.iteritems():
     print "INFO:", hpath, " entries =", h.GetEntries()
#     h.Write()

  _ofile.cd()
  _ofile.Write()
#  _ofile.cd()
#  for hname, h in histograms.iteritems(): h.Write()
  _ofile.Close()

#########################################

def cd( path ):
  _ofile.cd()
  _ofile.cd( path )

def Get( hname ):
   return ROOT.gDirectory.Get( hname )

def Fill1D( hpath, y, w=1. ):
   h = histograms[hpath]
   h.Fill( y, w )

def Fill2D( hpath, x, y, w=1. ):
   h = histograms[hpath]
   h.Fill( x, y, w )
