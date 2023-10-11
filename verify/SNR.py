# -*- coding: utf-8 -*-
"""
Created on Mon Apr 24 16:36:17 2023

@author: yulep
"""
import numpy as np
from scipy import signal
from mins_to_points import mins_to_points
from EDFlib import edfreader

def find_all_SNR(sampling_rate,time,last,hdl):
    first_point = mins_to_points(time,sampling_rate)
    
    number_of_signals = hdl.getNumSignals()
    for channel in range(number_of_signals):
        hdl.fseek(channel,first_point,0)
        arr1 = np.array([0 for i in range(0,last * sampling_rate)])
        
        
        hdl.readSamples(channel, arr1, last * sampling_rate)
        # Calculate the power spectral density (PSD) using Welch's method
        freqs, psd = signal.welch(arr1, fs=sampling_rate, nperseg=10000)
        
        find_SNR(sampling_rate,channel,arr1)
        
def find_SNR(sampling_rate,channel,freqs, psd):       
        
    # Convert the PSD to decibels
    psd_dB = 10 * np.log10(psd)
        
    # Find the indices of the frequencies closest to 35 Hz, 40 Hz, and 45 Hz
    i_35 = np.argmin(np.abs(freqs - 35))
    i_40 = np.argmin(np.abs(freqs - 40))
    i_45 = np.argmin(np.abs(freqs - 45))
    
    # Calculate the mean power from 35-45 Hz, excluding 40 Hz, in decibels
    mean_power_dB = 10 * np.log10((np.sum(psd[i_35:i_40]) + np.sum(psd[i_40+1:i_45+1])) / (len(psd[i_35:i_40]) + len(psd[i_40+1:i_45+1])))
        
    # Calculate the power at 40 Hz in decibels
    power_40_dB = psd_dB[i_40]
        
    # Calculate the ratio of power at 40 Hz to mean power from 35-45 Hz, excluding 40 Hz, in decibels
    ratio_dB = power_40_dB - mean_power_dB
        
    print("Ratio of power at 40 Hz for channel {} to mean power from 35-45 Hz, excluding 40 Hz, in decibels: {:.2f} dB".format(channel,ratio_dB))
    return ratio_dB