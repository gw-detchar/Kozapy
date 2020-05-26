#!/bin/bash

DARM=K1:CAL-CS_PROC_DARM_DISPLACEMENT_DQ
channels=("K1:ASC-REFL_QPDA1_DC_PIT_OUT_DQ" "K1:ASC-REFL_QPDA1_DC_YAW_OUT_DQ")
gpsstart=1270974173
gpsend=1270974237
outdir=/home/$USER/omicron0415

kozapy=/home/chihiro.kozakai/detchar/analysis/code/gwpy/Kozapy/samples
mkdir -p $outdir


python $kozapy/batch_timeseries.py -c ${channels[@]} -s $gpsstart -e $gpsend -d full -o $outdir -i omicronmulti

for channel in ${channels[@]}; do
    python $kozapy/batch_timeseries.py -c $channel -s $gpsstart -e $gpsend -d full -o $outdir -i omicron
    python $kozapy/batch_whitening_spectrogram.py -c $channel -s $gpsstart -e $gpsend -w -o $outdir -i omicron
done



python $kozapy/batch_timeseries.py -c $DARM -s $gpsstart -e $gpsend -d full -o $outdir -i omicron
python $kozapy/batch_whitening_spectrogram.py -c $DARM -s $gpsstart -e $gpsend -w -o $outdir -i omicron 
    
