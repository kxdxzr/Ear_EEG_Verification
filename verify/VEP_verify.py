# -*- coding: utf-8 -*-
"""
Created on Thu Sep  7 17:31:27 2023

@author: yulep
"""

from average_difference import alpha_power_all
from STFT5 import STFT
from load_EEG_all_channels import load_EEG_all_channels
from montage.mean_and_replace import mean_and_replace
from montage.subtract_and_replace import subtract_and_replace
from extract_arrays import extract_arrays

path = "Z:/data_collected/ASSR40_2023-09-08_18-05-08.bdf"

sampling_rate = 5000 
last = 40 # 40 seconds

time_list = ["0.05","1.05","2.05","3.05","4.05"]
frequency = [(7,9),(11,13),(14,16),(11,13),(7,9)]
channel_number = [6,7,8]

EEG_data = load_EEG_all_channels(path)
EEG_data = mean_and_replace(EEG_data, channel_number)
EEG_data = extract_arrays(EEG_data,[5,6])

i = 0
while i < len(time_list):
    STFT(sampling_rate, time_list[i], last, EEG_data)
    alpha_power_all(sampling_rate,time_list[i],last,EEG_data,frequency[i])
    i+=1