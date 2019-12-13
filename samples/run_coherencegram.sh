#!/bin/bash

# PLEASE NEVER CHANGE THIS FILE BY HAND.
# This file is generated from FPMI_coherencegram.sh.
# If you need to change, please edit FPMI_coherencegram.sh.

if [ `hostname` == "m31-01.kagra.icrr.u-tokyo.ac.jp" ]; then
    Kozapy=/home/chihiro.kozakai/detchar/analysis/code/gwpy/Kozapy/samples
elif [ `hostname` == "m31-02.kagra.icrr.u-tokyo.ac.jp" ]; then
    Kozapy=/home/chihiro.kozakai/detchar/analysis/code/gwpy/Kozapy/samples
else
    Kozapy=/users/DET/tools/GlitchPlot/Script/Kozapy/samples
    export PATH=/home/controls/bin:/home/controls/opt/summary-2.7/bin:/usr/local/bin:/usr/bin:/bin:/usr/local/games:/usr/games
fi

echo $@
#python /home/chihiro.kozakai/detchar/analysis/code/gwpy/Kozapy/samples/batch_coherencegram.py $@
python $Kozapy/batch_coherencegram.py $@
