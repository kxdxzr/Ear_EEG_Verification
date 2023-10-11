# -*- coding: utf-8 -*-
"""
Created on Tue Mar 28 13:04:55 2023

@author: yulep
"""

import wave
import matplotlib.pyplot as plt
import struct
import numpy as np

def FFT_EEG(arr1,sampling_rate,last):
    fft_arr1 = np.fft.fft(arr1)
    fft_arr1 = np.abs(fft_arr1)
    N = sampling_rate * last
    n = np.arange(N)
    T = N/sampling_rate
    freq = n/T
    # Plot the results
    
    end_point = int(N/10)
    f = plt.figure("FFT") 
    plt.plot(freq[30:end_point],fft_arr1[30:end_point])
    plt.xlim([950, 1050])
    #plt.xlim([frequency_interested-5, frequency_interested+5])
    plt.show()

# Read the wave file
with wave.open("40Hz.wav", "rb") as wave_file:
    num_channels = wave_file.getnchannels()
    sample_width = wave_file.getsampwidth()
    sample_rate = wave_file.getframerate()
    num_frames = wave_file.getnframes()
    byte_array = wave_file.readframes(num_frames)

# Convert the bytes to samples
sample_format = "<" + "h" * (len(byte_array) // sample_width)
samples = struct.unpack(sample_format, byte_array)

# Plot the waveform
plt.plot(np.arange(len(samples)) / sample_rate, samples)
plt.xlabel("Time (s)")
plt.ylabel("Amplitude")
plt.show()
FFT_EEG(samples,44100,100)
