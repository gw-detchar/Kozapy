

__author__ = "Chihiro Kozakai"

import sys
import glob
import matplotlib

matplotlib.use('Agg')  # this line is required for the batch job before importing other matplotlib modules.

from gwpy.timeseries import TimeSeries
from gwpy.timeseries import TimeSeriesDict
#from matplotlib import pylab as pl
from gwpy.detector import Channel
from matplotlib import cm


args = sys.argv

channel = args[1]
gpsstart = args[2]
gpsend = args[3]
outdir = args[4]
date = args[5]

print('gpsstart ' + gpsstart)
print('gpsend ' + gpsend)
print('channel ' + channel)
print('outdir' + outdir)
print('date' + date)

print(outdir + channel + '_whiteningspectrogram_'+ gpsstart + '_' + gpsend +'_' + date +'.pdf')

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

print(data.unit)
    
#white = data.whiten(fftlength=512)
#whitespectrogram = white.spectrogram(512,fftlength=8)
white = data.whiten(fftlength=1)
whitespectrogram = white.spectrogram(1)

sgplot=whitespectrogram.plot(figsize = (16, 9))
ax = sgplot.gca()
ax.set_ylabel('Frequency [Hz]')
ax.set_yscale('log')
ax.set_title(latexchnames)
ax.set_ylim(0.1,1000)

sgplot.add_colorbar(cmap='winter',label='Arbitrary')

#sgplot.savefig('/home/chihiro.kozakai/detchar/analysis/condor/result/' + channel + '_whiteningspectrogram_'+ gpsstart + '-' + gpsend +'_190314.pdf')
sgplot.savefig(outdir + channel + '_whiteningspectrogram_'+ gpsstart + '_' + gpsend +'_' + date +'.png')

sgplot.clf()
sgplot.close()

print(outdir + channel + '_whiteningspectrogram_'+ gpsstart + '_' + gpsend +'_' + date +'.png')
print('Successfully finished !')
