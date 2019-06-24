import glob
from gwpy.timeseries import TimeSeries

def GetFilelist(gpsstart,gpsend):
    '''
    This function gives full data frame file list.
    '''
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
        if int(x[24:34])>int(gpsend):
            removelist.append(x)

    for y in removelist:
        sources.remove(y)

    return sources

def GetMtrendFilelist(gpsstart,gpsend):
    '''
    This function gives minutes trend data frame file list.
    '''

    gpsstart=str(int(float(gpsstart)))
    gpsend=str(int(float(gpsend)))

    sources = []

    for i in range(int(gpsstart[0:5]),int(gpsend[0:5])+1):
        dir = '/data/trend/minute/' + str(i) + '/*'
        source = glob.glob(dir)
        sources.extend(source)
        
    sources.sort()
        
    removelist = []

    for x in sources:
        if int(x[32:42])<(int(gpsstart)-3599):
            removelist.append(x)
        if int(x[32:42])>int(gpsend):
            removelist.append(x)

    for y in removelist:
        sources.remove(y)

    return sources

def GetStrendFilelist(gpsstart,gpsend):
    '''
    This function gives second trend data frame file list.
    '''

    gpsstart=str(int(float(gpsstart)))
    gpsend=str(int(float(gpsend)))

    sources = []

    for i in range(int(gpsstart[0:5]),int(gpsend[0:5])+1):
        dir = '/data/trend/second/' + str(i) + '/*'
        source = glob.glob(dir)
        sources.extend(source)
        
    sources.sort()
        
    removelist = []

    for x in sources:
        if int(x[32:42])<(int(gpsstart)-599):
            removelist.append(x)
        if int(x[32:42])>int(gpsend):
            removelist.append(x)

    for y in removelist:
        sources.remove(y)

    return sources

def GetFilelist_Kamioka(gpsstart,gpsend):
    '''
    This function gives full data frame file list for Kashiwa server.
    '''
    gpsstart=str(int(float(gpsstart)))
    gpsend=str(int(float(gpsend)))

    sources = []

    for i in range(int(gpsstart[0:5]),int(gpsend[0:5])+1):
        dir = '/frame0/full/' + str(i) + '/*'
        source = glob.glob(dir)
        sources.extend(source)
        
    sources.sort()

    removelist = []

    for x in sources:
        if int(x[26:36])<(int(gpsstart)-31):
            removelist.append(x)
        if int(x[26:36])>int(gpsend):
            removelist.append(x)

    for y in removelist:
        sources.remove(y)

    return sources

def GetMtrendFilelist_Kamioka(gpsstart,gpsend):
    '''
    This function gives minutes trend data frame file list.
    '''
    gpsstart=str(int(float(gpsstart)))
    gpsend=str(int(float(gpsend)))

    sources = []

    for i in range(int(gpsstart[0:5]),int(gpsend[0:5])+1):
        dir = '/frame0/trend/minute/' + str(i) + '/*'
        source = glob.glob(dir)
        sources.extend(source)
        
    sources.sort()
        
    removelist = []

    for x in sources:
        if int(x[34:44])<(int(gpsstart)-3599):
            removelist.append(x)
        if int(x[34:44])>int(gpsend):
            removelist.append(x)

    for y in removelist:
        sources.remove(y)

    return sources

def GetStrendFilelist_Kamioka(gpsstart,gpsend):
    '''
    This function gives second trend data frame file list.
    '''
    gpsstart=str(int(float(gpsstart)))
    gpsend=str(int(float(gpsend)))

    sources = []

    for i in range(int(gpsstart[0:5]),int(gpsend[0:5])+1):
        dir = '/frame0/trend/second/' + str(i) + '/*'
        source = glob.glob(dir)
        sources.extend(source)
        
    sources.sort()
        
    removelist = []

    for x in sources:
        if int(x[34:44])<(int(gpsstart)-3599):
            removelist.append(x)
        if int(x[34:44])>int(gpsend):
            removelist.append(x)

    for y in removelist:
        sources.remove(y)

    return sources

def GetTriggerList(gpsstart,gpsend,channel,kamioka=False):
    '''
    This function gives omicron trigger file list in Kamioka on K1sum0,1.
    '''

    sources = []

    for i in range(int(gpsstart[0:5]),int(gpsend[0:5])+1):
        #dir = '/data/full/' + str(i) + '/*'
        if kamioka:
            dir = '/home/controls/triggers/K1/' + channel + '/' + str(i) + '/*'
        else:
            dir = '/home/detchar/triggers/K1/' + channel + '/' + str(i) + '/*'
        source = glob.glob(dir)
        sources.extend(source)
        
    sources.sort()
        
    removelist = []

    for x in sources:
        tmp = x.rsplit("-",2)
        if int(tmp[1])<(int(gpsstart)-59):
            removelist.append(x)
        if int(tmp[1])>int(gpsend):
            removelist.append(x)

    for y in removelist:
        sources.remove(y)

    return sources

