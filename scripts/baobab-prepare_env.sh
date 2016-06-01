#!/bin/bash

INSTALLDIR=$(python -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")

ANALYSIS=$1
if [ "$1" == "" ] 
then
  echo "ERROR: please specify one analysis package"
  exit
fi


echo "INFO: Preparing environment for Baobab/$ANALYSIS"
echo "INFO: Config files from $INSTALLDIR"

cat > setenv.sh << EOF
export DERIVATION="TOPQ4"
export SELECTION="TightTop"
export DSID=410007
export SFMC=0.75
export SYSTEMATICS=allhadronic-systematics_all.dat
export BAOBAB_ANALYSIS=$ANALYSIS

echo "INFO: analysis    = \$BAOBAB_ANALYSIS"
echo "INFO: derivation  = \$DERIVATION"
echo "INFO: selection   = \$SELECTION"
echo "INFO: SFMC        = \$SFMC"
echo "INFO: signl DSID  = \$DSID"
echo "INFO: systematics = \$SYSTEMATICS"

echo "To mount EOS: eosmount eos"
EOF

[ ! -d eos    ] && mkdir -p eos
[ ! -d logs   ] && mkdir -p logs
[ ! -d jobs   ] && mkdir -p jobs
[ ! -d output ] && mkdir -p output/{data,nominal,particle,parton,uncertainty,test}

ln -s $INSTALLDIR/$ANALYSIS/config/ .
