# -*- coding: utf-8 -*-
"""
Created on Wed Mar  1 15:54:55 2023

@author: yulep
"""

from average_difference import alpha_power_all
from STFT5 import STFT
from load_EEG_all_channels import load_EEG_all_channels
from montage.mean_and_replace import mean_and_replace
from montage.subtract_and_replace import subtract_and_replace
from extract_arrays import extract_arrays

path = "Z:/data_collected/NeoRec_2023-10-31_13-38-33.bdf"

sampling_rate = 5000
last = 60 # 40 seconds

time_list = ["0:05","1:05","2:05","3:05","4:05"]
channel_number = [7,8,9]

EEG_data,channel_names = load_EEG_all_channels(path, BPFfc = [1,100])
#EEG_data = mean_and_replace(EEG_data, channel_number)
#EEG_data = extract_arrays(EEG_data,[5,6])


for i in time_list:
    STFT(sampling_rate, i, last, EEG_data,channel_names = channel_names)
    alpha_power_all(sampling_rate,i,last,EEG_data, channel_name_1 = channel_names)
