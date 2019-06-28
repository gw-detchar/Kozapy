'''Make q-transform plot.
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
parser.add_argument('-e','--gpsend',help='GPS ending time.',required=True)
parser.add_argument('-t','--time',help='Plot time duration.',type=float,default=None)

#parser.add_argument('-f','--fftlength',help='FFT length.',type=float,default=1.)
parser.add_argument('-i','--index',help='It will be added to the output file name.',default='test')

parser.add_argument('-l','--lchannel',help='Make locked segment bar plot.',default='')
parser.add_argument('--llabel',help='Label of the locked segment bar plot.',default='')
parser.add_argument('-n','--lnumber',help='The requirement for judging locked. lchannel==lnumber will be used as locked.',default=99,type=int)
parser.add_argument('-k','--kamioka',help='Flag to run on Kamioka server.',action='store_true')

# define variables
args = parser.parse_args()
outdir=args.outdir

channel=args.channel
latexchname = channel.replace('_','\_')

gpsstart=args.gpsstart
gpsend=args.gpsend
gpshalf=(float(gpsstart)+float(gpsend))/2.
time = args.time
if time == None:
    time=(float(gpsend)-float(gpsstart))/2.

index=args.index
#fft=args.fftlength
#ol=fft/2.  #  overlap in FFTs. 

lchannel=args.lchannel
lnumber=args.lnumber
llabel=args.llabel

lflag=bool(lchannel)

kamioka = args.kamioka
    
unit = "Normalized energy"

# Get data from frame files
if kamioka:
    sources = mylib.GetFilelist_Kamioka(gpsstart,gpsend)
else:
    sources = mylib.GetFilelist(gpsstart,gpsend)

data = TimeSeries.read(sources,channel,format='gwf.lalframe',start=float(gpsstart),end=float(gpsend))

maxf=1024
if maxf > 1./data.dt.value/4.:
    maxf=1./data.dt.value/4.

qgram = data.q_transform(outseg=[gpshalf-time,gpshalf+time])
# default parameter
#qrange=(4, 64), frange=(0, inf), gps=None, search=0.5, tres='<default>', fres='<default>', logf=False, norm='median', mismatch=0.2, outseg=None, whiten=True, fduration=2, highpass=None, **asd_kw 
plot=qgram.plot(figsize = (12, 8))

ax = plot.gca()
ax.set_ylabel('Frequency [Hz]')
ax.set_yscale('log')
ax.set_title(latexchname+" Q-transform")

plot.add_colorbar(cmap='YlGnBu_r',label="Normalized energy")
fname = outdir + '/' + channel + '_qtransform_'+ gpsstart + '_' + gpsend +'_' + index +'.png'

if lflag:
    ldata = TimeSeries.read(sources,lchannel,format='gwf.lalframe',start=float(gpsstart),end=float(gpsend))
    locked = ldata == lnumber
    flag = locked.to_dqflag(name = '', label = llabel, round = True)
    plot.add_state_segments(flag)
else:
    pass


plot.savefig(fname)

plot.clf()
plot.close()

print(fname)
print('Successfully finished !')
