#!/bin/bash

OUTDIR=output/data
[ ! -d ${OUTDIR} ] && mkdir -p ${OUTDIR}

for file in $(ls config/filelist/data15_13TeV.DAOD_${DERIVATION}.dat.*)
do
  echo $file

  id=$(echo $file | cut -d'.' -f4)

  baobab-submit.sh -i $file -o ${OUTDIR}/data15_13TeV.DAOD_${DERIVATION}.histograms.root.${id} -j data15_13TeV.DAOD_${DERIVATION}.${id} 
done
