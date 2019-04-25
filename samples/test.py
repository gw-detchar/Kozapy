from gwpy.timeseries import TimeSeries
from gwpy.segments import DataQualityFlag
from mylib import mylib


lchannel='K1:GRD-IO_STATE_N'
gpsstart = '1237888878'
gpsend = '1237892078'

lnumber=99
llabel='IMC_LSC'
sources=mylib.GetFilelist(gpsstart,gpsend)

ldata = TimeSeries.read(sources,lchannel,format='gwf.lalframe',start=int(gpsstart),end=int(gpsend))
print(ldata)
locked = ldata == lnumber
print(locked)
flag = locked.to_dqflag(name = '', label = llabel, round = True)
plot = flag.plot()
plot.show()

plot.close()
