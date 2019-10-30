'''Make timeseries.
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

#pl.rcParams['figure.figsize'] = 12, 8
pl.rcParams['font.size'] = 16
pl.rcParams['font.family'] = 'Verdana'
#pl.rcParams['mathtext.fontset'] = 'stixsans'

#  argument processing
import argparse

parser = argparse.ArgumentParser(description='Make coherencegram.')
parser.add_argument('-o','--outdir',help='output directory.',default='/tmp')
parser.add_argument('-c','--channel',help='channel list.',nargs='*',required=True)
parser.add_argument('-s','--gpsstart',help='GPS starting time.',required=True)
parser.add_argument('-e','--gpsend',help='GPS ending time.',required=True)
parser.add_argument('-d','--datatype',help='Data type. Options are minute(default), second, and full.',default='minute',choices=['minute','second','full'])
parser.add_argument('-w','--whitening',help='Apply whitening.',action='store_true')
parser.add_argument('-m','--margin',help='Marginal time for better whitening.',type=float,default=2.)
parser.add_argument('-f','--fftlength',help='FFT length for whitening.',type=float,default=1.)
parser.add_argument('-i','--index',help='It will be added to the output file name.',default='test')
parser.add_argument('--nolegend',help='Flag to make legend or not.',action='store_false')
parser.add_argument('-p','--lposition',help='Legend position. Choice is \'br\'(bottom right), \'bl\'(bottom left), \'tr\'(top right), or \'tl\'(top left), .',default='tr',choices=['br','bl','tr','tl'])
parser.add_argument('-t','--title',help='Plot title.',default='')
parser.add_argument('--dpi',help='Plot resolution. dot per inch.',type=int,default=100)

parser.add_argument('-l','--lchannel',help='Make locked segment bar plot.',default='')
parser.add_argument('--llabel',help='Label of the locked segment bar plot.',default='')
parser.add_argument('-n','--lnumber',help='The requirement for judging locked. lchannel==lnumber will be used as locked.',default=99,type=int)

parser.add_argument('-k','--kamioka',help='Flag to run on Kamioka server.',action='store_true')

# define variables
args = parser.parse_args()

kamioka = args.kamioka

outdir = args.outdir

channel = args.channel

whitening=args.whitening
margin=args.margin

latexchnames = args.channel

if kamioka:
    latexchnames = [c.replace('_','\_') for c in channel]
    title = args.title.replace('_','\_')
else:
    latexchnames = args.channel
    title = args.title
gpsstart = args.gpsstart
gpsend = args.gpsend

gpsstartmargin=gpsstart
gpsendmargin=gpsend

if whitening:
    gpsstartmargin=str(float(gpsstart)-margin)
    gpsendmargin=str(float(gpsend)+margin)


fft=args.fftlength
ol=fft/2.  #  overlap in FFTs.

datatype = args.datatype
index = args.index

legend=args.nolegend
lposition=args.lposition
dpi=args.dpi
lchannel = args.lchannel
lnumber = args.lnumber
llabel = args.llabel

# If lflag is True, locked segments is plotted. 
lflag = bool(lchannel)

# Get data from frame files

if kamioka:
    if datatype == 'minute':
        sources = mylib.GetMtrendFilelist_Kamioka(gpsstartmargin,gpsendmargin)
    elif datatype == 'second':
        sources = mylib.GetStrendFilelist_Kamioka(gpsstartmargin,gpsendmargin)
    elif datatype == 'full':
        sources = mylib.GetFilelist_Kamioka(gpsstartmargin,gpsendmargin)
else:
    if datatype == 'minute':
        sources = mylib.GetMtrendFilelist(gpsstartmargin,gpsendmargin)
    elif datatype == 'second':
        sources = mylib.GetStrendFilelist(gpsstartmargin,gpsendmargin)
    elif datatype == 'full':
        sources = mylib.GetFilelist(gpsstartmargin,gpsendmargin)

#unit = r'Amplitude [$\sqrt{\mathrm{Hz}^{-1}}$]'
unit = ''
if channel[0].find('ACC') != -1:
    unit = r'Acceleration [m/s^2]'
elif channel[0].find('MIC') != -1:
    unit = 'Sound [Pa]'

data = TimeSeriesDict.read(sources,channel,format='gwf.lalframe',start=float(gpsstartmargin),end=float(gpsendmargin))


for d in data:
    if whitening:
        data[d] = data[d].whiten(fftlength=fft,overlap=ol)
        data[d] = data[d].crop(float(gpsstart),float(gpsend))

    if len(data[d]) > 10000:
        rate = 10000./len(data[d])/data[d].dt
        data[d] = data[d].resample(rate)
        print("The sample rate*duration is over capacity. Down sampled to rate of "+str(rate)+".")

#plot=data.plot(figsize = (12, 8))
plot=data.plot()

ax = plot.gca()
ax.set_title(title)
ax.set_ylabel(unit)
#ax.set_yscale('log')
if legend:
    ax.legend(latexchnames,bbox_to_anchor = mylib.GetBBTA(lposition),loc=mylib.Getloc(lposition),borderaxespad=1)

if lflag:
#    ldata = TimeSeries.read(sources,lchannel,format='gwf.lalframe',start=int(tmpgpsstart),end=int(tmpgpsend))
    ldata = TimeSeries.read(sources,lchannel,format='gwf.lalframe',start=float(gpsstart),end=float(gpsend))
    locked = ldata == lnumber
    flag = locked.to_dqflag(name = '', label = llabel)
    plot.add_state_segments(flag)
else:
    pass

fname = outdir + '/' + channel[0] + '_timeseries_'+ gpsstart + '_' + gpsend +'_' + index +'.png'
# dpi = dot per inch. It is figure resolution. default is 80 ?

plot.savefig(fname,dpi=dpi) #,bbox_inches="tight")

plot.clf()
plot.close()

print(fname)
print('Successfully finished !')
