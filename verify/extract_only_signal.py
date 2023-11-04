# -*- coding: utf-8 -*-
"""
Created on Thu Oct 19 21:51:31 2023

@author: Steve Yu
"""
from extract_arrays import extract_arrays

def extract_only_signal(EEG_data, channel_names, extract_channels):
    extract_index = []
    i = 0
    while i < len(channel_names):
        print(channel_names[i])
        if channel_names[i] in extract_channels:
            extract_index.append(i)
        i+=1
    siganl_list = range(EEG_data.shape[0])
    siganl_list = [x for x in siganl_list if x not in extract_index]
    return extract_arrays(EEG_data,siganl_list)