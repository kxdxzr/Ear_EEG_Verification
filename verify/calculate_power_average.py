# -*- coding: utf-8 -*-
"""
Created on Thu Apr 27 12:13:11 2023

@author: yulep
"""

import sys
import numpy as np
from EDFlib import edfreader
import matplotlib.pyplot as plt 
from scipy.signal import stft
from mins_to_points import mins_to_points
from grand_average import alpha_power_all, alpha_power
import scipy.signal as signal
def calculate_power_average_difference(hdl,time, last,sampling_freq, freq_range):
    first_point = mins_to_points(time,sampling_rate)
    
    number_of_signals = hdl.getNumSignals()
    arr1 = np.array([0 for i in range(0,last * sampling_rate)])
    arr2 = np.array([0 for i in range(0,last * sampling_rate)])
    for i in range(number_of_signals):
        hdl.readSamples(i, arr1, last * sampling_rate)
        hdl.fseek(i,first_point-13,0)
        hdl.readSamples(i, arr2, 10 * sampling_rate)
        close_value = calculate_power_average(arr1,sampling_freq,freq_range)
        open_value = calculate_power_average(arr2,sampling_freq,freq_range)
        print("channel {} at time {} is:{}".format(i,time,close_value / open_value))
    


def calculate_power_average(arr1, sampling_freq, freq_range):
    # Compute the power spectral density of the signal using Welch's method
    f, psd = signal.welch(arr1, fs=sampling_freq, nperseg=1024)

    # Find the indices corresponding to the frequency range of interest
    indices = np.where((f >= freq_range[0]) & (f <= freq_range[1]))[0]

    # Compute the average power in the frequency range of interest
    avg_power = np.mean(psd[indices])

    return avg_power


#path = "NeoRec_2023-03-02_16-35-13.bdf"
#path = "NeoRec_2023-03-02_16-52-04.bdf"
#path = "NeoRec_2023-03-10_14-37-42.bdf"
path = "D:/USYD/BMET4111/Electrode/data_collected/Extend_electrode/Straight_4_electride+2_fixed_reference_silver/Alpha_2023-04-28_15-05-52.bdf"

hdl = edfreader.EDFreader(path)

print("Number of signals: %d" %(hdl.getNumSignals()))
print("Number of datarecords: %d" %(hdl.getNumDataRecords()))

filetype = hdl.getFileType()

edfsignals = hdl.getNumSignals()

n = edfsignals
# channel number starts with 0
channel = 0
sampling_rate = 5000
last = 23

#time_list = ["0.10","1.10","2.20","3.00","3.50"]
#time_list = ["0.30","1.10","3.10","4.50","5.50"]
time_list = ["0.20","1.20","2.20","3.20","4.20"]

for i in time_list:
    calculate_power_average_difference(hdl,i, last,sampling_rate, [8,12])
    
