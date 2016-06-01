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
      scripts=['scripts/runBaobab.py'],
     )
