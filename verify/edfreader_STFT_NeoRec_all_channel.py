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
import matplotlib.pyplot as plt

path = "Z:/data_collected/dragonfly/4.7mm/Steve/Alpha_2023-09-07_16-13-43.bdf"

sampling_rate = 5000
last = 40 # 40 seconds

time_list = ["0:05","1:05","2:05","3:07","4:05"]

EEG_data,channel_names = load_EEG_all_channels(path, BPFfc = [5,20])
#EEG_data = mean_and_replace(EEG_data, [-3,-2,-1])
#EEG_data = extract_arrays(EEG_data,[3,-1])
#channel_names = ["a)","b)"]
plt.close('all')

i = time_list[3]
STFT(sampling_rate, i, last, EEG_data,channel_names = channel_names)
alpha_power_all(sampling_rate,i,last,EEG_data, channel_name_1 = channel_names)
