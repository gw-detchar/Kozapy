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
parser.add_argument('-w','--whitening',help='Apply whitening.',action='store_true')

parser.add_argument('-f','--fftlength',help='FFT length.',type=float,default=1.)
parser.add_argument('--stride',help='Stride of the coherencegram.',type=float,default=10.)
parser.add_argument('-i','--index',help='It will be added to the output file name.',default='test')

parser.add_argument('-l','--lchannel',help='Make locked segment bar plot.',default='')
parser.add_argument('--llabel',help='Label of the locked segment bar plot.',default='')
parser.add_argument('-n','--lnumber',help='The requirement for judging locked. lchannel==lnumber will be used as locked.',default=99,type=int)
parser.add_argument('-k','--kamioka',help='Flag to run on Kamioka server.',action='store_true')

# define variables
args = parser.parse_args()
outdir=args.outdir

whitening=args.whitening

channel=args.channel
latexchname = channel.replace('_','\_')
if whitening:
    latexchname += " whitened"
latexchname += " spectrogram"
gpsstart=args.gpsstart
gpsend=args.gpsend



index=args.index
stride=args.stride
fft=args.fftlength
ol=fft/2.  #  overlap in FFTs. 

print("fft="+str(fft))
print("ol="+str(ol))
print("stride="+str(stride))
lchannel=args.lchannel
lnumber=args.lnumber
llabel=args.llabel

lflag=bool(lchannel)

kamioka = args.kamioka

if fft*2. > stride:
    print('Warning: stride is shorter than fft length. Set stride=fft*2.')
    stride=fft*2.
    
unit = r'Amplitude [$\sqrt{\mathrm{Hz}^{-1}}$]'
if channel.find('ACC') != -1:
    unit = r'Acceleration [$m/s^2$]'
elif channel.find('MIC') != -1:
    unit = 'Sound [Pa]'

# Get data from frame files
if kamioka:
    sources = mylib.GetFilelist_Kamioka(gpsstart,gpsend)
else:
    sources = mylib.GetFilelist(gpsstart,gpsend)

data = TimeSeries.read(sources,channel,format='gwf.lalframe',start=float(gpsstart),end=float(gpsend))

if fft <= data.dt.value:
    fft=2*data.dt.value
    ol=fft/2.  #  overlap in FFTs. 
    stride=2*fft
    print("Given fft/stride was bad against the sampling rate. Automatically set to:")
    print("fft="+str(fft))
    print("ol="+str(ol))
    print("stride="+str(stride))

if whitening:
    print('Whitening applied.')
    white = data.whiten(fftlength=fft,overlap=ol)
    whitespectrogram = white.spectrogram(stride,fftlength=fft,overlap=ol) ** (1/2.)

    sgplot=whitespectrogram.plot(figsize = (12, 8))
else:
    print('Not whitening applied.')
    spectrogram = data.spectrogram(stride,fftlength=fft,overlap=ol) ** (1/2.)
    sgplot=spectrogram.plot(figsize = (12, 8),norm='log')

ax = sgplot.gca()
ax.set_ylabel('Frequency [Hz]')
ax.set_yscale('log')
ax.set_title(latexchname)
y_min = 0.8/fft
ax.set_ylim(y_min,1000)

if whitening:
    sgplot.add_colorbar(cmap='YlGnBu_r',label='Arbitrary')
    fname = outdir + '/' + channel + '_whiteningspectrogram_'+ gpsstart + '_' + gpsend +'_' + index +'.png'
else:
    sgplot.add_colorbar(cmap='YlGnBu_r',label=unit,log=True)
    fname = outdir + '/' + channel + '_spectrogram_'+ gpsstart + '_' + gpsend +'_' + index +'.png'

if lflag:
    ldata = TimeSeries.read(sources,lchannel,format='gwf.lalframe',start=float(gpsstart),end=float(gpsend))
    locked = ldata == lnumber
    flag = locked.to_dqflag(name = '', label = llabel, round = True)
    sgplot.add_state_segments(flag)
else:
    pass


sgplot.savefig(fname)

sgplot.clf()
sgplot.close()

print(fname)
print('Successfully finished !')
