# -*- coding: utf-8 -*-
"""
Created on Wed Sep  6 11:59:38 2023

@author: yulep
"""

from mins_to_points import mins_to_points
import numpy as np
import matplotlib.pyplot as plt
from EDFlib import edfreader
from load_EEG_all_channels import load_EEG_all_channels
from montage.mean_and_replace import mean_and_replace
import math
from extract_arrays import extract_arrays

def find_peak_positions(array_2d):
    if len(array_2d) == 0:
        return []

    first_row = array_2d[0]
    peak_positions = []
    
    i = 1  # Start from the second element
    while i < len(first_row) - 1:
        if first_row[i] >= first_row[i - 1] and first_row[i] >= first_row[i + 1]:
            if first_row[i] > first_row[i + 1]:
                peak_positions.append(i)
            elif first_row[i] == first_row[i + 1]:
                # Handle continuous same values
                start = i
                while i < len(first_row) - 1 and first_row[i] == first_row[i + 1]:
                    i += 1
                end = i
                middle = (start + end) // 2
                if end == len(first_row) - 1 or first_row[middle] > first_row[end + 1]:
                    peak_positions.append(middle)
        i += 1
    return peak_positions

def plot_All_Channels_EEG(sampling_rate, time, last, EEG_data2):
    time_point = mins_to_points(time, sampling_rate)  # Define mins_to_points function
    number_of_channels = EEG_data2.shape[0]
    
    fig, ax = plt.subplots(figsize=(15, 5))
    fig.canvas.set_window_title("EEG Channels")
    channel_name = ["Scalp", "Ear"]
    
    for i in range(number_of_channels):
        channel = i
        EEG_data = EEG_data2[channel][time_point:time_point + last * sampling_rate]

        x = np.linspace(0, last, last * sampling_rate)
        
        ax.plot(x, EEG_data, label='Channel {}'.format(channel_name[channel]))

    ax.set_ylabel('EEG Value')
    ax.set_xlabel('Time [sec]')
    ax.legend()
    '''
    peak_list = find_peak_positions(EEG_data2)
    for peak_position in peak_list:
        ax.axvline(x=peak_position / sampling_rate, color='black', linestyle='--')
    '''
    plt.show()

    
path = "Z:/data_collected/NeoRec_2023-09-07_16-12-18.bdf"
sampling_rate = 5000
time = '0.05'
last = 10

EEG_data = load_EEG_all_channels(path = path, 
                                 BPFfc = [1,7],
                                 sampling_rate = sampling_rate, 
                                 last = 20)

EEG_data = mean_and_replace(EEG_data, [-3,-2,-1])
EEG_data = extract_arrays(EEG_data, [0,6])

plot_All_Channels_EEG(sampling_rate, time, last, EEG_data)
