# -*- coding: utf-8 -*-
"""
Created on Mon Oct  9 17:24:47 2023

@author: leyu3109
"""

from plot_Raw_EEG import plot_All_Channels_EEG
from load_EEG_all_channels_uV import load_EEG_all_channels
from spiking_detection import detect_spikes
from read_first_line_to_list import read_first_line_to_list

path = "Z:/data_collected/Sample Test Result/N400_2023-10-15_16-19-31.bdf"
sampling_rate = 5000
last = 1
before_spike = 0.2
vertical_lines = [0.42]

EEG_data, channel_names = load_EEG_all_channels(path = path, 
                                 BPFfc = [1,30],
                                 sampling_rate = sampling_rate)
spike_time_points = detect_spikes(EEG_data[-2], 5e5, sampling_rate,before_spike)
print(len(spike_time_points))
#EEG_data = mean_and_replace(EEG_data, [-3,-2,-1])
#EEG_data = extract_arrays(EEG_data, [9])
for i in range(0,10):
    time = spike_time_points[i]
    extra_title_1 = read_first_line_to_list('../test/2023_10_15_16_24_12.txt',0)[i]
    extra_title_2 = read_first_line_to_list('../test/2023_10_15_16_24_12.txt',1)[i]
    extra_title = extra_title_1 + "_" + extra_title_2
    plot_All_Channels_EEG(sampling_rate,
                          time,
                          last,
                          EEG_data,
                          before_spike,
                          vertical_lines,
                          channel_names = channel_names,
                          extra_title = extra_title)