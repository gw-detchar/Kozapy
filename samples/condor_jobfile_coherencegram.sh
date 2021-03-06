#!/bin/bash

################################################################
# This file is for submitting coherencegram plot job into condor.
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

source mylib/Kchannels.sh  #  This shell script includes some channel lists. If you need new list, please see mylib/Kchannels.py. 

refchannels=("K1:IMC-CAV_TRANS_OUT_DQ" "K1:IMC-CAV_REFL_OUT_DQ")

channels=(${LAS_IMC[@]})
channels+=(${SEIS_IXV[@]})

gpsstarts=("1237888878" "1237923078")  # array of starting times
gpsends=("1237888978" "1237923178")  # array of ending times

#kamioka=true
kamioka=false  

# For locked segments bar plot.                            
lock=true

lchannel="K1:GRD-IO_STATE_N"  #guardian channel            
lnumber=99  #number of the required state                  
llabel='IMC_LSC'  #y-axis label for the bar plot.
# Set the output directory.

name="coherencegram"
  
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
#py="~/batch_coherencegram.py"  # For the case you use non-conventional python script name.

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

option=""
if "${kamioka}" ; then
    option+=" -k"
fi

if "${lock}" ; then
    option+=" -l ${lchannel} -n ${lnumber} --llabel ${llabel}"
fi

# Loop over each plot. 

for refchannel in ${refchannels[@]}; do
    for channel in ${channels[@]}; do
	for i in ${!gpsstarts[@]}; do
	    {
		# channel can be array for the argument. 
		# if you need, you can use argument of -f (FFT length) and --stride (stride of the coherencegram). Please try 
		#  $ python batch_spectrum.py -h
		# for detail.
		echo "Arguments = -r ${refchannel} -c ${channel} -s ${gpsstarts[i]} -e ${gpsends[i]} -o ${outdir} -i ${index} ${option}"
		echo "Output       = log/out_\$(Cluster).\$(Process).txt"
		echo "Error        = log/err_\$(Cluster).\$(Process).txt"
		echo "Queue"
	    } >> job_${name}.sdf
	done
    done
done
# Submit job into condor.

echo job_${name}.sdf
condor_submit job_${name}.sdf
