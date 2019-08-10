'''Make spectrums. If several channels or times are given, they are overlaid.
'''

__author__ = "Chihiro Kozakai"

import os
import matplotlib
matplotlib.use('Agg')  # this line is required for the batch job before importing other matplotlib modules.     

import subprocess
import glob
from gwpy.timeseries import TimeSeries
from gwpy.timeseries import TimeSeriesDict
from matplotlib import pylab as pl
from gwpy.detector import Channel
from matplotlib import cm
from mylib import mylib

from matplotlib import pylab as pl
pl.rcParams['font.size'] = 16
pl.rcParams['font.family'] = 'Verdana'

#  argument processing
import argparse

parser = argparse.ArgumentParser(description='Make spectrums. If several channels or times are given, they are overlaid.')
parser.add_argument('-o','--outdir',help='output directory.',default='/tmp')
parser.add_argument('-c','--channel',help='channel list.',nargs='*',required=True)
parser.add_argument('-s','--gpsstart',help='GPS starting time list.',nargs='*',required=True)
parser.add_argument('-e','--gpsend',help='GPS ending time list.',nargs='*',required=True
)
parser.add_argument('--title',help='Legend title list.',nargs='*',default=None)
parser.add_argument('-t','--ltype',help='Legend type. Choice is \'time\', \'channel\', or \'combined\'.',default='combined',choices=['time','channel','combined'])
parser.add_argument('-p','--lposition',help='Legend position. Choice is \'br\'(bottom right), \'bl\'(bottom left), \'tr\'(top right), or \'tl\'(top left), .',default='tr',choices=['br','bl','tr','tl'])
parser.add_argument('--dpi',help='Plot resolution. dot per inch.',type=int,default=100)
parser.add_argument('-f','--fftlength',help='FFT length.',type=float,default=1.)
parser.add_argument('-i','--index',help='It will be added to the output file name.',default='test')
parser.add_argument('-k','--kamioka',help='Flag to run on Kamioka server.',action='store_true')


# define variables
args = parser.parse_args()
outdir=args.outdir
channels=args.channel
gpsstarts=args.gpsstart
gpsends=args.gpsend
index=args.index
fft=args.fftlength
ol=fft/2.  #  overlap in FFTs. 

title=args.title
ltype=args.ltype
lposition=args.lposition
dpi=args.dpi
kamioka = args.kamioka

# Loop over channels and gps times.
isFirst = True
legend = []

#legend title
if title != None:
    legend=title

#color list
color=["orange","royalblue","limegreen","red","gold","magenta","lightskyblue","black","aquamarine","darkorchid","saddlebrown","salmon","greenyellow","navy"]
colorindex=0

for channel in channels:

    #unit = r'Amplitude [$\sqrt{\mathrm{Hz}^{-1}}$]'
    unit = 'Amplitude [1/rHz]'
    if channel.find('ACC') != -1:
        #unit = r'Acceleration [$m/s^2$ $/ \sqrt{\mathrm{Hz}^{-1}}$]'
        unit = 'Acceleration [m/s^2/rHz]'
    elif channel.find('MIC') != -1:
        #unit = r'Sound [Pa $/ \sqrt{\mathrm{Hz}^{-1}}$]'
        unit = 'Sound [Pa/rHz]'

    for gpsstart,gpsend in zip(gpsstarts,gpsends):

        if kamioka:
            sources = mylib.GetFilelist_Kamioka(gpsstart,gpsend)
        else:
            sources = mylib.GetFilelist(gpsstart,gpsend)

        data = TimeSeries.read(sources,channel,format='gwf.lalframe',start=float(gpsstart),end=float(gpsend))
        
        if fft > float(gpsend)-float(gpsstart): 
            tmpfft = float(gpsend)-float(gpsstart)
            tmpol = tmpfft / 2.
            print("Given FFT length is too long. Automatically modified to given time duration.")
            print("FFT length = " + str(tmpfft))
        elif fft <= data.dt.value:
            fft=2*data.dt.value
            ol=fft/2.  #  overlap in FFTs.
            stride=2*fft
            print("Given fft/stride was bad against the sampling rate. Automatically set to:")
            print("fft="+str(fft))
            print("ol="+str(ol))
            print("stride="+str(stride))
        else:
            tmpfft = fft
            tmpol = ol
        spectrum = data.asd(fftlength=tmpfft,overlap=tmpol)

        if isFirst:           
            fplot=spectrum.plot(figsize = (12, 8),color=color[colorindex])
            ax = fplot.gca()
            ax.set_ylabel(unit)
            ax.set_yscale('log')
            ax.set_title(mylib.GetTitlefromLegend(ltype,gpsstart,gpsend,channel)+" Spectrum")
            isFirst = False

        else:
            colorindex+=1
            ax.plot(spectrum,color=color[colorindex])

        if title == None:
            legend+=(mylib.GetLegend(ltype,gpsstart,gpsend,channel))

ax.legend(legend,bbox_to_anchor = mylib.GetBBTA(lposition),loc=mylib.Getloc(lposition),borderaxespad=1)

fname = outdir + '/' + channel + '_spectrum_' + gpsstart +  '_' + index + '.png'
print(fname)
fplot.savefig(fname,dpi=dpi)
fplot.clf()
fplot.close()


print('Successfully finished !')
