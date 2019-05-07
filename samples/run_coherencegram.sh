#!/bin/bash

# PLEASE NEVER CHANGE THIS FILE BY HAND.
# This file is generated from condor_jobfile_coherencegram.sh.
# If you need to change, please edit condor_jobfile_coherencegram.sh.

echo $@
python /home/chihiro.kozakai/detchar/analysis/code/gwpy/Kozapy/samples/batch_coherencegram.py $@
