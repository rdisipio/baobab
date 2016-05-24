#!/usr/bin/env python

import os, sys
import argparse

from ROOT import *
from root_numpy import *

parser = argparse.ArgumentParser(description='ttbar all-hadronic analyzer')
parser.add_argument( '-i', '--input_filelist', help="Input file list", default="" )
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
