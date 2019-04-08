import glob

def GetFilelist(gpsstart,gpsend):
    '''
    This function gives full data frame file list.
    '''

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

def GetLegend(ltype,gpsstart,gpsend,channel):
    '''
    It gives string for legend description.
    '''

    print('GetLegend is called.')
    print(ltype)
    print(gpsstart)
    print(gpsend)
    print(channel)    
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

