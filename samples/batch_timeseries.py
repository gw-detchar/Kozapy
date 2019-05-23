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

#  argument processing
import argparse

parser = argparse.ArgumentParser(description='Make coherencegram.')
parser.add_argument('-o','--outdir',help='output directory.',default='result')
parser.add_argument('-c','--channel',help='channel list.',nargs='*',required=True)
parser.add_argument('-s','--gpsstart',help='GPS starting time.',required=True)
parser.add_argument('-e','--gpsend',help='GPS ending time.',required=True)
parser.add_argument('-d','--datatype',help='Data type. Options are minute(default), second, and full.',default='minute',choices=['minute','second','full'])
parser.add_argument('-i','--index',help='It will be added to the output file name.',default='test')
parser.add_argument('-p','--lposition',help='Legend position. Choice is \'br\'(bottom right), \'bl\'(bottom left), \'tr\'(top right), or \'tl\'(top left), .',default='tr',choices=['br','bl','tr','tl'])

parser.add_argument('-l','--lchannel',help='Make locked segment bar plot.',default='')
parser.add_argument('--llabel',help='Label of the locked segment bar plot.',default='')
parser.add_argument('-n','--lnumber',help='The requirement for judging locked. lchannel==lnumber will be used as locked.',default=99,type=int)
parser.add_argument('-k','--kamioka',help='Flag to run on Kamioka server.',action='store_true')

# define variables
args = parser.parse_args()
outdir = args.outdir

channel = args.channel

latexchnames = [c.replace('_','\_') for c in channel]

gpsstart = args.gpsstart
gpsend = args.gpsend

datatype = args.datatype
index = args.index

lposition=args.lposition

lchannel = args.lchannel
lnumber = args.lnumber
llabel = args.llabel

kamioka = args.kamioka

# If lflag is True, locked segments is plotted. 
lflag = bool(lchannel)

# Get data from frame files
if kamioka:
    if datatype == 'minute':
        sources = mylib.GetMtrendFilelist_Kamioka(gpsstart,gpsend)
    elif datatype == 'second':
        sources = mylib.GetStrendFilelist_Kamioka(gpsstart,gpsend)
    elif datatype == 'full':
        sources = mylib.GetFilelist_Kamioka(gpsstart,gpsend)
else:
    if datatype == 'minute':
        sources = mylib.GetMtrendFilelist(gpsstart,gpsend)
    elif datatype == 'second':
        sources = mylib.GetStrendFilelist(gpsstart,gpsend)
    elif datatype == 'full':
        sources = mylib.GetFilelist(gpsstart,gpsend)

unit = r'Amplitude [$\sqrt{\mathrm{Hz}^{-1}}$]'
if channel[0].find('ACC') != -1:
    unit = r'Acceleration [$m/s^2$]'
elif channel[0].find('MIC') != -1:
    unit = 'Sound [Pa]'

data = TimeSeriesDict.read(sources,channel,format='gwf.lalframe',start=int(gpsstart),end=int(gpsend))
plot=data.plot(figsize = (12, 8))

ax = plot.gca()
ax.set_ylabel(unit)
#ax.set_yscale('log')
ax.legend(latexchnames,bbox_to_anchor = mylib.GetBBTA(lposition),loc=mylib.Getloc(lposition),borderaxespad=1)

if lflag:
    ldata = TimeSeries.read(sources,lchannel,format='gwf.lalframe',start=int(gpsstart),end=int(gpsend))
    locked = ldata == lnumber
    flag = locked.to_dqflag(name = '', label = llabel, round = True)
    plot.add_state_segments(flag)
else:
    pass

fname = outdir + '/' + channel[0] + '_timeseries_'+ gpsstart + '_' + gpsend +'_' + index +'.png'
plot.savefig(fname)

plot.clf()
plot.close()

print(fname)
print('Successfully finished !')
