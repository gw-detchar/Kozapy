from gwpy.timeseries import TimeSeries
source = ['/data/full/12311/K-K1_C-1231133824-32.gwf','/data/full/12311/K-K1_C-1231133856-32.gwf']
chname = 'K1:PEM-IXV_GND_TR120Q_X_OUT_DQ'
chnames = ['K1:PEM-IXV_GND_TR120Q_X_OUT_DQ', 'K1:PEM-IXV_GND_TR120Q_Y_OUT_DQ']

gwdata = TimeSeries.read(source,chname,format='gwf.lalframe')

specgram = gwdata.spectrogram(20, fftlength=8, overlap=4) ** (1/2.)

plot = specgram.plot(norm='log', vmin=1e-23, vmax=1e-19)
ax = plot.gca()
ax.set_ylim(40, 4000)
ax.set_yscale('log')
#ax.colorbar(label='GW strain ASD [strain/$\sqrt{\mathrm{Hz}}$]')
plot.add_colorbar(cmap='YlGnBu', log=True)
plot.show()
