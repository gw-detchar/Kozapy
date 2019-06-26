'''
Provide summary of lock state.
'''

__author__ = "Chihiro Kozakai"

import argparse
import matplotlib
matplotlib.use('Agg')  # this line is required for the batch job before importing other matplotlib modules.
from gwpy.segments import DataQualityFlag
from mylib import mylib

#  argument processing


parser = argparse.ArgumentParser(description='Make lock segment bars.')
parser.add_argument('-o','--outdir',help='output directory.',default='result')
parser.add_argument('-s','--gpsstart',help='GPS starting time.',required=True)
parser.add_argument('-e','--gpsend',help='GPS ending time.',required=True)
parser.add_argument('-t','--triggertime',help='trigger starting time.',type=float,required=True)
parser.add_argument('-d','--triggerduration',help='trigger dration.',type=float,required=True)
parser.add_argument('-i','--index',help='It will be added to the output file name.',default='test')
parser.add_argument('-k','--kamioka',help='Flag to run on Kamioka server.',action='store_true')

# define variables
args = parser.parse_args()
outdir = args.outdir
gpsstart = args.gpsstart
gpsend = args.gpsend
triggertime = args.triggertime
duration = args.triggerduration
index = args.index
kamioka = args.kamioka

trigger = DataQualityFlag(name="Trigger",known=[(float(gpsstart),float(gpsend))],active=[(triggertime,triggertime+duration)])
xarm = mylib.GetDQFlag(gpsstart,gpsend,config="xarm",kamioka=kamioka)
LSC = mylib.GetDQFlag(gpsstart,gpsend,config="LSC",kamioka=kamioka)
IMC = mylib.GetDQFlag(gpsstart,gpsend,config="IMC",kamioka=kamioka)
    
print(trigger)
plot = trigger.plot()
ax = plot.gca()
ax.plot(xarm)
ax.plot(LSC)
ax.plot(IMC)

plot.savefig(outdir+"/lockedsegments_"+index+".png")