def GetLegend(ltype,gpsstart,gpsend,channel):
    '''
    It gives string for legend description.
    If any argument is not relevant, please use dummy value.
    '''

    if(ltype=='time'):
        return [gpsstart + '-' + gpsend]

    latexchannel = channel.replace('_','\_')

    if(ltype=='channel'):
        return [latexchannel]
    elif(ltype=='combined'):
        return [latexchannel + ' ' + gpsstart + '-' + gpsend]
    else:
        print('Warning! Legend type is out of option.')
        return [latexchannel]

def GetDQFlag(gpsstart,gpsend,config="xarm",min_len=0,kamioka=False):
    '''
    It gives Detector Quality Flag for pointed configuration.
    '''
    channel=""
    number=-1
    if kamioka:
        sources = GetFilelist_Kamioka(gpsstart,gpsend)
    else:
        sources = GetFilelist(gpsstart,gpsend)

    if config == "xarm":
        channel="K1:GRD-LSC_LOCK_STATE_N"
        number=31415
    elif config == "LSC":
        channel="K1:GRD-LSC_LOCK_OK"
        number=1
    elif config == "IMC":
        channel="K1:GRD-IO_STATE_N"
        number=99
    else:
        print("mylib.GetDQFlag Error: No difinition for given config.")
        
    ldata = TimeSeries.read(sources,channel,format='gwf.lalframe',start=int(gpsstart),end=int(gpsend))
    locked = ldata == number
    flag = locked.to_dqflag(name = '',minlen=min_len)
    return flag
    
def GetBBTA(lposition):
    '''
    It gives argument for 
    ax.legend(bbox_to_anchor = mylib.GetBBTA(lposition))
    depending on the designated lposition.
    '''
    
    if(lposition=='br'):
        return (1,0)
    elif(lposition=='bl'):
        return (0,0)
    elif(lposition=='tr'):
        return (1,1)
    elif(lposition=='tl'):
        return (0,1)
    else:
        print('Warning! Legend type is out of option.')
        return (1,1)

def Getloc(lposition):
    '''
    It gives argument for 
    ax.legend(loc = mylib.Getloc(lposition))
    depending on the designated lposition.
    '''

    if(lposition=='br'):
        return 'lower right'
    elif(lposition=='bl'):
        return 'lower left'
    elif(lposition=='tr'):
        return 'upper right'
    elif(lposition=='tl'):
        return 'upper left'
    else:
        print('Warning! Legend type is out of option.')
        return 'upper right'

def GetTitlefromLegend(ltype,gpsstart,gpsend,channel):
    '''
    It is expected to be used with GetFromLegend. 
    If legend is time, the title is channel name.
    If legend is channel name, the title is time.
    '''

    if(ltype=='channel'):
        return gpsstart + '-' + gpsend

    latexchannel = channel.replace('_','\_')

    if(ltype=='time'):
        return latexchannel
    elif(ltype=='combined'):
        return ''
    else:
        print('Warning! Legend type is out of option.')
        return gpsstart + '-' + gpsend

# Filter function for EventTable.
# Usage: tmpevents=events.filter(('peak_time', in_time,(tmpstart,tmpend)))
def Islarger(column,target):
    return (column > target)
def Issmaller(column,target):
    return (column < target)
def Islargerequal(column,target):
    return (column >= target)
def Issmallerequal(column,target):
    return (column <= target)
def IsSame(column,target):
    return (column == target)
def between(column, interval):
    return (column >= interval[0]) & (column < interval[1])
def IsScienceMode(gpstime,mode,interval=60):
    '''
    It returns true if it is science mode from gpstime-interval to gpstime+interval.  
    '''
    dqflag = GetDQFlag(str(gpstime-interval), str(gpstime+interval), mode)

    activedq = dqflag.active
    if len(activedq) != 1:
        return False
    else:
        return ((activedq[0].start == gpstime-interval) and (activedq[0].end == gpstime+interval))
def IsFlagTrue(gpstime,dqflag,interval=60):
    '''
    It returns true if it is science mode from gpstime-interval to gpstime+interval.  
    '''
    dqflag = DataQualityFlag(str(gpstime-interval), str(gpstime+interval), mode)

    activedq = dqflag.active
    if len(activedq) != 1:
        return False
    else:
        return ((activedq[0].start == gpstime-interval) and (activedq[0].end == gpstime+interval))
