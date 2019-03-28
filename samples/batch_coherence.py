

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

refchannel = args[1]
channel = args[2]
gpsstart = args[3]
gpsend = args[4]
outdir = args[5]
date = args[6]

print('gpsstart ' + gpsstart)
print('gpsend ' + gpsend)
print('refchannel ' + refchannel)
print('channel ' + channel)
print('outdir' + outdir)
print('date' + date)



unit = ''
if channel.find('TEMPERATURE') != -1:
    unit = r'Temperature [\textcelsius]' 
elif channel.find('HUMIDITY') != -1:
    unit = 'Humidity [\%]'
elif channel.find('ACC') != -1:
    unit = r'Acceleration [$m/s^2$]'
elif channel.find('MIC') != -1:
    unit = 'Sound [Pa]'

channels = [refchannel, channel]
    
latexchnames = channel.replace('_','\_')
latexrefchnames = refchannel.replace('_','\_')

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

data = TimeSeriesDict.read(sources,channels,format='gwf.lalframe',nproc=2,start=int(gpsstart),end=int(gpsend))
    
ref = data[refchannel]
acc = data[channel]

#coh = ref.coherence_spectrogram(acc,512,fftlength=64)
coh = ref.coherence_spectrogram(acc,2048,fftlength=256)

cohplot=coh.plot(figsize = (16, 9))
ax = cohplot.gca()
ax.set_ylabel('Frequency [Hz]')
ax.set_yscale('log')
ax.set_title(latexrefchnames + ' ' + latexchnames)
ax.set_ylim(0.1,1000)

cohplot.add_colorbar(cmap='winter',label='Coherence')

#sgplot.savefig('/home/chihiro.kozakai/detchar/analysis/condor/result/' + channel + '_whiteningspectrogram_'+ gpsstart + '-' + gpsend +'_190314.pdf')
#cohplot.savefig(outdir + refchannel + '_' + channel + '_coherence_'+ gpsstart + '_' + gpsend +'_' + date +'.pdf')
cohplot.savefig(outdir + refchannel + '_' + channel + '_coherence_'+ gpsstart + '_' + gpsend +'_' + date +'.png')

cohplot.clf()
cohplot.close()

print(outdir + refchannel + '_' + channel + '_coherence_'+ gpsstart + '_' + gpsend +'_' + date +'.pdf')
print('Successfully finished !')
