# -*- coding: utf-8 -*-
"""
Created on Tue Aug 15 16:49:24 2023

@author: yulep
"""

import numpy as np
import matplotlib.pyplot as plt 
from scipy.signal import stft, butter, lfilter, iirnotch
from mins_to_points import mins_to_points
from EDFlib import edfreader  # Make sure you have the EDFlib library available
from C5 import Filtering_BSF
from C5_2 import Filtering_BPF
import numpy as np
from scipy.signal import cwt, morlet


global channel_name
channel_name = ["T3", "T4", "T5", "T6", "O1", "O2", "1", "2", "3", "4", "Ref1", "Ref2"]
Sampling_rate = 5000

BPF = Filtering_BPF(7,100,Sampling_rate)
BSF = Filtering_BSF(55,45,Sampling_rate)

def STFT_EEG_all_channels(sampling_rate, time, last, hdl):
    time_point = mins_to_points(time, sampling_rate)
    # Define the STFT parameters
    window = 'hann'
    nperseg = int(sampling_rate * 1.5)
    noverlap = int(sampling_rate * 0.5)

    fig, axs = plt.subplots(nrows=3, ncols=4, figsize=(10, 10))
    fig.canvas.set_window_title("{} STFT".format(time))
    number_of_signals = hdl.getNumSignals()

    for i in range(number_of_signals):
        channel = i
        hdl.fseek(channel, 0, 0)
        EEG_data = np.array([0 for i in range(0, last * sampling_rate)])
        hdl.readSamples(channel, EEG_data, last * sampling_rate)
        
        f, t, Zxx = stft(EEG_data, fs=sampling_rate, window=window, nperseg=nperseg, noverlap=noverlap)
        
        row = i // 4
        col = i % 4
        
        axs[row, col].pcolormesh(t, f, np.abs(Zxx), vmin=0, vmax=np.max(np.abs(Zxx)[f<20]), shading='gouraud')
        axs[row, col].set_ylim([1, 20])  # Adjust the y-axis limit to start from 1 Hz
        axs[row, col].set_title('{}'.format(channel_name[channel]))
        axs[row, col].set_ylabel('Frequency [Hz]')
        axs[row, col].set_xlabel('Time [sec]')
        axs[row, col].axvline(x=32, color='red', linestyle='--')
        axs[row, col].axvline(x=10, color='red', linestyle='--')
    
    fig.tight_layout()
    plt.show()

def wavelet_convolution_EEG_all_channels(sampling_rate, time, last, hdl):
    time_point = mins_to_points(time, sampling_rate)
    # Define the wavelet convolution parameters
    scales = np.arange(1, 21)  # Wavelet scales corresponding to frequencies 1 Hz to 20 Hz

    fig, axs = plt.subplots(nrows=3, ncols=4, figsize=(10, 10))
    fig.canvas.set_window_title("{} Wavelet Convolution".format(time))
    number_of_signals = hdl.getNumSignals()

    for i in range(number_of_signals):
        channel = i
        hdl.fseek(channel, 0, 0)
        EEG_data = np.array([0 for i in range(0, last * sampling_rate)])
        hdl.readSamples(channel, EEG_data, last * sampling_rate)
        
        # Perform wavelet convolution using scipy.signal.cwt
        coefficients = cwt(EEG_data, morlet, widths=scales)
        
        row = i // 4
        col = i % 4
        
        # Display wavelet coefficients as an image
        axs[row, col].imshow(np.abs(coefficients), extent=[0, last, 1, 20], aspect='auto', cmap='viridis', vmin=0, vmax=np.max(np.abs(coefficients)))
        axs[row, col].set_title('{}'.format(channel_name[channel]))
        axs[row, col].set_ylabel('Frequency [Hz]')
        axs[row, col].set_xlabel('Time [sec]')
        axs[row, col].axvline(x=32, color='red', linestyle='--')
        axs[row, col].axvline(x=10, color='red', linestyle='--')
    
    fig.tight_layout()
    plt.show()

