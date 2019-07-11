import glob
from gwpy.timeseries import TimeSeries

def GetFilelist(gpsstart,gpsend):
    '''                                                                           
    This function gives full data frame file list.                                
    '''
    ingpsstart=float(gpsstart)
    ingpsend=float(gpsend)

    gpsstart=str(int(float(gpsstart)))
    gpsend=str(int(float(gpsend)))

    sources = []

    for i in range(int(gpsstart[0:5]),int(gpsend[0:5])+1):
        dir = '/data/full/' + str(i) + '/*'
        source = glob.glob(dir)
        sources.extend(source)

    sources.sort()

    removelist = []

    for x in sources:
        if int(x[24:34])<(int(gpsstart)-31):
            removelist.append(x)
#        if int(x[24:34])>int(gpsend):
        if int(x[24:34])>=ingpsend:
            removelist.append(x)

    for y in removelist:
        sources.remove(y)

    return sources


gpsstart=1246740736
gpsend=1246740737

sources=GetFilelist(gpsstart,gpsend)
print(sources)
