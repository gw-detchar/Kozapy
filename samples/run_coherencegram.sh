#!/bin/bash

# PLEASE NEVER CHANGE THIS FILE BY HAND.
# This file is generated from condor_jobfile_coherencegram.sh.
# If you need to change, please edit condor_jobfile_coherencegram.sh.

if [ `hostname` == "m31-01.kagra.icrr.u-tokyo.ac.jp" ]; then
    Kozapy=/home/chihiro.kozakai/detchar/analysis/code/gwpy/Kozapy/samples
elif [ `hostname` == "m31-02.kagra.icrr.u-tokyo.ac.jp" ]; then
    Kozapy=/home/chihiro.kozakai/detchar/analysis/code/gwpy/Kozapy/samples
else
    Kozapy=/users/DET/tools/GlitchPlot/Script/Kozapy/samples
fi

echo $@
python $Kozapy/batch_coherencegram.py $@
