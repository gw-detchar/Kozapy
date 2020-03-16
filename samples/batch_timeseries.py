'''Make timeseries.
'''

__author__ = "Chihiro Kozakai"

import os
import pprint
import numpy as np
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
#parser.add_argument('-b','--bandpass',help='Apply band pass filter. If blow or bhigh is not given, blow is determined by given time duration and bhigh is determined by sampling frequency.',action='store_true')
parser.add_argument('--blow',help='Low pass cutoff frequency.',type=float,default=-1) #40)
parser.add_argument('--bhigh',help='High pass cutoff frequency.',type=float,default=-1) #1000)

parser.add_argument('-i','--index',help='It will be added to the output file name.',default='test')
parser.add_argument('--nolegend',help='Flag to make legend or not.',action='store_false')
parser.add_argument('-p','--lposition',help='Legend position. Choice is \'br\'(bottom right), \'bl\'(bottom left), \'tr\'(top right), or \'tl\'(top left), .',default='tr',choices=['br','bl','tr','tl'])
parser.add_argument('-t','--title',help='Plot title.',default='')
parser.add_argument('--dpi',help='Plot resolution. dot per inch.',type=int,default=100)

parser.add_argument('-l','--lchannel',help='Make locked segment bar plot.',default='')
parser.add_argument('--llabel',help='Label of the locked segment bar plot.',default='')
parser.add_argument('-n','--lnumber',help='The requirement for judging locked. lchannel==lnumber will be used as locked.',default=99,type=int)

parser.add_argument('-k','--kamioka',help='Flag to run on Kamioka server.',action='store_true')
parser.add_argument('--ll',help='Flag to use low latency files. Valid only in Kashiwa.',action='store_true')

# define variables
args = parser.parse_args()

kamioka = args.kamioka
ll = args.ll

outdir = args.outdir

channel = args.channel

whitening=args.whitening
margin=args.margin

#bandpass = args.bandpass
blow = args.blow
bhigh = args.bhigh

if blow > 0:
    lowpass = True
else:
    lowpass = False

if bhigh > 0:
    highpass = True
else:
    highpass = False

latexchnames = args.channel

if kamioka:
    latexchnames = [c.replace('_','\_') for c in channel]
    title = args.title.replace('_','\_')
else:
    latexchnames = args.channel
    title = args.title


gpsstart = args.gpsstart
gpsend = args.gpsend

#gpsstartmargin=gpsstart
#gpsendmargin=gpsend

# To keep small number, tricky method is used. Commented out expression is what intended. 
#gpsstartmargin=gpsstart-margin
#gpsendmargin=gpsend+margin

if '.' in gpsstart:
    smallstart='.'+gpsstart.split('.')[1]
else:
    smallstart=''
if '.' in gpsend:
    smallend='.'+gpsend.split('.')[1]
else:
    smallend=''
#gpsstartmargin=str(int(int(float(gpsstart))-margin))+'.'+gpsstart.split('.')[1]
#gpsendmargin=str(int(int(float(gpsend))+margin))+'.'+gpsend.split('.')[1]
gpsstartmargin=str(int(int(float(gpsstart))-margin))+smallstart
gpsendmargin=str(int(int(float(gpsend))+margin))+smallend

#if whitening or bandpass:
#    gpsstartmargin=str(float(gpsstart)-margin)
#    gpsendmargin=str(float(gpsend)+margin)


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
lflag = bool(llabel)

# Get data from frame files

if kamioka:
    if datatype == 'minute':
        sources = mylib.GetMtrendFilelist_Kamioka(gpsstartmargin,gpsendmargin)
    elif datatype == 'second':
        sources = mylib.GetStrendFilelist_Kamioka(gpsstartmargin,gpsendmargin)
    elif datatype == 'full':
        sources = mylib.GetFilelist_Kamioka(gpsstartmargin,gpsendmargin)
elif ll:
    sources = mylib.GetLLFilelist(gpsstartmargin,gpsendmargin)
else:
    if datatype == 'minute':
        sources = mylib.GetMtrendFilelist(gpsstartmargin,gpsendmargin)
    elif datatype == 'second':
        sources = mylib.GetStrendFilelist(gpsstartmargin,gpsendmargin)
    elif datatype == 'full':
        sources = mylib.GetFilelist(gpsstartmargin,gpsendmargin)

#unit = r'Amplitude [$\sqrt{\mathrm{Hz}^{-1}}$]'
unit = ''
if channel[0].find('ACC_') != -1:
    unit = r'Acceleration [m/s^2]'
elif channel[0].find('MIC_') != -1:
    unit = 'Sound [Pa]'

