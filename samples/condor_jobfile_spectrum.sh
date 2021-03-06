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
index="190507"

# channel list file can be generated by hand or by chlist.sh.      
# chlist.sh will not rewrite existing file.
channels="chlist.dat"
./chlist.sh $channels

gpsstart=("1237888878" "1237923078")
gpsend=("1237888978" "1237923178")

#kamioka=true
kamioka=false  

# Set the output directory.

name="spectrum"
  
if [ "$condir" = "" ]; then
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
echo "Notification = never"
# if needed, use following line to set the necessary amount of the memory for a job. In Kashiwa, each node has total memory 256 GB, 2 CPU, 28 cores.
echo "request_memory = 1 GB"
echo "Getenv  = True "
echo ""
echo "should_transfer_files = YES"
echo "when_to_transfer_output = ON_EXIT"
echo ""
} > job_${name}.sdf

# Loop over each plot. 

# Loop over each plot.                                                  
option=""
if "${kamioka}" ; then
    option+=" -k"
fi

cat $channels | while read chlist
do
    {
    # channel can be array for the argument. 
    # if you need, you can use argument of -t (legend type), -p (legend position), -f (FFT length). Please try 
    #  $ python batch_spectrum.py -h
    # for detail.
#    echo "Arguments = -c ${chlist} -s ${gpsstart[@]} -e ${gpsend[@]} -o ${outdir} -i ${index} -t time"
    echo "Arguments = -c ${chlist} -s ${gpsstart[@]} -e ${gpsend[@]} -o ${outdir} -i ${index} -t combined ${option}"
    echo "Output       = log/out_\$(Cluster).\$(Process).txt"
    echo "Error        = log/err_\$(Cluster).\$(Process).txt"
    echo "Queue"
    } >> job_${name}.sdf
done

# Submit job into condor.

echo job_${name}.sdf
condor_submit job_${name}.sdf
