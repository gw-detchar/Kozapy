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
# measurement period 2018/12/29~2019/01/03, 1230044418~1230476418
gpsstarts = ['1230044418','1230104898','1230199938','1230407298']
gpsends = ['1230044518','1230104998','1230200038','1230407398']

channels=['K1:PEM-PSL_ACC_PERI_REFCAV_OUT_DQ',
          'K1:PEM-PSL_ACC_PERI_EXIT_OUT_DQ',
          'K1:PEM-PSL_ACC_SIGNAL1_OUT_DQ',
          'K1:PEM-PSL_ACC_SIGNAL2_OUT_DQ',
          'K1:PEM-PSL_ACC_TABLE1_Z_OUT_DQ',
          'K1:PEM-PSL_ACC_TABLE2_Z_OUT_DQ',
          'K1:PEM-PSL_ACC_TABLE3_Z_OUT_DQ',
          'K1:PEM-PSL_MIC_CENTER_OUT_DQ'
      ]

if not os.path.exists('results'):
    cmd = 'mkdir results'
    subprocess.call(cmd.split())
    print('directory results/ is made.')

isFirst = True

for channel in channels:
    print(channel)

    unit = ''
    if channel.find('ACC') != -1:
        unit = r'Acceleration [$m/s^2$]'
    elif channel.find('MIC') != -1:
        unit = 'Sound [Pa]'

    latexchnames = channel.replace('_','\_')

    for gpsstart,gpsend in zip(gpsstarts,gpsends):
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

        data = TimeSeries.read(sources,channel,format='gwf.lalframe',nproc=2,start=int(gpsstart),end=int(gpsend))

        fft=10
        ol=fft/2.
        spectrum = data.asd(fftlength=fft,overlap=ol)

        if isFirst:           
            fplot=spectrum.plot(figsize = (16, 9))
            ax = fplot.gca()
            ax.set_ylabel(unit)
            ax.set_yscale('log')
            ax.set_title(latexchnames)
            isFirst = False
        else:
            ax.plot(spectrum)

    ax.legend(gpsstarts,bbox_to_anchor = (1,0),loc='lower right',borderaxespad=1)
    fplot.savefig('results/' + channel + '_spectrum.png')
    fplot.clf()
    fplot.close()
