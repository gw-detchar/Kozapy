#!/bin/bash

# PLEASE NEVER CHANGE THIS FILE BY HAND.
# This file is generated from condor_jobfile_whitening_spectrogram.sh.
# If you need to change, please edit condor_jobfile_whitening_spectrogram.sh.

echo $@
python /home/chihiro.kozakai/detchar/analysis/code/gwpy/Kozapy/samples/batch_whitening_spectrogram.py $@
