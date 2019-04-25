#!/bin/bash

################################################################
# This file is for submitting time series plot job into condor.
#
# $condir will be used as output directory.
#
# Recommendation: 
# 
# In python script, package Kozapy/samples/mylib/ is reuired.
# Please make symbolic link in your working directory like this. 
# $ ln -s /path/to/Kozapy/samples/mylib/ mylib
#
# Edit your ~/.bashrc file and insert the output directory.
#  export condir=~/path/to/output/directory/
# If $condir is empty, current directory will be used.
################################################################

# Define variables.

# $index will be added to the output file name to distinguish from others. 
index="190425"

source mylib/Kchannels.sh  #  This shell script includes some channel lists. If you need new list, please see mylib/Kchannels.py. 

#channels=("K1:IMC-CAV_TRANS_OUT_DQ" "K1:IMC-CAV_REFL_OUT_DQ")

channels=(${LAS_IMC[@]})
channels+=(${SEIS_IXV[@]})

suffix=(".mean" ".max" ".min")

gpsstarts=("1237888878" "1237923078")  # array of starting times
gpsends=("1237889878" "1237924078")  # array of ending times

# default is to use minutes trend. second trend or full data can be used with following flags. Please set one of them true and set the others false. Or it will give warning message and exit. 

data="minute"
#data="second"
#data="full"

# For locked segments bar plot.
lock=true

lchannel="K1:GRD-IO_STATE_N.mean"  #guardian channel
lnumber=99  #number of the required state
llabel='IMC_LSC'  #y-axis label for the bar plot.

# Set the output directory.

name="timeseries"
  
if [ $condir = "" ]; then
    condir=$PWD
fi

outdir="$condir/${name}/"

# Confirm the existance of output directory.

if [ ! -e $outdir ]; then
    mkdir -p $outdir
fi

logdir="$PWD/log/"
if [ ! -e $logdir ]; then
    mkdir -p $logdir
fi

# make main script.

run="$PWD/run_${name}.sh"
py="$PWD/batch_${name}.py"
#py="~/batch_timesries.py"  # For the case you use non-conventional python script name.

{
echo "#!/bin/bash"
echo ""
echo "# PLEASE NEVER CHANGE THIS FILE BY HAND."
echo "# This file is generated from `basename $0`."
echo "# If you need to change, please edit `basename $0`."
echo ""
echo "echo \$@"
echo "python $py \$@"

} > $run

chmod u+x $run


# Write a file for condor submission.

{
echo "Executable = ${run}"
echo "Universe   = vanilla"
echo "Notification = always"
# if needed, use following line to set the necessary amount of the memory for a job. In Kashiwa, each node has total memory 256 GB, 2 CPU, 28 cores.
echo "request_memory = 1 GB"
echo "Getenv  = True            # the environment variables will be copied."
echo ""
echo "should_transfer_files = YES"
echo "when_to_transfer_output = ON_EXIT"
echo ""
} > job_${name}.sdf

# Loop over each plot. 
option=""
if [ lock ] ; then
    option+=" -l ${lchannel} -n ${lnumber} --llabel ${llabel}"
fi
echo $data
if [ $data = "minute" ] ; then
    option+=" -d minute"
elif [ $data = "second" ] ; then
    option+=" -d second"
elif [ $data = "full" ] ; then
    option+=" -d full"
fi

for channel in ${channels[@]}; do
    for i in ${!gpsstarts[@]}; do
	chlist=()
	for s in ${suffix[@]}; do
	    chlist+=( $channel$s )
	done

	{
	    # Please try
	    #  $ python batch_spectrum.py -h
	    # for option detail.

	    echo "Arguments = -c ${chlist[@]} -s ${gpsstarts[i]} -e ${gpsends[i]} -o ${outdir} -i ${index} ${option}"
	    echo "Output       = log/out_\$(Cluster).\$(Process).txt"
	    echo "Error        = log/err_\$(Cluster).\$(Process).txt"
	    echo "Log          = log/log_\$(Cluster).\$(Process).txt"
	    echo "Queue"
	} >> job_${name}.sdf
    done
done

# Submit job into condor.

echo job_${name}.sdf
condor_submit job_${name}.sdf