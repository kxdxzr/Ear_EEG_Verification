# -*- coding: utf-8 -*-
"""
Created on Sat Oct 21 15:42:21 2023

@author: leyu3109
"""

from plot_Raw_EEG import plot_All_Channels_EEG
from load_EEG_all_channels_uV import load_EEG_all_channels
from spiking_detection import detect_spikes
from read_first_line_to_list import read_first_line_to_list
from PSD_six_channels_resampling import PD_EEG
from extract_only_signal import extract_only_signal
from montage.mean_and_replace import mean_and_replace
from extract_arrays import extract_arrays

path = "Z:/data_collected/N_back_2023-10-22_15-13-50.bdf"
log_path = '../test/2023_10_22_15_19_43.txt'
sampling_rate = 5000
last = 2
before_spike = 0.5

EEG_data, channel_names = load_EEG_all_channels(path = path, 
                                 BPFfc = [0.5,100],
                                 sampling_rate = sampling_rate)
extract_channels = ['pulse','standard']
spike_time_points = detect_spikes(EEG_data, 5e5, sampling_rate,channel_names, 'pulse',before_spike)
standard_time_points = detect_spikes(EEG_data, 5e5, sampling_rate,channel_names, 'standard',before_spike)
print(len(spike_time_points))
#EEG_data = mean_and_replace(EEG_data, [-3,-2,-1])
#EEG_data = extract_arrays(EEG_data, [9])
EEG_data = extract_only_signal(EEG_data, channel_names, extract_channels)
EEG_data = mean_and_replace(EEG_data,[-3,-2,-1])
EEG_data = extract_arrays(EEG_data,[1,-1])
channel_names = ["a)","b)"]
for i in range(0,100):
    time = standard_time_points[i]
    #extra_title_1 = read_first_line_to_list(log_path,0)[i//48]
    #extra_title_2 = read_first_line_to_list(log_path,1)[i]
    #extra_title_3 = read_first_line_to_list(log_path,2)[i]
    #extra_title = extra_title_1 + "_" + extra_title_2 + "_" + extra_title_3
    #print(extra_title)
    '''
    plot_All_Channels_EEG(sampling_rate,
                          time,
                          last,
                          EEG_data,
                          before_spike,
                          channel_names = channel_names)
    '''
    PD_EEG(sampling_rate, 
               time,
               last, 
               EEG_data, 
               channel_names = channel_names,
               vertial_line = [7,12],
               xlim = [0, 100],
               nperseg = 5000,
               extra_title = "",
               show_SNR = False)

    