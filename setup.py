#!/usr/bin/env python

from distutils.core import setup

setup(name='Baobab',
      version='0.1',
#      py_modules=['runBaobab.py'],
      description='Analysis program based on root_numpy and python/cython',
      author='Riccardo Di Sipio',
      author_email='disipio@cern.ch',
      url='',
      packages=['baobab', 'TTbarDiffXsAllHadBoosted' ],
      scripts=['scripts/runBaobab.py', 'scripts/baobab-prepare_env.sh', 'scripts/baobab-submit.sh' ],
      package_data={ 'baobab' : [ "share/*" ], 'TTbarDiffXsAllHadBoosted' : [ "config/*.xml", "config/*.dat", "config/analysis_params/*.xml",  "config/filelist/*.dat" ] },
     )
