'''Make coherencegram.
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
from gwpy.plot import BodePlot
from mylib import mylib


from matplotlib import pylab as pl
pl.rcParams['font.size'] = 16
pl.rcParams['font.family'] = 'Verdana'

#  argument processing
import argparse

parser = argparse.ArgumentParser(description='Make coherencegram.')
parser.add_argument('-o','--outdir',help='output directory.',default='/tmp')
#parser.add_argument('-r','--refchannel',help='main reference channel.',required=True)
parser.add_argument('-r','--refchannel',help='main reference channel.',default='K1:IMC-CAV_TRANS_OUT_DQ')
#parser.add_argument('-c','--channel',help='compared channel.',required=True)
parser.add_argument('-c','--channel',help='compared channel.',default='K1:CAL-CS_PROC_C00_STRAIN_DBL_DQ')
#parser.add_argument('-s','--gpsstart',help='GPS starting time.',required=True)
parser.add_argument('-s','--gpsstart',help='GPS starting time.',default='1255475898')
#parser.add_argument('-e','--gpsend',help='GPS ending time.',required=True)
parser.add_argument('-e','--gpsend',help='GPS ending time.',default='1255476498')
parser.add_argument('-f','--fftlength',help='FFT length.',type=float,default=1.)
parser.add_argument('--fmin',help='Frequency minimum limit.',type=float,default=-1.)
parser.add_argument('--fmax',help='Frequency maximum limit.',type=float,default=8000.)
parser.add_argument('--stride',help='Stride of the coherencegram.',type=float,default=10.)
parser.add_argument('-i','--index',help='It will be added to the output file name.',default='test')

parser.add_argument('-l','--lchannel',help='Make locked segment bar plot.',default='')
parser.add_argument('--llabel',help='Label of the locked segment bar plot.',default='')
parser.add_argument('-n','--lnumber',help='The requirement for judging locked. lchannel==lnumber will be used as locked.',default=99,type=int)
parser.add_argument('-k','--kamioka',help='Flag to run on Kamioka server.',action='store_true')

parser.add_argument('--dpi',help='Plot resolution. dot per inch.',type=int,default=100)
# define variables
args = parser.parse_args()

kamioka = args.kamioka

outdir=args.outdir

refchannel=args.refchannel
channel=args.channel
if kamioka:
    latexchname = channel.replace('_','\_')
    latexrefchname = refchannel.replace('_','\_')
else:
    latexchname = channel
    latexrefchname = refchannel

gpsstart=args.gpsstart
gpsend=args.gpsend
index=args.index
stride=args.stride
fft=args.fftlength
ol=fft/2.  #  overlap in FFTs. 

fmin=args.fmin
fmax=args.fmax

lchannel = args.lchannel
lnumber = args.lnumber
llabel = args.llabel

dpi=args.dpi
    
# Get data from frame files
if kamioka:    
    sources = mylib.GetFilelist_Kamioka(gpsstart,gpsend)
else:
    sources = mylib.GetFilelist(gpsstart,gpsend)
    
channels = [refchannel, channel]

data = TimeSeriesDict.read(sources,channels,format='gwf.lalframe',start=float(gpsstart),end=float(gpsend))


ref = data[refchannel]
com = data[channel]

#if fft < ref.dt.value:
#    fft=2*ref.dt.value
#    ol=fft/2.  #  overlap in FFTs.                        
#    stride=2*fft
#    print("Given fft/stride was bad against the sampling rate. Automatically set to:")
#    print("fft="+str(fft))
#    print("ol="+str(ol))
#    print("stride="+str(stride))
#if fft < com.dt.value:
#    fft=2*com.dt.value
#    ol=fft/2.  #  overlap in FFTs.                        
#    stride=2*fft
#    print("Given fft/stride was bad against the sampling rate. Automatically set to:")
#    print("fft="+str(fft))
#    print("ol="+str(ol))
#    print("stride="+str(stride))

reffft = ref.average_fft(fft, ol, window='hanning')
comfft = com.average_fft(fft, ol, window='hanning')

size = min(reffft.size, comfft.size)
tf = comfft[:size] / reffft[:size]

plot = BodePlot(tf)
plot.maxes.set_title('Transfer function')
#coh = ref.coherence_spectrogram(com,stride,fftlength=fft,overlap=ol)

# The time axis of coherencegram seems buggy in this version. Temporal fix is needed.
#coh.dx = stride

#cohplot=coh.plot(figsize = (12, 8),vmin=0.,vmax=1.)
#ax = cohplot.gca()
ax = plot.gca()
#ax.set_ylabel('Frequency [Hz]')
#ax.set_yscale('log')
#ax.set_title(latexrefchname + ' ' + latexchname)

#if fmin < 0:
#    fmin = 0.8/fft
#ax.set_ylim(fmin,fmax)

#cohplot.add_colorbar(cmap='YlGnBu_r',label='Coherence')

fname = outdir + '/' + refchannel + '_' + channel + '_TF_'+ gpsstart + '_' + gpsend +'_' + index +'.png'
plot.savefig(fname,dpi=dpi)

plot.clf()
plot.close()

print(fname)
print('Successfully finished !')
