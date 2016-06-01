#!/bin/bash

SUBMISSION_TIMESTAMP=$(date +"%Y%m%d%H%M%S")

#skipwn='-R "select[ (hname!='wn-205-04-13-02-b') && (hname!='wn-205-04-24-01-b') && (hname!='wn-205-04-22-01-b')]"'

######################

function print_help {
    echo "To submit a job to your batch system:"
    echo "$0 -p paramfile.xml -f file_list.txt [-n n_events_max] [-o output_file_name.root] [-j job_name] [-q queue]"
    exit
}

######################


if [ -z ${ROOTCOREDIR} ]
then
  echo "ROOTCOREDIR not set. Did you set up the environment first?"
  exit
fi

WORKDIR=${PWD}
jobdir=${WORKDIR}/jobs
logdir=${WORKDIR}/logs

if [[ -z ${OUTPUTDIR} ]]
then
   outdir=${WORKDIR}/output
else
   outdir=${OUTPUTDIR}
fi

queue=1nh #CERN LXPLUS
backend=lsf #options are: lsf pbs
dryrun=0

jobname=Job_${SUBMISSION_TIMESTAMP}
filelist=UNSET
outfilename=output/test/histograms.root
nevents=-1
xmlconfig=config/analysis_params/nominal.xml

while [ $# -gt 0 ] ; do
case $1 in
    -b) backend=$2             ; shift 2;;
    -c) xmlconfig=$2           ; shift 2;;
    -i) filelist=$2            ; shift 2;;
    -n) nevents=$2             ; shift 2;;
    -o) outfilename=$2         ; shift 2;;
    -q) queue=$2               ; shift 2;;
    -j) jobname=$2             ; shift 2;;
    -d) dryrun=$2              ; shift 2;;
    -h) print_help             ; shift 2;;
    *)                           shift 1;;
esac
done

if [ -z filelist ]
then
    echo File list not set
    exit
fi

# determine which backend to use
if [ "$backend" == "lsf" ]
then
   exe="bsub"
   logopts="-oe -oo"
   jobnameopts="-J"
else
   exe="qsub -V"
   logopts="-j oe -o"
   jobnameopts="-N"
fi


test -d $jobdir || mkdir -p $jobdir
test -d $logdir || mkdir -p $logdir
test -d $outdir || mkdir -p $outdir

jobfile=$jobdir/${jobname}.job.sh
logfile=$logdir/${jobname}.log

rm -fr $logfile
rm -fr $logfile.ok
rm -fr $logfile.fail

## NOW CREATE ON-THE-FLY THE SCRIPT TO BE SUBMITTED
echo job file: ${jobfile}

# add to run on scinet ?
#PBS -l nodes=1:ppn=8,walltime=2:00:00
#PBS -N $jobname

cat > ${jobfile} <<EOF
#!/bin/bash
echo Running on \$HOSTNAME
echo Shell: $SHELL
echo Timestamp: $(date)

# setup the environment

##export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase
source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh

cd ${ROOTCOREBIN}/..
source $ATLAS_LOCAL_RCSETUP_PATH/rcSetup.sh
source setenv.sh

cd ${WORKDIR}

source /afs/cern.ch/project/eos/installation/atlas/etc/setup.sh 
[ ! -d eos ] && mkdir -p eos
eosmount eos

time runBaobab.py -i ${filelist} -o ${outfilename} -c ${xmlconfig} -n ${nevents} 

echo "End of run"
date

EOF


# OK NOW SUBMIT THE JOB

chmod +x $jobfile

if [[ "${dryrun}" == "0" ]] 
then
  ${exe} -q $queue ${logopts} $logfile ${jobnameopts} $jobname $jobfile #${skipwn}
else
  echo "Dry run. See ${jobfile}"
fi

job_return_code=$?
if [ $job_return_code -ne 0 ]
then
  touch $logdir/${jobname}.fail
  echo Job command has failed with code=$job_return_code - quit job now...
  exit $job_return_code
else
  touch $logdir/${jobname}.ok
fi

