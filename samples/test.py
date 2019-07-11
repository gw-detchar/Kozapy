from gwpy.timeseries import TimeSeries
from mylib import mylib

gpsstart = 1244000830.81
gpsend = 1244000832

sources = mylib.GetFilelist(gpsstart,gpsend)

print(gpsstart)
print(gpsend)
print(sources)

chname = "K1:IMC-CAV_TRANS_OUT_DQ"

data = TimeSeries.read(sources,chname,start=gpsstart,end=gpsend,format='gwf.lalframe')
#plot=data.plot()
print(data)
print(len(data))
print(6*2048)

exit()
#stride=.093750
#fft=0.015625
stride=0.093750
fft=0.015625
ol=fft/2.

#data=data.whiten(fftlength=fft,overlap=ol)
#asd = data.asd()
#plot=asd.plot()
spectrogram = data.spectrogram(stride,fftlength=fft,overlap=ol) ** (1/2.)
plot=spectrogram.plot(figsize = (12, 8),norm='log')

plot.show()
