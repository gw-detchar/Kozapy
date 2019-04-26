#!/bin/bash

# Usage: ./chlist.sh output_chlist.dat
# $1 is output file name. 
# This file generates channel lists file if $1 does not exist. 
# In condor_jobfile_*.sh, the channel list of this output file $tmp is used line by line. 

source mylib/Kchannels.sh

tmp=$1

if [ ! -e $tmp ]; then
    echo "Make new channel list $1."

    suffix=(".mean" ".max" ".min")

    # List channels to be plotted in one png file in a line.
    # First line has to be ended by        } > $tmp
    # The other lines have to be ended by  } >> $tmp

    {
	echo ${SEIS_IXV[@]} ${LAS_IMC[@]}
    } > $tmp

    {
	channel=${LAS_IMC[@]}
	chlist=()
	for s in ${suffix[@]}; do
	    chlist+=( $channel$s )
	done
	echo ${chlist[@]}
    } >> $tmp

else
    echo "Use existing list."
fi

#cat $tmp | while read line
#do
#    echo "echo " $line
#done