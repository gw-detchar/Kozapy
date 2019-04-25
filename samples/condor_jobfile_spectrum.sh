#!/bin/bash

################################################################
# This file is for submitting spectrum plot job into condor.
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
index="190408"

source mylib/Kchannels.sh  #  This shell script includes some channel lists. If you need new list, please see mylib/Kchannels.py. 
channels=(${LAS_IMC[@]})
channels+=(${SEIS_IXV[@]})

gpsstart=("1237888878" "1237923078")
gpsend=("1237888978" "1237923178")

# Set the output directory.

name="spectrum"
  
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
#py="~/batch_spectrum.py"  # For the case you use non-conventional python script name.

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

for channel in ${channels[@]}; do
    {
    # channel can be array for the argument. 
    # if you need, you can use argument of -t (legend type), -p (legend position), -f (FFT length). Please try 
    #  $ python batch_spectrum.py -h
    # for detail.
    echo "Arguments = -c ${channel} -s ${gpsstart[@]} -e ${gpsend[@]} -o ${outdir} -i ${index} -t time"
    echo "Output       = log/out_\$(Cluster).\$(Process).txt"
    echo "Error        = log/err_\$(Cluster).\$(Process).txt"
    echo "Log          = log/log_\$(Cluster).\$(Process).txt"
    echo "Queue"
    } >> job_${name}.sdf
done

# Submit job into condor.

echo job_${name}.sdf
condor_submit job_${name}.sdf