# -*- coding: utf-8 -*-
"""
Created on Mon Oct  9 17:24:47 2023

@author: leyu3109
"""

from plot_Raw_EEG import plot_All_Channels_EEG
from load_EEG_all_channels_uV import load_EEG_all_channels
from spiking_detection import detect_spikes
from PSD_six_channels import PD_EEG
from extract_only_signal import extract_only_signal
from montage.mean_and_replace import mean_and_replace
from extract_arrays import extract_arrays

path = "Z:/data_collected/Sample Test Result/P300_2023-10-12_21-40-15.bdf"
sampling_rate = 5000
time = '0.00'
last = 1
before_spike = 0.2
vertical_lines = [0.3,0.4,0.8]
vertical_color = ["Red","Red","Blue"]

EEG_data, channel_names = load_EEG_all_channels(path = path, 
                                 BPFfc = [1,30],
                                 sampling_rate = sampling_rate)
spike_time_points = detect_spikes(EEG_data, 5e5, sampling_rate, channel_names, target_channel = "pulse", before_spike = before_spike)
print(len(spike_time_points))
EEG_data = extract_only_signal(EEG_data, channel_names, ["pulse","standard"])
EEG_data = mean_and_replace(EEG_data,[-3,-2,-1])
EEG_data = extract_arrays(EEG_data,[1,-1])

for i in range(0,10):
    time = spike_time_points[i]
    plot_All_Channels_EEG(sampling_rate,
                          time,
                          last,
                          EEG_data,
                          before_spike,
                          vertical_lines,
                          channel_names = ["Scalp","Ear"],
                          vertical_color = vertical_color)
    PD_EEG(sampling_rate, 
               time,
               last, 
               EEG_data, 
               channel_names = ["Scalp","Ear"],
               xlim = [0,30])