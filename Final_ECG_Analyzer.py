# -*- coding: utf-8 -*-
"""
Created on Wed Nov 27 22:31:17 2019

@author: Dev
"""

from scipy import signal
import numpy as np
import matplotlib.pyplot as plt
import wfdb
from tkinter import filedialog
from tkinter import Tk


# Load File name
root = Tk()
root.withdraw()
file_name = filedialog.askopenfilename(title="Select file",
                                       filetypes=(("ECG FIles", "*.dat"),
                                                  ("all files", "*.*")))

root.destroy()
# Import data
signal_ecg = wfdb.rdrecord(file_name[:-4])

# X-axis
xax = np.arange(0, signal_ecg.fs, float(signal_ecg.fs/signal_ecg.sig_len))

# Extract MLII signal 'record' object
opt1 = int(input('\nSelect signal:\n1.MLII\n2.V1\nEnter Choice:'))
samp = signal_ecg.p_signal[:, opt1-1]

opt2 = int(input('\nDo you want to add noise:\n1.Yes\n2.No\nEnter Choice:'))
if opt2 == 1:
    # Noise
    fnoise = int(input('\nEnter frequency to be added:'))
    amp = int(input('\nEnter amplitude of noise:'))
    n = np.array(range(signal_ecg.sig_len))
    noise = amp*np.cos(2*np.pi*fnoise*n/signal_ecg.fs)
    # Add noise
    noise_samp = samp + noise
else:
    noise = 0
    noise_samp = samp

# FFT of orignal data
fft_samp = abs(np.fft.fft(samp))
fft_samp /= max(fft_samp)

# FFT of noisy signal
fft_noise = abs(np.fft.fft(noise_samp))
fft_noise /= max(fft_noise)

# IIR Notch filter
fc = int(input('\nEnter cutoff frequency to be removed:'))
fs = signal_ecg.fs
Q = float(input('\nQuality Factor:'))
b, a = signal.iirnotch(fc, Q, fs)
filtered_samp = signal.lfilter(b, a, noise_samp)

# FFT of Filtered data
filt_fftsamp = abs(np.fft.fft(filtered_samp))
filt_fftsamp /= max(fft_samp)

# Plot of Orignal data 'signal_ecg'
plt.figure('Original ECG')
plt.subplot(211)
plt.plot(xax, samp)
plt.title('Time(' + signal_ecg.record_name + ')')
plt.subplot(212)
plt.plot(xax, fft_samp)
plt.title('Freq(' + signal_ecg.record_name + ')')

# Plot of 'noise00'
plt.figure('Noisy ECG')
plt.subplot(211)
plt.plot(xax, noise_samp)
plt.title('Time(Noisy Signal)')
plt.subplot(212)
plt.plot(xax, fft_noise)
plt.title('Freq(Noisy Signal)')

# Plot of filtered data signal_ecg
plt.figure('Filtered ECG')
plt.subplot(211)
plt.plot(xax, filtered_samp)
plt.title('Time(filtered_samp00)')
plt.subplot(212)
plt.plot(xax, filt_fftsamp)
plt.title('Freq(filtered_samp)')

# Plot of frequency response of iir filter
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
