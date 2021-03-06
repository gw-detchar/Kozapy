'''
Provide summary of lock state.
'''

__author__ = "Chihiro Kozakai"

import argparse
import matplotlib
matplotlib.use('Agg')  # this line is required for the batch job before importing other matplotlib modules.
from gwpy.segments import DataQualityFlag
from mylib import mylib

from matplotlib import pylab as pl
pl.rcParams['font.size'] = 18
pl.rcParams['font.family'] = 'Verdana'
pl.rcParams['figure.subplot.left'] = 0.15


#  argument processing

parser = argparse.ArgumentParser(description='Make lock segment bars.')
parser.add_argument('-o','--outdir',help='output directory.',default='/tmp')
parser.add_argument('-s','--gpsstart',help='GPS starting time.',required=True)
parser.add_argument('-e','--gpsend',help='GPS ending time.',required=True)
parser.add_argument('-t','--triggertime',help='trigger starting time.',type=float,default=0)
parser.add_argument('-d','--triggerduration',help='trigger dration.',type=float,default=0)
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

#trigger = DataQualityFlag(name="Trigger",known=[(float(gpsstart),float(gpsend))],active=[(triggertime,triggertime+duration)])
#xarm = mylib.GetDQFlag(gpsstart,gpsend,config="xarm",kamioka=kamioka)
#LSC = mylib.GetDQFlag(gpsstart,gpsend,config="LSC",kamioka=kamioka)
#FPMI = mylib.GetDQFlag(gpsstart,gpsend,config="FPMI",kamioka=kamioka)
Observation = mylib.GetDQFlag(gpsstart,gpsend,config="Observation",kamioka=kamioka)
IFO = mylib.GetDQFlag(gpsstart,gpsend,config="IFO",kamioka=kamioka)
IMC = mylib.GetDQFlag(gpsstart,gpsend,config="IMC",kamioka=kamioka)
PMC = mylib.GetDQFlag(gpsstart,gpsend,config="PMC",kamioka=kamioka)
FSS = mylib.GetDQFlag(gpsstart,gpsend,config="FSS",kamioka=kamioka)
ISS = mylib.GetDQFlag(gpsstart,gpsend,config="ISS",kamioka=kamioka)
#DAQ = mylib.GetDQFlag(gpsstart,gpsend,config="DAQ",kamioka=kamioka)
#MICH = mylib.GetDQFlag(gpsstart,gpsend,config="MICH",kamioka=kamioka)
trigger = DataQualityFlag(name="Trigger",known=IFO.known,active=[(triggertime,triggertime+duration)])
    
untriggered = ~trigger
plot = untriggered.plot(figsize = (12,8))
ax = plot.gca()
ax.set_title("Interferometer state summary")
#ax.plot(LSC)
#ax.plot(FPMI)
ax.plot(Observation)
ax.plot(IFO)
#ax.plot(xarm)
#ax.plot(MICH)
ax.plot(ISS)
ax.plot(IMC)
ax.plot(PMC)
ax.plot(FSS)
#ax.plot(DAQ)
ax.set_xlim(IFO.known[0][0],IFO.known[0][1])

fname = outdir+"/lockedsegments_"+index+".png"
plot.savefig(fname,dpi=50)

print(fname)
print('Successfully finished !')
