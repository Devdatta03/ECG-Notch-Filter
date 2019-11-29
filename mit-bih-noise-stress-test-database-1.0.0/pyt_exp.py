from scipy import signal
import numpy as np
import matplotlib.pyplot as plt
import wfdb
from tkinter import filedialog



#Import Data
record24 = wfdb.rdrecord('118e24')
record00 = wfdb.rdrecord('118e00')



#X-axis
xax = np.arange(0,360,float(360/650000))

#50Hz power line noise
fnoise = 50
n = np.array(range(650000))
noise = 10*np.cos(2*np.pi*fnoise*n/360)

#Extract MLII signal 'record' object
samp24 = record24.p_signal[:,0]
samp00 = record00.p_signal[:,0]

#Add noise
noise00 = samp00 + noise
noise24 = samp24 + noise

#Fft of orignal data
fftsamp24 = abs(np.fft.fft(samp24))
fftsamp24 = fftsamp24/max(fftsamp24)
fftsamp00 = abs(np.fft.fft(samp00))
fftsamp00 = fftsamp24/max(fftsamp00)

#FFT of noisy signal
fftnoise24 = abs(np.fft.fft(noise24))
fftnoise24 /= max(fftnoise24)
fftnoise00 = abs(np.fft.fft(noise00))
fftnoise00 /= max(fftnoise00)

#IIR Notch filter
fs = 360
Q = 10
b,a = signal.iirnotch(fnoise,Q,fs)
filtered_samp00 = signal.lfilter(b,a,noise00)
filtered_samp24 = signal.lfilter(b,a,noise24)

#FFT of Filtered data
filt_fftsamp24 = abs(np.fft.fft(filtered_samp24))
filt_fftsamp24 /= max(fftsamp24)
filt_fftsamp00 = abs(np.fft.fft(filtered_samp00))
filt_fftsamp00 /= max(fftsamp00)


#Plot of Orignal data 'record00'
plt.figure()
plt.subplot(211)
plt.plot(xax,samp00)
plt.title('Time(record00)')
plt.subplot(212)
plt.plot(xax,fftsamp00)
plt.title('Freq(record00)')

#Plot of 'noise00'
plt.figure()
plt.subplot(211)
plt.plot(xax,noise00)
plt.title('Time(Noise00)')
plt.subplot(212)
plt.plot(xax,fftnoise00)
plt.title('Freq(Noise00)')

#Plot of orignal data 'record24' 
plt.figure()
plt.subplot(211)
plt.plot(samp24)
plt.title('Time')
plt.subplot(212)
plt.plot(fftsamp24)
plt.title('Freq')

#Plot of noise24
plt.figure()
plt.subplot(211)
plt.plot(noise24)
plt.title('Time')
plt.subplot(212)
plt.plot(fftnoise24)
plt.title('Freq')

#Plot of filtered data record 00
plt.figure()
plt.subplot(211)
plt.plot(xax,filtered_samp00)
plt.title('Time(filtered_samp00)')
plt.subplot(212)
plt.plot(xax,filt_fftsamp00)
plt.title('Freq(filtered_samp00)')

#Plot of filtere data record24
plt.figure()
plt.subplot(211)
plt.plot(filtered_samp24)
plt.title('Time')
plt.subplot(212)
plt.plot(filt_fftsamp24)
plt.title('Freq')

#Plot of frequency response of iir filter
freq, h = signal.freqz(b, a, fs=fs)
fig, ax = plt.subplots(2, 1, figsize=(8, 6))
ax[0].plot(freq, 20*np.log10(abs(h)), color='blue')
ax[0].set_title("Frequency Response")
ax[0].set_ylabel("Amplitude (dB)", color='blue')
ax[0].set_xlim([0, 100])
ax[0].set_ylim([-100, 25])
ax[0].grid()
ax[1].plot(freq, np.unwrap(np.angle(h))*180/np.pi, color='green')
ax[1].set_ylabel("Angle (degrees)", color='green')
ax[1].set_xlabel("Frequency (Hz)")
ax[1].set_xlim([0, 100])
ax[1].set_yticks([-90, -60, -30, 0, 30, 60, 90])
ax[1].set_ylim([-180, 180])
ax[1].grid()
plt.show()