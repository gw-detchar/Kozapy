import glob

def GetFilelist(gpsstart,gpsend):
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
        if int(x[24:34])>int(gpsend):
            removelist.append(x)

    for y in removelist:
        sources.remove(y)

    return sources
