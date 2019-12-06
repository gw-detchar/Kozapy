#!/bin/bash

# PLEASE NEVER CHANGE THIS FILE BY HAND.
# This file is generated from condor_jobfile_timeseries.sh.
# If you need to change, please edit condor_jobfile_timeseries.sh.

echo $@
python /users/DET/tools/GlitchPlot/Script/Kozapy/samples/batch_timeseries.py $@
