'''Read timeseries from gwffile
'''

__author__ = "Chihiro Kozakai"

import os
import subprocess
import glob
from gwpy.timeseries import TimeSeries
from gwpy.timeseries import TimeSeriesDict
from matplotlib import pylab as pl
from gwpy.detector import Channel
from matplotlib import cm

# readout from gwf file
gpsstart = '1230044418'
gpsend = '1230045018'

# make file list

sources = []

for i in range(int(gpsstart[0:5]),int(gpsend[0:5])+1):
    dir = '/data/full/' + str(i) + '/*'
    source = glob.glob(dir)
    sources.extend(source)

sources.sort()

removelist = []

for x in sources:
    if int(x[24:34])<(int(gpsstart)-31):
        removelist.append(x)
    if int(x[24:34])>int(gpsend):
        removelist.append(x)

for y in removelist:
    sources.remove(y)

channels=['K1:PEM-PSL_ACC_PERI_REFCAV_OUT_DQ',
          'K1:PEM-PSL_ACC_PERI_EXIT_OUT_DQ',
          'K1:PEM-PSL_ACC_SIGNAL1_OUT_DQ',
          'K1:PEM-PSL_ACC_SIGNAL2_OUT_DQ',
          'K1:PEM-PSL_ACC_TABLE1_Z_OUT_DQ',
          'K1:PEM-PSL_ACC_TABLE2_Z_OUT_DQ',
          'K1:PEM-PSL_ACC_TABLE3_Z_OUT_DQ',
          'K1:PEM-PSL_MIC_CENTER_OUT_DQ',
      ]

if not os.path.exists('results'):
    cmd = 'mkdir results'
    subprocess.call(cmd.split())

for channel in channels:
    print(channel)

    unit = ''
    if channel.find('TEMPERATURE') != -1:
        unit = r'Temperature [\textcelsius]' 
    elif channel.find('HUMIDITY') != -1:
        unit = 'Humidity [\%]'
    elif channel.find('ACC') != -1:
        unit = r'Acceleration [$m/s^2$]'
    elif channel.find('MIC') != -1:
        unit = 'Sound [Pa]'

    latexchnames = channel.replace('_','\_')

    # Time series
    data = TimeSeries.read(sources,channel,format='gwf.lalframe',nproc=2,start=int(gpsstart))
    #source and chname are necessary.
    #format='gwf.lalframe': input file format
    #nproc=2              : # of CPUs
    #start=1231133850     : start time can be selected.
    #end=1231133860       : end time can be selected.
    #resample=10.         : change the sampling rate. [Hz]
    #data.override_unit(unit)

    fft=1
    ol=fft/2.
    stride=1

    if fft > stride:
        print('Warning: stride is shorter than fft length. Set stride=fft.')
        stride=fft

    spectrogram = data.spectrogram(stride, fftlength=fft,overlap=ol)
    print(4)   
    ftplot=spectrogram.plot(norm='log')
    ax = ftplot.axes
    ax[0].set_ylabel('Frequency [Hz]')
    ax[0].set_ylim(0.1,1000)
    ax[0].set_yscale('log')
    ax[0].set_title(latexchnames)

    ftplot.add_colorbar(cmap='winter',log=True,label=unit)

    ftplot.savefig('results/' + channel + '_spectrogram.png')
    ftplot.close()
    print(5)   
