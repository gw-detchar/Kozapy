#!/bin/bash

DARM=K1:CAL-CS_PROC_DARM_DISPLACEMENT_DQ
channels=("K1:PEM-MIC_OMC_TABLE_AS_Z_OUT_DQ")
gpsstart=1270998759
gpsend=1270998823
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
    
