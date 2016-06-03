.. -*- mode: rst -*-

Baobab: An analysis program based on root_numpy and python/cython
=================================================================

==============
* INSTALLATION
==============

.. code-block:: python

   virtualenv env_baobab
   source env_baobab/bin/activate
   
   # dependencies
   pip install numpy
   pip install root_numpy
   pip install cython
   pip install xmltodict
   
   git clone https://github.com/rdisipio/baobab.git


===============
* MISE EN PLACE
===============

.. code-block:: python

   setupATLAS
   cd /your/AnalysisTop
   rcSetup
   
   # setup local user libs (e.g. virtualenv, numpy), e.g.:
   export PYTHONPATH=$PWD/local/lib/python2.7/site-packages:$PYTHONPATH
   export PATH=$PWD/local/bin:$PATH
   lsetup "lcgenv -p LCG_84 x86_64-slc6-gcc49-opt pyanalysis"
   
   # activate virtual environment
   source env_baobab/bin/activate
   
   # go to your run directory
   cd baobab


===========
* EXECUTION
===========

Create file list, e.g.:

.. code-block:: bash

   ls /afs/cern.ch/work/d/disipio/public/ttbar_diffxs_13TeV/ntuples/allhad/disipio-20160521-02/*/* > share/filelist/data16_13TeV.DAOD_TOPQ4.dat

.. code-block:: bash  

   ./runBaobab.py -c configuration.xml -i share/filelist/data16_13TeV.DAOD_TOPQ4.dat -o output.root -n 100
