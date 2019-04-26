'''Make spectrogram.
'''

__author__ = "Chihiro Kozakai"

import os
import matplotlib
matplotlib.use('Agg')  # this line is required for the batch job before importing other matplotlib modules.     

import subprocess
import glob
from gwpy.timeseries import TimeSeries
from gwpy.timeseries import TimeSeriesDict
from gwpy.segments import DataQualityFlag

from matplotlib import pylab as pl
from gwpy.detector import Channel
from matplotlib import cm
from mylib import mylib

#  argument processing
import argparse

parser = argparse.ArgumentParser(description='Make coherencegram.')
parser.add_argument('-o','--outdir',help='output directory.',default='result')
parser.add_argument('-c','--channel',help='channel.',required=True)
parser.add_argument('-s','--gpsstart',help='GPS starting time.',required=True)
parser.add_argument('-e','--gpsend',help='GPS ending time.',required=True
)
parser.add_argument('-f','--fftlength',help='FFT length.',type=float,default=1.)
parser.add_argument('--stride',help='Stride of the spectrogram.',type=float,default=10.)
parser.add_argument('-i','--index',help='It will be added to the output file name.',default='test')
parser.add_argument('-w','--whitening',help='Apply whitening.',action='store_true')

parser.add_argument('-l','--lchannel',help='Make locked segment bar plot.',default='')
parser.add_argument('--llabel',help='Label of the locked segment bar plot.',default='')
parser.add_argument('-n','--lnumber',help='The requirement for judging locked. lchannel==lnumber will be used as locked.',default=99,type=int)


# define variables
args = parser.parse_args()
outdir=args.outdir

channel=args.channel
latexchname = channel.replace('_','\_')

gpsstart=args.gpsstart
gpsend=args.gpsend
index=args.index
stride=args.stride
fft=args.fftlength
ol=fft/2.  #  overlap in FFTs. 

lchannel=args.lchannel
lnumber=args.lnumber
llabel=args.llabel

lflag=bool(lchannel)
whitening=args.whitening

if fft*2. > stride:
    print('Warning: stride is shorter than fft length. Set stride=fft*2.')
    stride=fft*2.
    
unit = r'Amplitude [$\sqrt{\mathrm{Hz}^{-1}}$]'
if channel.find('ACC') != -1:
    unit = r'Acceleration [$m/s^2$]'
elif channel.find('MIC') != -1:
    unit = 'Sound [Pa]'

# Get data from frame files
    
sources = mylib.GetFilelist(gpsstart,gpsend)

data = TimeSeries.read(sources,channel,format='gwf.lalframe',start=int(gpsstart),end=int(gpsend))

if whitening:
    white = data.whiten(fftlength=fft,overlap=ol)
    whitespectrogram = white.spectrogram(1,fftlength=fft,overlap=ol)
    
    sgplot=whitespectrogram.plot(figsize = (12, 8))
else:
    spectrogram = data.spectrogram(1,fftlength=fft,overlap=ol)
    sgplot=spectrogram.plot

ax = sgplot.gca()
ax.set_ylabel('Frequency [Hz]')
ax.set_title(latexchname)

if whitening:
    pass
else:
    ax.set_yscale('log')

sgplot.add_colorbar(cmap='YlGnBu_r',label='Arbitrary')

if lflag:
    ldata = TimeSeries.read(sources,lchannel,format='gwf.lalframe',start=int(gpsstart),end=int(gpsend))
    locked = ldata == lnumber
    flag = locked.to_dqflag(name = '', label = llabel, round = True)
    sgplot.add_state_segments(flag)
else:
    pass
if whitening:
    fname = outdir + '/' + channel + '_whiteningspectrogram_'+ gpsstart + '_' + gpsend +'_' + index +'.png'
else:
    fname = outdir + '/' + channel + '_spectrogram_'+ gpsstart + '_' + gpsend +'_' + index +'.png'

sgplot.savefig(fname)

sgplot.clf()
sgplot.close()

print(fname)
print('Successfully finished !')
