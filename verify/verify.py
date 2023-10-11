# -*- coding: utf-8 -*-
"""
Created on Sun Sep 17 14:26:14 2023

@author: yulep
"""

import numpy as np
from STFT5 import STFT
from scipy.io import wavfile
import os

file_path = 'C:/Users/leyu3109/OneDrive - The University of Sydney (Staff)/Desktop/Thesis/BMET4111/Electrode/data_collected/Code/1.wav'

if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
else:
    sample_rate, audio_data = wavfile.read(file_path)
    print(sample_rate)

    time = "0.05"
    last = 80
    
    print(audio_data.shape[0])
    #left_channel = audio_data[:, 0]
    audio_data = np.transpose(audio_data)
    print(audio_data.shape[0])
    STFT(sample_rate, time, last, audio_data, set_ylim=[32, 47])