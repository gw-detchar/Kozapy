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


# readout from gwf file
# measurement period 2018/12/29~2019/01/03, 1230044418~1230476418
gpsstart = '1230044418'
gpsend = '1230045418'
#gpsend = '1230130818' # 12/29 24:00
#gpsend = '1230217218' # 12/30 24:00
#gpsend = '1230303618' # 12/31 24:00
#gpsend = '1230390018' # 1/1 24:00
# 1/2 24:00
#gpsend = '1230476418' 


# make file list

sources = []

for i in range(int(gpsstart[0:5]),int(gpsend[0:5])+1):
    dir = '/data/trend/minute/' + str(i) + '/*'
    source = glob.glob(dir)
    sources.extend(source)

sources.sort()

removelist = []

for x in sources:
    if int(x[32:42])<(int(gpsstart)-3599):
        removelist.append(x)
    if int(x[32:42])>int(gpsend):
        removelist.append(x)

for y in removelist:
    sources.remove(y)

# make channel list
channels=['K1:PEM-PSL_ACC_PERI_REFCAV_OUT_DQ',
          'K1:PEM-PSL_ACC_PERI_EXIT_OUT_DQ',
          'K1:PEM-PSL_ACC_SIGNAL1_OUT_DQ',
          'K1:PEM-PSL_ACC_SIGNAL2_OUT_DQ',
          'K1:PEM-PSL_ACC_TABLE1_Z_OUT_DQ',
          'K1:PEM-PSL_ACC_TABLE2_Z_OUT_DQ',
          'K1:PEM-PSL_ACC_TABLE3_Z_OUT_DQ',
          'K1:PEM-PSL_MIC_CENTER_OUT_DQ',
          'K1:PEM-HUMIDITY_BOOTH_PSL',
          'K1:PEM-TEMPERATURE_BOOTH_PSL',
          'K1:PEM-HUMIDITY_FIELD_PSL2',
          'K1:PEM-TEMPERATURE_FIELD_PSL2',
          'K1:PEM-HUMIDITY_FIELD_PSL',
          'K1:PEM-TEMPERATURE_FIELD_PSL']

if not os.path.exists('results'):
    cmd = 'mkdir results'
    subprocess.call(cmd.split())

for channel in channels:
    print(channel)
    chnames = []
    latexchnames = []
    suffix = ['max','min','mean']

    unit = ''
    if channel.find('TEMPERATURE') != -1:
        unit = r'Temperature [\textcelsius]' 
    elif channel.find('HUMIDITY') != -1:
        unit = 'Humidity [\%]'
    elif channel.find('ACC') != -1:
        unit = r'Acceleration [$m/s^2$]'
    elif channel.find('MIC') != -1:
        unit = 'Sound [Pa]'

    for x in suffix:
        chnames.append(channel + '.' + x)
        latexchnames.append(channel.replace('_','\_') + '.' + x)

    # Time series
    data = TimeSeriesDict.read(sources,chnames,format='gwf.lalframe',nproc=2,start=int(gpsstart))
    #source and chname are necessary.
    #format='gwf.lalframe': input file format
    #nproc=2              : # of CPUs
    #start=1231133850     : start time can be selected.
    #end=1231133860       : end time can be selected.
    #resample=10.         : change the sampling rate. [Hz]
    #data.override_unit(unit)
    
    plot = data.plot(label='name')
    ax = plot.axes
    ax[0].legend(latexchnames,bbox_to_anchor = (1,0),loc='lower right',borderaxespad=1)
    ax[0].set_ylabel(unit)
    plot.savefig('results/' + channel + '_timeseries.png')
    plot.close()
