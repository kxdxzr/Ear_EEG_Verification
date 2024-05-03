# -*- coding: utf-8 -*-
"""
Created on Thu Mar 28 15:58:30 2024

@author: leyu3109
"""

import numpy as np
from scipy.fft import fft, fftfreq
from EDFlib import edfreader
from load_EEG_all_channels import load_EEG_all_channels
from montage.mean_and_replace import mean_and_replace
from montage.subtract_and_replace import subtract_and_replace
from extract_arrays import extract_arrays
from mins_to_points import mins_to_points

def calculate_power_in_frequency_range(signal, time, last, sampling_rate, freq_range):
    # Find the indices corresponding to the time range
    start_index = mins_to_points(time, sampling_rate)
    end_index = start_index + last * sampling_rate
    number_of_signals = signal.shape[0]
    
    R_AM_values = []  # List to store RAM values for each channel
    
    for channel in range(number_of_signals):   
        signal_segment_rest = signal[channel][start_index:start_index + 10 * sampling_rate] + signal[channel][end_index - 10 * sampling_rate:end_index]
        signal_segment_active = signal[channel][start_index + 10 * sampling_rate:end_index - 10 * sampling_rate]
        
        # Perform FFT on the signal segment
        n_rest = len(signal_segment_rest)
        n_active = len(signal_segment_active)
        
        fft_result_rest = fft(signal_segment_rest)
        fft_result_active = fft(signal_segment_active)
        
        # Calculate the frequencies corresponding to FFT result
        freqs_rest = fftfreq(n_rest, d=1/sampling_rate)
        freqs_active = fftfreq(n_active, d=1/sampling_rate)
        
        # Find the indices corresponding to the frequency range
        indices_rest = np.where((freqs_rest >= freq_range[0]) & (freqs_rest <= freq_range[1]))[0]
        indices_active = np.where((freqs_active >= freq_range[0]) & (freqs_active <= freq_range[1]))[0]
        
        # Calculate the power within the frequency range
        power_rest = np.sum(np.abs(fft_result_rest[indices_rest])**2) / n_rest
        power_active = np.sum(np.abs(fft_result_active[indices_active])**2) / n_active
        
        ratio = power_active/power_rest
        
        R_AM_values.append(ratio)
    
    return R_AM_values

if __name__ == "__main__":
    # Frequency range of interest (replace these values with your desired frequency range)
    freq_start = 8  # Start frequency in Hz
    freq_end = 12  # End frequency in Hz
    freq_range = (freq_start, freq_end)
    
    path = "Z:/data_collected/dragonfly/4.7mm/Steve/Alpha_2023-09-07_16-13-43.bdf"
    
    hdl = edfreader.EDFreader(path)
    
    time_list = ["0:05","1:05","2:05","3:07","4:05"]
    sampling_rate = 5000
    last = 40
    
    EEG_data,channel_names = load_EEG_all_channels(path, BPFfc = [5,20])
    EEG_data = mean_and_replace(EEG_data, [-3,-2,-1])
    EEG_data = extract_arrays(EEG_data,[3,-1])
    
    for i in time_list:
        power_in_range = calculate_power_in_frequency_range(EEG_data, i, last, sampling_rate, freq_range)
        print("Power Ratio:", power_in_range)
