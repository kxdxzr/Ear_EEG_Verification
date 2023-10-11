# -*- coding: utf-8 -*-
"""
Created on Tue Aug 15 13:49:16 2023

@author: yulep
"""

import numpy as np
import matplotlib.pyplot as plt 
from scipy.signal import stft, butter, lfilter, iirnotch
from mins_to_points import mins_to_points
from EDFlib import edfreader  # Make sure you have the EDFlib library available

global channel_name
channel_name = ["T3", "T4", "T5", "T6", "O1", "O2", "1", "2", "3", "4", "Ref1", "Ref2"]
Sampling_rate = 5000

def butter_bandpass(lowcut, highcut, fs, order=6):
    nyquist = 0.5 * fs
    low = lowcut / nyquist
    high = highcut / nyquist
    b, a = butter(order, [low, high], btype='band')
    return b, a

def butter_bandpass_filter(data, lowcut, highcut, fs, order=6):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y

def butter_notch_filter(data, f0, fs):
    b, a = iirnotch(f0, Q=30, fs=fs)
    y = lfilter(b, a, data)
    return y

def STFT_EEG_all_channels(sampling_rate, time, last, hdl):
    #last = 290
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
        print("EEG_data: {}".format(EEG_data.shape))
        EEG_data_filtered = butter_bandpass_filter(EEG_data, 1, 100, sampling_rate)
        print("EEG_data_filtered: {}".format(EEG_data_filtered.shape))
        EEG_data_filtered_notch = butter_notch_filter(EEG_data_filtered, 50, sampling_rate)
        EEG_data_filtered_notch = EEG_data_filtered_notch.astype(int)
        print("EEG_data_filtered_notch: {}".format(EEG_data_filtered_notch.shape))
        
        f, t, Zxx = stft(EEG_data_filtered_notch, fs=sampling_rate, window=window, nperseg=nperseg, noverlap=noverlap)
        print("t: {}".format(t.shape))
        print("Zxx: {}".format(Zxx.shape))
        row = i // 4
        col = i % 4
        
        axs[row, col].pcolormesh(t, f, np.abs(Zxx), vmin=0, vmax=np.max(np.abs(Zxx)[f>1]), shading='gouraud')
        axs[row, col].set_ylim([1, 20])
        axs[row, col].set_title('{}'.format(channel_name[channel]))
        axs[row, col].set_ylabel('Frequency [Hz]')
        axs[row, col].set_xlabel('Time [sec]')
        axs[row, col].axvline(x=32, color='red', linestyle='--')
        axs[row, col].axvline(x=10, color='red', linestyle='--')
        #return EEG_data, EEG_data_filtered_notch
    fig.tight_layout()
    plt.show()