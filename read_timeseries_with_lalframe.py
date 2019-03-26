'''Read timeseries from gwffile
'''

__author__ = "Chihiro Kozakai"

from gwpy.timeseries import TimeSeries
from gwpy.timeseries import TimeSeriesDict
from matplotlib import pylab as pl
from gwpy.detector import Channel

# readout from gwf file
#for single file
#source = '/data/full/12311/K-K1_C-1231133824-32.gwf'
#if multiple files needed,
sources = ['/data/full/12311/K-K1_C-1231133824-32.gwf','/data/full/12311/K-K1_C-1231133856-32.gwf']

#for single channel
chname = 'K1:PEM-IXV_GND_TR120Q_X_OUT_DQ'
#for multiple channels
chnames = ['K1:PEM-IXV_GND_TR120Q_X_OUT_DQ', 'K1:PEM-IXV_GND_TR120Q_Y_OUT_DQ']

# Time series
#for single channel,
#data = TimeSeries.read(source,chname,format='gwf.lalframe',nproc=2,start=1231133850,end=1231133860,resample=10.)
data = TimeSeries.read(sources,chname,format='gwf.lalframe')
#for multiple channels, TimeSeriesDict should be used
#data = TimeSeriesDict.read(source,chnames,format='gwf.lalframe',nproc=2)
#source and chname are necessary.
#format='gwf.lalframe': input file format
#nproc=2              : # of CPUs
#start=1231133850     : start time can be selected.
#end=1231133860       : end time can be selected.
#resample=10.         : change the sampling rate. [Hz]
#data.override_unit('um/s')
print(data)

#plot the data in time series
plot = data.plot()

#save as a png file
plot.savefig('result_timeseries.png')
plot.close()

# write to text file
data.write('timeseries.txt')

# Transform to frequency series
spectrum = data.psd()

fplot = spectrum.plot()
fplot.savefig('result_frequencyseries.png')
fplot.close()

spectrum.write('frequencyseries.txt')

# Transform to spectrogram
sg = data.spectrogram(20,fftlength=8,overlap=4)
# 1 is time bin width in sec.

ftplot = sg.plot(norm='log',vmin=1e-6, vmax=1)
ax1 = ftplot.gca()
ax1.set_ylim(0.01,1000)
ax1.set_yscale('log')
ftplot.add_colorbar(cmap='YlGnBu', log=True)

ftplot.savefig('result_spectrogram.png')

#ftplot.show()
ftplot.close()

#sg.write('spectrogram.txt')

qt = data.q_transform()
qtplot = qt.plot(norm='log')
qtplot.add_colorbar(cmap='YlGnBu', log=True)
qtplot.show()
qtplot.savefig('result_spectrogram.png')
qtplot.close()
