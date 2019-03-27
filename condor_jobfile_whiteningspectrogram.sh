#!/bin/bash

function writeSum(){
_suffix=$1
_exeName=$2
_gpsstart=$3
_gpsend=$4
_outdir=$5
_date=$6
shift
shift
shift
shift
shift
shift
_channelList=($@)

echo "Executable = ${_exeName}"
echo "Universe   = vanilla"
echo "Notification = always"
echo "Getenv  = True            # the environment variables will be copied."
echo ""
echo "# comment out the followings if you don't need to save STDOUT/STDERR/CondorLog"
echo "Log        = out_${_suffix}.log"
echo ""
echo "should_transfer_files = YES"
echo "when_to_transfer_output = ON_EXIT"

for _channel in ${_channelList[@]}; do
	    echo "Arguments = ${_channel} ${_gpsstart} ${_gpsend} ${_outdir} ${_date}"
	    echo "Output       = log/out_\$(Cluster).\$(Process).txt"
	    echo "Error        = log/err_\$(Cluster).\$(Process).txt"
	    echo "Log          = log/log_\$(Cluster).\$(Process).txt"
	    echo "Queue"
done
return
}

name="Whitening_spectrogram"


run="$PWD/run_whitening_spectrogram.sh"
echo $run
channel=()
channel+=("K1:PEM-PSL_ACC_PERI_REFCAV_OUT_DQ")
channel+=("K1:PEM-PSL_ACC_PERI_EXIT_OUT_DQ")
channel+=("K1:PEM-PSL_ACC_SIGNAL1_OUT_DQ")
channel+=("K1:PEM-PSL_ACC_SIGNAL2_OUT_DQ")
channel+=("K1:PEM-PSL_ACC_TABLE1_Z_OUT_DQ")
channel+=("K1:PEM-PSL_ACC_TABLE2_Z_OUT_DQ")
channel+=("K1:PEM-PSL_ACC_TABLE3_Z_OUT_DQ")
channel+=("K1:PEM-PSL_MIC_CENTER_OUT_DQ")
#gpsstart="1230044418"
#gpsend="1230087618"
#gpsstart="1230104898"
#gpsend="1230182658"
#gpsstart="1230199938"
#gpsend="1230390018"
gpsstart="1230407298"
gpsend="1230433218"

outdir="/home/chihiro.kozakai/detchar/analysis/condor/result/whitening_spectrogram/"
date="190314"

mkdir $outdir
writeSum ${name} $run $gpsstart $gpsend $outdir $date ${channel[@]}  > job_${name}_${gpsstart}.sdf

echo job_${name}_${gpsstart}.sdf
condor_submit job_${name}_${gpsstart}.sdf
