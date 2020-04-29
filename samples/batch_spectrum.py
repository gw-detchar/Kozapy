'''Make spectrums. If several channels or times are given, they are overlaid.
'''

__author__ = "Chihiro Kozakai"

import os
import matplotlib
matplotlib.use('Agg')  # this line is required for the batch job before importing other matplotlib modules.     

import subprocess
import glob
from gwpy.timeseries import TimeSeries
from gwpy.frequencyseries import FrequencySeries
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
parser.add_argument('--ymin',help='Yaxis minimum limit.',type=float,default=-1)
parser.add_argument('--ymax',help='Yaxis maximum limit.',type=float,default=-1)
parser.add_argument('--fmin',help='Frequency minimum limit.',type=float,default=-1)
parser.add_argument('--fmax',help='Frequency maximum limit.',type=float,default=-1)
parser.add_argument('-r','--reffile',help='Reference FrequencySeries file.',default=None)
parser.add_argument('--reftitle',help='Reference FrequencySeries title.',nargs=1, default='Reference')
parser.add_argument('--makefile',help='Reference FrequencySeries output file name.',action='store_true')
parser.add_argument('--ll',help='Flag to use low latency files. Valid only in Kashiwa.',action='store_true')
parser.add_argument('-g','--geo',help='Flag to use GEO files. Valid only in Kashiwa.',action='store_true')
# GEO h(t) channel G1:DER_DATA_H 16384
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
reffile=args.reffile
reftitle=args.reftitle
makefile=args.makefile

dpi=args.dpi
kamioka = args.kamioka
ll = args.ll
GEO = args.geo

ymin = args.ymin
ymax = args.ymax
fmin = args.fmin
fmax = args.fmax

# Loop over channels and gps times.
isFirst = True
legend = []

#legend title
if title != None:
    legend=title

    if reffile != None:
        legend.append(reftitle)

#color list
color=["orange","royalblue","limegreen","red","gold","magenta","lightskyblue","black","aquamarine","darkorchid","saddlebrown","salmon","greenyellow","navy"]
colorindex=0

for gpsstart,gpsend in zip(gpsstarts,gpsends):

    if kamioka:
        sources = mylib.GetFilelist_Kamioka(gpsstart,gpsend)
    elif ll:
        sources = mylib.GetLLFilelist(gpsstart,gpsend)
    elif GEO:
        sources = mylib.GetGeoFilelist(gpsstart,gpsend)
    else:
        sources = mylib.GetFilelist(gpsstart,gpsend)

    datas = TimeSeriesDict.read(sources,channels,format='gwf.lalframe',start=float(gpsstart),end=float(gpsend))

    for channel in channels:
        data = datas[channel]
        #unit = r'Amplitude [$\sqrt{\mathrm{Hz}^{-1}}$]'
        unit = 'Amplitude [1/rHz]'
        if channel.find('ACC_') != -1:
            #unit = r'Acceleration [$m/s^2$ $/ \sqrt{\mathrm{Hz}^{-1}}$]'
            unit = 'Acceleration [m/s^2/rHz]'
        elif channel.find('MIC_') != -1:
            #unit = r'Sound [Pa $/ \sqrt{\mathrm{Hz}^{-1}}$]'
            unit = 'Sound [Pa/rHz]'
        elif channel.find('DARM_DISPLACEMENT_DQ') != -1:
            #unit = 'Amplitude [nm/rHz]'
            unit = 'Strain [/rHz]'

        
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

        if sum(spectrum.value) == 0.:
            print("Warning !!! : The data is constant. Plot is not provided.")

            # following is for successcheck.sh to take it as OK. 
            if kamioka:
                print("/users/DET/tools/GlitchPlot/Script/Kozapy/samples/dummy")
            else:
                print("/home/chihiro.kozakai/detchar/analysis/code/gwpy/Kozapy/samples/dummy")
            print('Successfully finished !')

            exit()

        if channel == "K1:CAL-CS_PROC_DARM_DISPLACEMENT_DQ":
            spectrum = spectrum.filter([10]*4,[1]*4,1e-9/3000.) * 1e-4 #1e-9/3000.*1e-4)

        if makefile:
            spectrum.write(outdir + '/' + channel + '_spectrum_' + gpsstart +  '_' + index + '.hdf5')

        if isFirst:           
            fplot=spectrum.plot(figsize = (12, 8),color=color[colorindex])
            ax = fplot.gca()
            ax.set_ylabel(unit)
            ax.set_yscale('log')
            ax.set_title(mylib.GetTitlefromLegend(ltype,gpsstart,gpsend,channel)+" Spectrum")
            
            if ymin > 0 and ymax > 0:
                ax.set_ylim(ymin,ymax)
            if fmin > 0 and fmax > 0:
                ax.set_xlim(fmin,fmax)

            isFirst = False

        else:
            colorindex+=1
            ax.plot(spectrum,color=color[colorindex])

        if title == None:
            legend+=(mylib.GetLegend(ltype,gpsstart,gpsend,channel))

if reffile:
    ref = FrequencySeries.read(reffile)
    ax.plot(ref,color=color[colorindex+1])
    
ax.legend(legend,bbox_to_anchor = mylib.GetBBTA(lposition),loc=mylib.Getloc(lposition),borderaxespad=1)

fname = outdir + '/' + channel + '_spectrum_' + gpsstart +  '_' + index + '.png'
print(fname)
fplot.savefig(fname,dpi=dpi)
fplot.clf()
fplot.close()


print('Successfully finished !')
