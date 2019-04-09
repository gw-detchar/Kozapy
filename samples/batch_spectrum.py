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

#  argument processing
import argparse

parser = argparse.ArgumentParser(description='Make spectrums. If several channels or times are given, they are overlaid.')
parser.add_argument('-o','--outdir',help='output directory.',default='result')
parser.add_argument('-c','--channel',help='channel list.',nargs='*',required=True)
parser.add_argument('-s','--gpsstart',help='GPS starting time list.',nargs='*',required=True)
parser.add_argument('-e','--gpsend',help='GPS ending time list.',nargs='*',required=True
)
parser.add_argument('-t','--ltype',help='Legend type. Choice is \'time\', \'channel\', or \'combined\'.',default='combined',choices=['time','channel','combined'])
parser.add_argument('-p','--lposition',help='Legend position. Choice is \'br\'(bottom right), \'bl\'(bottom left), \'tr\'(top right), or \'tl\'(top left), .',default='tr',choices=['br','bl','tr','tl'])
parser.add_argument('-f','--fftlength',help='FFT length.',type=float,default=1.)
parser.add_argument('-i','--index',help='It will be added to the output file name.',default='test')

# define variables
args = parser.parse_args()
outdir=args.outdir
channels=args.channel
gpsstarts=args.gpsstart
gpsends=args.gpsend
index=args.index
fft=args.fftlength
ol=fft/2.  #  overlap in FFTs. 

ltype=args.ltype
lposition=args.lposition

# Loop over channels and gps times.
isFirst = True
legend = []

for channel in channels:
    print(channel)

    unit = r'Amplitude [$\sqrt{\mathrm{Hz}^{-1}}$]'
    if channel.find('ACC') != -1:
        unit = r'Acceleration [$m/s^2$]'
    elif channel.find('MIC') != -1:
        unit = 'Sound [Pa]'

    for gpsstart,gpsend in zip(gpsstarts,gpsends):

        sources = mylib.GetFilelist(gpsstart,gpsend)

        data = TimeSeries.read(sources,channel,format='gwf.lalframe',start=int(gpsstart),end=int(gpsend))

        spectrum = data.asd(fftlength=fft,overlap=ol)

        if isFirst:           
            fplot=spectrum.plot(figsize = (12, 8))
            ax = fplot.gca()
            ax.set_ylabel(unit)
            ax.set_yscale('log')
            ax.set_title(mylib.GetTitlefromLegend(ltype,gpsstart,gpsend,channel))
            isFirst = False

        else:
            ax.plot(spectrum)

        print('plot is given.')
        print(ltype)
        print(gpsstart)
        print(gpsend)
        print(channel)
        legend+=(mylib.GetLegend(ltype,gpsstart,gpsend,channel))
        print(legend)


ax.legend(legend,bbox_to_anchor = mylib.GetBBTA(lposition),loc=mylib.Getloc(lposition),borderaxespad=1)

fname = outdir + '/' + channel + '_' + gpsstart +  '_spectrum_' + index + '.png'
fplot.savefig(fname)
fplot.clf()
fplot.close()

print(fname)
print('Successfully finished !')


