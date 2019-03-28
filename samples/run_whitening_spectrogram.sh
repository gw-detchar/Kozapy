#!/bin/bash

#source /home/chihiro.kozakai/.bashrc

#source /opt/intel/bin/compilervars.sh intel64

# Source global definitions                                                                            
#if [ -f /etc/bashrc ]; then
#        . /etc/bashrc
#fi

echo $@
python /home/chihiro.kozakai/detchar/analysis/code/gwpy/newyear/batch_whitening_spectrogram.py $@
#python /home/chihiro.kozakai/detchar/analysis/code/gwpy/newyear/batch_test1.py $@

