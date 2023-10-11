# -*- coding: utf-8 -*-
"""
Created on Wed Aug 16 11:14:19 2023

@author: yulep
"""

import numpy as np
import matplotlib.pyplot as plt 
from scipy.signal import stft, butter, lfilter, iirnotch
from mins_to_points import mins_to_points
from EDFlib import edfreader  # Make sure you have the EDFlib library available
from FFT_filter import fft_filter

global channel_name
channel_name = ["T3", "T4", "T5", "T6", "O1", "O2", "1", "2", "3", "4", "Ref1", "Ref2"]
Sampling_rate = 5000


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
        hdl.fseek(channel, time_point, 0)
        EEG_data = np.array([0 for i in range(0, last * sampling_rate)])
        hdl.readSamples(channel, EEG_data, last * sampling_rate)
        
        EEG_data = fft_filter(EEG_data,5,Sampling_rate)
        
        #EEG_data = EEG_data[10*sampling_rate:10*-sampling_rate]
        
        f, t, Zxx = stft(EEG_data, fs=sampling_rate, window=window, nperseg=nperseg, noverlap=noverlap)
        
        row = i // 4
        col = i % 4
        
        axs[row, col].pcolormesh(t, f, np.abs(Zxx), vmin=0, vmax=np.max(np.abs(Zxx)[f<20]), shading='gouraud')
        axs[row, col].set_ylim([0, 20])  # Adjust the y-axis limit to start from 1 Hz
        axs[row, col].set_title('{}'.format(channel_name[channel]))
        axs[row, col].set_ylabel('Frequency [Hz]')
        axs[row, col].set_xlabel('Time [sec]')
        axs[row, col].axvline(x=32, color='red', linestyle='--')
        axs[row, col].axvline(x=10, color='red', linestyle='--')
    
    fig.tight_layout()
    plt.show()
