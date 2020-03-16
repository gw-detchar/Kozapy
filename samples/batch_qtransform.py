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

from matplotlib import pylab as pl
pl.rcParams['font.size'] = 16
pl.rcParams['font.family'] = 'Verdana'

#  argument processing
import argparse

parser = argparse.ArgumentParser(description='Make coherencegram.')
parser.add_argument('-o','--outdir',help='output directory.',default='/tmp')
parser.add_argument('-c','--channel',help='channel.',required=True)
parser.add_argument('-s','--gpsstart',help='GPS starting time.',required=True)
parser.add_argument('-e','--gpsend',help='GPS ending time.',required=True)
parser.add_argument('-t','--time',help='Plot time duration.',type=float,default=None)
parser.add_argument('-f','--fmin',help='frequency range.',default=8 )
parser.add_argument('-q','--q',help='Q range.',type=float, default=-1 )

parser.add_argument('-i','--index',help='It will be added to the output file name.',default='test')

parser.add_argument('-l','--lchannel',help='Make locked segment bar plot.',default='')
parser.add_argument('--llabel',help='Label of the locked segment bar plot.',default='')
parser.add_argument('-n','--lnumber',help='The requirement for judging locked. lchannel==lnumber will be used as locked.',default=99,type=int)
parser.add_argument('-k','--kamioka',help='Flag to run on Kamioka server.',action='store_true')
parser.add_argument('--dpi',help='Plot resolution. dot per inch.',type=int,default=100)
parser.add_argument('--ll',help='Flag to use low latency files. Valid only in Kashiwa.',action='store_true')
# define variables
args = parser.parse_args()
outdir=args.outdir

channel=args.channel
#latexchname = channel.replace('_','\_')
latexchname = channel

gpsstart=args.gpsstart
gpsend=args.gpsend
fmin=args.fmin

dpi=args.dpi

#margin=40
margin=4

# Adjust margin to match the requirement from Q and fmin.
if (float(gpsend)-float(gpsstart)+2.*margin) * float(fmin) < float(args.q):
    margin = (float(args.q)/float(fmin)-(float(gpsend)-float(gpsstart))) /2.
    # for safety.
    margin+=1

gpsstartmargin=float(gpsstart)-margin
gpsendmargin=float(gpsend)+margin

qmin = 4
qmax = 100

if args.q > 0:
    qmin = int(args.q)
    qmax = int(args.q)

index=args.index

lchannel=args.lchannel
lnumber=args.lnumber
llabel=args.llabel

lflag=bool(llabel)

kamioka = args.kamioka
ll = args.ll
    
unit = "Normalized energy"

# Get data from frame files
if kamioka:
    sources = mylib.GetFilelist_Kamioka(gpsstartmargin,gpsendmargin)
elif ll:
    sources = mylib.GetLLFilelist(gpsstartmargin,gpsendmargin)
else:
    sources = mylib.GetFilelist(gpsstartmargin,gpsendmargin)

data = TimeSeries.read(sources,channel,format='gwf.lalframe',start=float(gpsstartmargin),end=float(gpsendmargin))

#maxf=1024
#if maxf > 1./data.dt.value/4.:
fmax=1./data.dt.value/4.

if data.value[0] == data.value[1]:
    print("Warning !!! : The data is constant. Plot is not provided.")

    # following is for successcheck.sh to take it as OK.                                         
    if kamioka:
        print("/users/DET/tools/GlitchPlot/Script/Kozapy/samples/dummy")
    else:
        print("/home/chihiro.kozakai/detchar/analysis/code/gwpy/Kozapy/samples/dummy")
        
    print('Successfully finished !')

    exit()

qgram = data.q_transform(outseg=[float(gpsstart),float(gpsend)],frange=(fmin,fmax),qrange=(qmin,qmax),gps=float(gpsstart)/2.+float(gpsend)/2.,logf=True)

#qgram = data.q_transform(outseg=[float(1267205087),float(1267205098)],frange=(fmin,fmax),qrange=(qmin,qmax),gps=float(gpsstart)/2.+float(gpsend)/2.,logf=True)

# default parameter
#qrange=(4, 64), frange=(0, inf), gps=None, search=0.5, tres='<default>', fres='<default>', logf=False, norm='median', mismatch=0.2, outseg=None, whiten=True, fduration=2, highpass=None, **asd_kw 
#plot=qgram.plot(figsize = (12, 8),vmin=0.,vmax=25.)

plot=qgram.plot(figsize = (12, 8))

ax = plot.gca()
ax.set_ylabel('Frequency [Hz]')
ax.set_yscale('log')
ax.set_title(latexchname+" Q-transform")

plot.add_colorbar(cmap='YlGnBu_r',label="Normalized energy",log=True, clim=[0.1,None])
fname = outdir + '/' + channel + '_qtransform_'+ gpsstart + '_' + gpsend +'_' + index +'.png'

if lflag:
    flag = mylib.GetDQFlag(float(gpsstart),float(gpsend),config=llabel, kamioka=kamioka)
    if flag == None:
        ldata = TimeSeries.read(sources,lchannel,format='gwf.lalframe',start=float(gpsstart),end=float(gpsend))
        locked = ldata == lnumber
        flag = locked.to_dqflag(name = '', label = llabel)
    plot.add_state_segments(flag)
else:
    pass

plot.savefig(fname,dpi=dpi)

plot.clf()
plot.close()

print(fname)
print('Successfully finished !')
