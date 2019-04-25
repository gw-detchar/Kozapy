# Kozapy
This repository contains sample code for GWpy [https://gwpy.github.io/docs/stable/index.html].


## Contents 

#### example_read
Basic examples for begginer to read data 

#### script
Script for making a cache file.

#### sample/mylib/*
Making libraries. 
###### Kchannels.py, Kchannel.sh
Channel lists are given. If you want to add new list, first write it in the python file and then copy and paste the last 2 lines replacing channel name to your new channnel list. Please do "python Kchannels.py", and you will get Kchannel.sh with new list. it can be used by exporting.
###### ck.py
It has convenient functions. 

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

  4/24: Added new feature. 
  locked segments can be plotted below the spectrogram.
  To use it, add options of 
  -l 'guardian channel' -n number of required state --llabel optional, for ytitle
  ex) -l 'K1:GRD-IO_STATE_N' -n 99 --llabel 'IMC_LSC'
#### batch_coherencegram.py, condor_jobfile_coherencegram.sh, run_coherencegram.sh
  They make coherencegram plots in batch job. 
  Please see the description for batch job for whitening spectrum to learn how to use them. 
  
#### batch_timeseries.py, condor_jobfile_timeseries.sh, run_timeseries.sh
  They make timeseries plots in batch job. 
  Please see the description for batch job for whitening spectrum to learn how to use them. 
  
#### batch_spectrum.py, condor_jobfile_spectrum.sh, run_spectrum.sh
  They make spectrum plots in batch job. 
  Please see the description for batch job for whitening spectrum to learn how to use them. 
  
## Tips for condor

##### ジョブファイルの例
Universe     = vanilla
Executable   = [実行ファイルの名前、絶対PATHで書いておくと便利]
Notify_User  =
Notification = always
request_memory = 1 GB
GetEnv       = true

should_transfer_files = YES
when_to_transfer_output = ON_EXIT
Arguments    = [Executableの後ろに引数やオプションが必要であればここに書く、ないなら空白にしておく]
Output       = result/out_$(Cluster).$(Process).txt
Error        = result/err_$(Cluster).$(Process).txt
Log          = result/log_$(Cluster).$(Process).txt
Queue
##### 例おわり #####

Output, Error, Logは実行結果がそこに出力されます、Outputは標準出力、Errorは標準エラー、Logは実行時間や必要だったメモリ量などが記録されます
$(Cluster).$(Process)とか書いてますが、これは実行時に自動的に置き換わるマクロ変数なので気にせずこのままにしておくと便利です

注意しておいたほうがいいこととしては、実行ファイルの中で相対PATHを使ったファイル入出力はできないということです
たぶんハマるとしたらここなのでご注意ください

request_memory は必ず設定してください。
request_memoryの値は，そのジョブで実際に必要なメモリの値を書いて下さい．
各ノードはメモリ256GB，2CPU，全コア数28コアです．
メモリは256GB以内で指定して下さい．
ただ，例えば256GBを指定すると，1ジョブで全メモリを使うと言うことなので，
1ノードに1つのジョブしか割り当てられなくなります．


#########
以下はジョブファイルを扱うコマンドの一例です、自分が知ってて使ってるほぼすべてです(なにか他に便利なコマンドがわかりましたら教えてください)

ジョブファイルをcondorに投げる
% condor_submit [ジョブファイル]

ジョブの状況を確認する
% condor_q

他の人のも見たいとき
% condor_q -all

すべてのオプションを表示したいとき
% condor_q -w

ジョブを止めたいとき
ジョブ番号はcondor_qで一番左端にあるIDのこと
15371.0と15371.1が同時に走っているときはcondor_rm 15371で2つとも止めることもできます
% condor_rm [ジョブの番号]