data = TimeSeriesDict.read(sources,channel,format='gwf.lalframe',start=float(gpsstartmargin),end=float(gpsendmargin))

for d in data:
    done=False

    #while not done:

    tmp=data[d]
    if whitening:
        tmp = tmp.whiten(fftlength=fft,overlap=ol)

    #if bandpass:
        
    #    if 1./tmp.dt.value/4. < blow:
    #        print("Failed: bandpass frequency setting is too high, more than sampling rate / 4. ")
    #        exit()
    #    if 1./tmp.dt.value/4. < bhigh:
    #        bhigh = 1./tmp.dt.value/4.
    #    tmp = tmp.bandpass(blow,bhigh)
    if highpass:
        if 1./tmp.dt.value/4. < bhigh:
            bhigh = 1./tmp.dt.value/4.
        tmp = tmp.highpass(bhigh)

    if lowpass:
        if 1./tmp.dt.value/4. < blow:
             print("Caution !!! : bandpass frequency setting is too high, more than sampling rate / 4. Low pass is not applied. ")
             blow = "*"
             lowpass = False
             #exit()
        else:
            tmp = tmp.lowpass(blow)

    # below is to avoid buggy parameter choice.
    #if tmp.value[0] <= 10.*data[d].value[0] and not np.isnan(tmp.value[0]):
    #    done = True
    #elif bandpass:

    #    print("Band pass failed. blow = "+str(blow)+", bhigh = "+str(bhigh)+". To be retried with modified parameter. ") 
    #    bhigh = 32768./blow
        #if bhigh > 8192:
            #bhigh = 8191
    #    if bhigh > 1./data[d].dt.value/2.:
    #        bhigh = 1./data[d].dt.value/2. -1
    #    tmp=data[d]
    #    tmp = tmp.bandpass(blow,bhigh)
    #    if tmp.value[0] <= 10.*data[d].value[0] and not np.isnan(tmp.value[0]):
    #        print("Band pass frequency adjustment is done. blow = "+str(blow)+", bhigh = "+str(bhigh)) 
    #    else:
    #        print("Band pass frequency adjustment failed. blow = "+str(blow)+", bhigh = "+str(bhigh))
 
    if len(tmp) > 360000:
        rate = 360000./len(tmp)/tmp.dt
        tmp = tmp.resample(rate)
        print("The sample rate*duration is over capacity. Down sampled to rate of "+str(rate)+".")

    data[d] = tmp.crop(float(gpsstart),float(gpsend))
    
#if bandpass:
#    title += " bandpass ("+str(blow)+"-"+str(bhigh)+ "Hz)"
if lowpass and highpass:
    title += " bandpass ("+str(bhigh)+"-"+str(blow)+ "Hz)"
elif lowpass:
    title += " lowpass ("+str(blow)+ "Hz)"
elif highpass:
    title += " highpass ("+str(bhigh)+ "Hz)"

#plot=data.plot(figsize = (12, 8))
plot=data.plot()

ax = plot.gca()
ax.set_title(title)
ax.set_ylabel(unit)
#ax.set_yscale('log')

if whitening:
    latexchnames = [c + " whitening" for c in latexchnames]

if lowpass and highpass:
    latexchnames = [c + " bandpass" for c in latexchnames]
elif lowpass:
    latexchnames = [c + " lowpass" for c in latexchnames]
elif highpass:
    latexchnames = [c + " highpass" for c in latexchnames]

if legend:
    ax.legend(latexchnames,bbox_to_anchor = mylib.GetBBTA(lposition),loc=mylib.Getloc(lposition),borderaxespad=1)

if lflag:
    flag = mylib.GetDQFlag(gpsstart,gpsend,config=llabel,kamioka=kamioka)

    if flag == None:
        ldata = TimeSeries.read(sources,lchannel,format='gwf.lalframe',start=float(gpsstart),end=float(gpsend))
        locked = ldata == lnumber
        flag = locked.to_dqflag(name = '', label = llabel)

    plot.add_state_segments(flag)
else:
    pass

option=""
if whitening:
    option += "whitened_"
#if bandpass:
#    option += "bandpass_"
if lowpass and highpass:
    option += "bandpass_"
if lowpass:
    option += "lowpass_"
if highpass:
    option += "highpass_"
fname = outdir + '/' + channel[0] + '_timeseries_' + option + gpsstart + '_' + gpsend +'_' + index +'.png'


# dpi = dot per inch. It is figure resolution. default is 80 ?

plot.savefig(fname,dpi=dpi) #,bbox_inches="tight")

plot.clf()
plot.close()

print(fname)
print('Successfully finished !')
