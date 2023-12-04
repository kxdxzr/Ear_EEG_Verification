# -*- coding: utf-8 -*-
"""
Created on Fri Sep  8 16:44:22 2023

@author: yulep
"""

from average_difference import alpha_power_all
from STFT5 import STFT
from load_EEG_all_channels import load_EEG_all_channels
from montage.mean_and_replace import mean_and_replace
from montage.subtract_and_replace import subtract_and_replace
from extract_arrays import extract_arrays

path = "Z:/data_collected/NeoRec_2023-09-13_13-13-46.bdf"

sampling_rate = 5000
last = 100 # 40 seconds

time = "0:15"
frequency = [(7,9),(11,13),(14,16),(11,13),(7,9)]
channel_number = [6,7,8]

EEG_data, channel_names = load_EEG_all_channels(path, BPFfc = [32,47])
EEG_data = mean_and_replace(EEG_data, channel_number)
EEG_data = extract_arrays(EEG_data,[3,6])

STFT(sampling_rate,time, last, EEG_data,[32,47], channel_names = channel_names)
