# -*- coding: utf-8 -*-
"""
Created on Mon Oct  9 17:24:47 2023

@author: leyu3109
"""

from plot_Raw_EEG_1 import plot_All_Channels_EEG
from load_EEG_all_channels_uV import load_EEG_all_channels
from spiking_detection import detect_spikes
from read_first_line_to_list import read_first_line_to_list
from extract_only_signal import extract_only_signal
from montage.mean_and_replace import mean_and_replace
from extract_arrays import extract_arrays

path = "Z:/data_collected/Sample Test Result/N100_2023-10-17_21-55-22.bdf"
log_path = 'C:/Users/leyu3109/OneDrive - The University of Sydney (Staff)/Desktop/Thesis/BMET4111/Electrode/data_collected/Code/test/2023_10_17_22_07_48.txt'
sampling_rate = 5000
last = 1
before_spike = 0.2
vertical_lines = [0.2]

EEG_data, channel_names = load_EEG_all_channels(path = path, 
                                 BPFfc = [1,30],
                                 sampling_rate = sampling_rate)
spike_time_points = detect_spikes(EEG_data, 5e5, sampling_rate, channel_names, target_channel = "pulse", before_spike = before_spike)
standard_time_points = detect_spikes(EEG_data, 5e5, sampling_rate, channel_names, target_channel = "standard", before_spike = before_spike)
print(len(spike_time_points))
print(len(standard_time_points))
EEG_data = extract_only_signal(EEG_data, channel_names, ["pulse","standard"])
EEG_data = mean_and_replace(EEG_data,[-3,-2,-1])
EEG_data = extract_arrays(EEG_data,[1,-1])

for i in range(30,50):
    time = spike_time_points[i]
    
    extra_title_1 = read_first_line_to_list(log_path,0)[i]
    extra_title_2 = read_first_line_to_list(log_path,1)[i]
    extra_title_3 = read_first_line_to_list(log_path,2)[i]
    extra_title = "{}_{}_{}".format(extra_title_1, 
                                    extra_title_2, 
                                    extra_title_3)
    
    plot_All_Channels_EEG(sampling_rate,
                          time,
                          last,
                          EEG_data,
                          before_spike,
                          vertical_lines,
                          extra_title = extra_title,
                          channel_names = ["a)","b)"])
