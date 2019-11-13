#!/bin/bash

hostname=`hostname`

if [ "`echo $hostname | grep  kagra.icrr.u-tokyo.ac.jp `" ]; then
    Kozapy=/home/chihiro.kozakai/detchar/analysis/code/gwpy/Kozapy/samples
else
    Kozapy=/users/DET/tools/GlitchPlot/Script/Kozapy/samples
fi


echo $@
python $Kozapy/batch_spectrum.py $@
