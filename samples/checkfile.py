import glob
from gwpy.timeseries import TimeSeries
from gwpy.timeseries import TimeSeriesDict
from matplotlib import pylab as pl
from gwpy.detector import Channel

gpsstart = '1229044418'
gpsend = '1230044418'

sources = []

for i in range(int(gpsstart[0:5]),int(gpsend[0:5])+1):
    dir = '/data/full/' + str(i) + '/*'
    source = glob.glob(dir)
    sources.extend(source)

sources.sort()

u = ''
fname = './' + gpsstart + '-' + gpsend + '.txt'
f = open(fname, mode='w')

for x in sources:
 
    if u == '':
        u = x

    space = int(x[24:34])-int(u[24:34])

    if int(x[24:34])<(int(gpsstart)-32):
        pass
    elif int(x[24:34])>int(gpsend):
        break
    elif space != 32:
        print('Data is missing !')
        print(x,u)
        #print(int(x[24:34])-int(u[24:34]))
        missing = int(u[24:34])
        
        while space != 32:
            missing += 32 
            f.write('\n'+ str(missing))
            space -= 32
    u = x

f.close()
print('missing file is written in ' + fname)
