# -*- coding: utf-8 -*-
"""
Created on Mon Oct  9 17:24:47 2023

@author: leyu3109
"""

from plot_Raw_EEG import plot_All_Channels_EEG
from load_EEG_all_channels_uV import load_EEG_all_channels
from spiking_detection import detect_spikes

path = "Z:/data_collected/NeoRec_2023-10-09_21-32-23.bdf"
sampling_rate = 5000
last = 1
before_spike = 0.2
exclude_channels = [10,11]
vertical_lines = [0.2]

EEG_data, channel_names = load_EEG_all_channels(path = path, 
                                 BPFfc = [1,30],
                                 sampling_rate = sampling_rate)
spike_time_points = detect_spikes(EEG_data[-2], 5e5, sampling_rate,before_spike)
standard_time_points = detect_spikes(EEG_data[-1], 5e5, sampling_rate,before_spike)
print(len(spike_time_points))
print(len(standard_time_points))

for i in range(0,10):
    time = spike_time_points[i]
    plot_All_Channels_EEG(sampling_rate,
                          time,
                          last,
                          EEG_data,
                          before_spike,
                          vertical_lines,
                          exclude_channels,
                          channel_names = channel_names)
'''
for i in range(0,10):
    time = standard_time_points[i]
    plot_All_Channels_EEG(sampling_rate,
                          time,
                          last,
                          EEG_data,
                          before_spike,
                          vertical_lines,
                          exclude_channels)
'''