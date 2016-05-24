# baobab
Analysis program based on root_numpy and python/cython

* INSTALLATION
virtualenv env_root_python
pip install numpy
pip install root_numpy
git clone https://github.com/rdisipio/baobab.git

* EXECUTION
Create file list, e.g.:
ls /afs/cern.ch/work/d/disipio/public/ttbar_diffxs_13TeV/ntuples/allhad/disipio-20160521-02/*/* > share/filelist/data16_13TeV.DAOD_TOPQ4.dat

./runBaobab.py -a TestAnalysis -i share/filelist/data16_13TeV.DAOD_TOPQ4.dat -o output.root
