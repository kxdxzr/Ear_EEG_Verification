# -*- coding: utf-8 -*-
"""
Created on Wed Sep  6 14:14:43 2023

@author: yulep
"""

from average_difference import alpha_power_all
from STFT5 import STFT
from load_EEG_all_channels import load_EEG_all_channels
from montage.mean_and_replace import mean_and_replace
from montage.subtract_and_replace import subtract_and_replace
from extract_arrays import extract_arrays

path = "Z:/data_collected/NeoRec_2023-09-07_16-12-18.bdf"

channel = 0 # channel number starts with 0
sampling_rate = 5000 
last = 10 # 40 seconds

time_list = ["0.05"]
channel_number = [6,7,8]

EEG_data = load_EEG_all_channels(path)
EEG_data = mean_and_replace(EEG_data, channel_number)
#EEG_data = mean_and_replace(EEG_data, channel_number)
EEG_data = extract_arrays(EEG_data,[1,6])


STFT(sampling_rate, "0.05", last, EEG_data,[0,100])