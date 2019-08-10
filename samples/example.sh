#!/bin/bash

channel=( "K1:IMC-CAV_TRANS_OUT_DQ" )
#if you need multiple channel overlaid (for time series or spectrum)
#channel=( "K1:IMC-CAV_TRANS_OUT_DQ.min" "K1:IMC-CAV_TRANS_OUT_DQ.max" )

gpsstart=( 1249442120 )
gpsend=( 1249442130 )
outdir="/path/to/output/directory/"

fft=1
stride=1

python batch_whitening_spectrogram.py -c ${channel[@]} -s ${gpsstart[@]} -e ${gpsend[@]} -o ${outdir} -k -f 1 --stride 1 > /tmp/log 2>&1

output=$(tail -n 2 /users/DET/tools/iKozapy/Script/tmp | head -n 1)

eog $output
