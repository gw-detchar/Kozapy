import glob
from gwpy.timeseries import TimeSeries

def filelist(start,end,trend='full',place='kashiwa',**kwargs):
    '''

    Parameters
    ----------
    gpsstart : `float`
        start gps time
    gpsend : `float`
        end gps time

    trend : `str`, optional
        'full' or 'mtrend' or 'strend'. Default is full
    place : `str`, optional
        'kamioka' or 'kashiwa'. Defalut is kashiwa        

    Returns
    -------
    function 
    
    '''
    if place=='kashiwa':
        if trend=='full':
            return _full_kashiwa(start,end,**kwargs)
        elif trend=='mtrend':
            return _mtrend_kashiwa(start,end,**kwargs)
        elif trend=='strend':
            return _strend_kashiwa(start,end,**kwargs)
        else:
            raise ValueError('"{}" is invalid trend name.'.format(trend))
    elif place=='kamioka':
        if trend=='full':
            return _full_kamioka(start,end,**kwargs)
        elif trend=='mtrend':
            return _mtrend_kamioka(start,end,**kwargs)
        elif trend=='strend':
            return _strend_kamioka(start,end,**kwargs)        
        else:
            raise ValueError('"{}" is invalid trend name.'.format(trend))            
    else:
        raise ValueError('"{}" is invalid place name.'.format(place))



def _full_kamioka(gpsstart,gpsend,**kwargs):
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


def _full_kashiwa(gpsstart,gpsend,**kwargs):
    '''
    This function gives full data frame file list.

    Parameters
    ----------
    gpsstart : `float`
        start gps time
    gpsend : `float`
        end gps time
    
    Returns
    -------
    sources : `list`
        paths to files
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


def _mtrend_kamioka(gpsstart,gpsend,**kwargs):
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

def _mtrend_kashiwa(gpsstart,gpsend,**kwargs):
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



def _strend_kamioka(gpsstart,gpsend,**kwargs):
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


def _strend_kashiwa(gpsstart,gpsend,**kwargs):
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
