#!/usr/bin/env python

import glob, os, sys
from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize
from root_setup_utils import *

rootsys = os.getenv('ROOTSYS', None)
if rootsys is not None:
    try:
        root_config = os.path.join(rootsys, 'bin', 'root-config')
        root_version = root_version_installed(root_config)
        root_cflags, root_ldflags = root_flags(root_config)
    except OSError:
        raise RuntimeError(
            "ROOTSYS is {0} but running {1} failed".format(
                rootsys, root_config))
else:
    try:
        root_version = root_version_installed()
        root_cflags, root_ldflags = root_flags()
    except OSError:
        raise RuntimeError(
            "root-config is not in PATH and ROOTSYS is not set. "
            "Is ROOT installed correctly?")


extensions = [
  Extension( "baobab.PhysicsHelperFunctions",            ["baobab/PhysicsHelperFunctions.pyx"], extra_compile_args=root_cflags  ),
  Extension( "baobab.FinalStateObjectsSelector",         ["baobab/FinalStateObjectsSelector.pyx"], extra_compile_args=root_cflags ),
  Extension( "TTbarDiffXsAllHadBoosted.HistogramFiller", ["TTbarDiffXsAllHadBoosted/HistogramFiller.pyx"], extra_compile_args=root_cflags  ),             
  Extension( "TTbarDiffXsAllHadBoosted.Cutflow",         ["TTbarDiffXsAllHadBoosted/Cutflow.pyx"], extra_compile_args=root_cflags  ),
  Extension( "TTHBoostedAllHadronic.HistogramFiller",    ["TTHBoostedAllHadronic/HistogramFiller.pyx"], extra_compile_args=root_cflags  ),
  Extension( "TTHBoostedAllHadronic.Cutflow",            ["TTHBoostedAllHadronic/Cutflow.pyx"], extra_compile_args=root_cflags  ),

 ]

setup(name='Baobab',
      version='0.1',
#      py_modules=['runBaobab.py'],
      description='Analysis program based on root_numpy and python/cython',
      author='Riccardo Di Sipio',
      author_email='disipio@cern.ch',
      url='',
      packages=['baobab', 'TTbarDiffXsAllHadBoosted', 'TTHBoostedAllHadronic' ],
      scripts=['scripts/runBaobab.py'] + glob.glob( "scripts/baobab-*.sh" ), 
      package_data={
           'baobab'                   : [ "share/*" ], 
           'TTbarDiffXsAllHadBoosted' : [ "config/*.xml", "config/*.dat", "config/analysis_params/*.xml",  "config/filelist/*.dat" ],
           'TTHBoostedAllHadronic'    : [ "config/*.xml", "config/*.dat", "config/analysis_params/*.xml",  "config/filelist/*.dat" ], 
          },
#      ext_modules = cythonize("baobab/*.pyx", "TTbarDiffXsAllHadBoosted/*.pyx" ),
      ext_modules = cythonize( extensions ),
     )
