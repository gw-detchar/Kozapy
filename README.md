# Kozapy
This directory contains sample code for GWpy [https://gwpy.github.io/docs/stable/index.html].


## Contents 
#### example_plot.py
  This is for GWpy beginers. Basic script to plot timeseries, spectrum and spectrogram. I recommend to check other sample code according to your purpose, they have more convenient functions.

#### example_timeseries.py
  It make a plot of minute-trend time series. Mean, maximum and minimum are overlaid.

#### example_spectrum.py
  Spectrums for given time spans are overlaid.

#### example_spectrogram.py
  Make spectrogram.

#### checkfile.py
  Check if frame file for given time span is not missing. The missing time is written down in a txt file.

#### batch_whitening_spectrogram.py, condor_jobfile_whiteningspectrogram.sh, run_whitening_spectrogram.sh, successcheck.sh
  They are scripts for batch job of condor. 
  They make whitened spectrograms.
  Please try it after replacing output directory 
  in condor_jobfile_whiteningspectrogram.sh. 
  To submit jobs, 
  $ ./condor_jobfile_whiteningspectrogram.sh
  A file to submit jobs to condor will be written and submitted. 
  Then, run_whitening_spectrogram.sh will run and 
  it executes batch_whitening_spectrogram.py. 
  The job status can be checked by 
  $ condor_q
  If you want to kill you jobs, 
  $ condor_rm (job number)
  After the jobs are finished, 
  you can check if they finished successfully by using successcheck.sh. 
  Please replace job number and sdf filename.
  $ ./successcheck.sh
  It will provide a new sdf file for failed job. 
  If the problem is not bug but any accidental one, 
  you can use it for re-submission of jobs.
  
#### batch_coherence.py, condor_jobfile_coherence.sh, run_coherence.sh
  They make coherence plots in batch job. 
  Please see the description for batch job for whitening spectrum to learn how to use them. 
  
#### example_read
Basic examples for begginer to read data 

#### example_cache
Script for making a cache file.