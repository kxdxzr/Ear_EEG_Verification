# -*- coding: utf-8 -*-
"""
Created on Tue May 23 22:08:58 2023

@author: Steve Yu
"""
import numpy as np
import matplotlib.pyplot as plt
from mins_to_points import mins_to_points
from EDFlib import edfreader
import math

channel_name_1 = ["T3", "T4", "T5", "T6", "O1", "O2", "1", "2", "3", "4", "Ref1", "Ref2"]
channel_name_2 = ["Scalp","Ear"]

def alpha_power(channel, sampling_rate, time, last, arr1, freq_range):
    # define the window length and step size in seconds
    window_len = 2.0
    step_size = 0.1

    # calculate the number of time steps and the number of samples in each window
    n_steps = int(np.ceil((last - window_len) / step_size)) + 1
    n_window_samples = int(window_len * sampling_rate)

    # create an array to store the power values for each window
    power = np.zeros(n_steps)

    # loop through each window, calculate the power in the desired frequency range, and store it in the power array
    for i in range(n_steps):
        start_idx = int(i * step_size * sampling_rate)
        end_idx = start_idx + n_window_samples
        
        # apply Fourier transform to the windowed segment of the signal to convert it to the frequency domain
        freqs = np.fft.rfftfreq(n_window_samples, d=1/sampling_rate)
        fft = np.fft.rfft(arr1[start_idx:end_idx])
        
        # find the indices of the frequency range in the frequency array
        idx_start = np.searchsorted(freqs, freq_range[0], side='left')
        idx_end = np.searchsorted(freqs, freq_range[1], side='right')
        
        # calculate the power in the frequency range by summing the squared amplitudes of the FFT values
        power[i] = np.sum(np.abs(fft[idx_start:idx_end])**2)
    # create a time vector for the x-axis of the plot
    time = np.linspace(0, last, n_steps)

    mean_power = np.mean(power)
    power = 10 * np.log10(power) - 10 * np.log10(mean_power)
    return power, n_steps

def alpha_power_all(sampling_rate, time, last, EEG_data2, freq_range = (8, 12), channel_name_1 = channel_name_1):
    first_point = mins_to_points(time, sampling_rate)
    
    number_of_signals = EEG_data2.shape[0]
    ncols = 3
    
    if number_of_signals <= ncols:
        nrows = 1
    else:
        nrows = math.ceil(number_of_signals / ncols)
    
    if number_of_signals <= ncols:
        fig, axs = plt.subplots(nrows=1, ncols=number_of_signals, figsize=(10, 4))
        channel_name = channel_name_2
    else:
        fig, axs = plt.subplots(nrows=nrows, ncols=ncols, figsize=(10, 10))
        channel_name = channel_name_1
    fig.canvas.manager.set_window_title("{} Alpha power".format(time))
    
    avg_power_difference = []
    
    for channel in range(number_of_signals):
        arr1 = EEG_data2[channel][first_point:first_point + last * sampling_rate]
        power, n_steps = alpha_power(channel, sampling_rate, time, last, arr1,freq_range)
        time = np.linspace(0, last, n_steps)
        
        row = channel // ncols
        col = channel % ncols
        
        if number_of_signals <= ncols:
            axs[col].plot(time, power)  # dB
            axs[col].axvline(x=10, color='gray', linestyle='--')
            axs[col].axvline(x=33, color='gray', linestyle='--')
            
            avg_power_period = np.mean(power[(time >= 10) & (time <= 33)])
            avg_power_rest = np.mean(power[(time < 10) | (time > 33)])
            
            axs[col].axhline(y=avg_power_period, color='red', linestyle='--', xmin=10/last, xmax=33/last)
            axs[col].axhline(y=avg_power_rest, color='green', linestyle='--', xmin=0, xmax=10/last)
            axs[col].axhline(y=avg_power_rest, color='green', linestyle='--', xmin=33/last, xmax=1)
            
            avg_power_difference.append(avg_power_period - avg_power_rest)

            axs[col].set_title('{}, power difference:{:.2f}dB'.format(channel_name[channel], avg_power_period - avg_power_rest))
        else:
            axs[row, col].plot(time, power)  # dB
            axs[row, col].axvline(x=10, color='gray', linestyle='--')
            axs[row, col].axvline(x=33, color='gray', linestyle='--')

            avg_power_period = np.mean(power[(time >= 10) & (time <= 33)])
            avg_power_rest = np.mean(power[(time < 10) | (time > 33)])

            axs[row, col].axhline(y=avg_power_period, color='red', linestyle='--', xmin=10/last, xmax=33/last)
            axs[row, col].axhline(y=avg_power_rest, color='green', linestyle='--', xmin=0, xmax=10/last)
            axs[row, col].axhline(y=avg_power_rest, color='green', linestyle='--', xmin=33/last, xmax=1)

            avg_power_difference.append(avg_power_period - avg_power_rest)

            axs[row, col].set_title('{}, power difference:{:.2f}dB'.format(channel_name[channel], avg_power_period - avg_power_rest))
        
    fig.text(0.5, 0.04, 'Time (Second)', ha='center', va='center')
    fig.text(0.06, 0.5, 'Power spectral density (dB)', ha='center', va='center', rotation='vertical')
    
    for i in range(axs.shape[0] - 1):
        if len(axs.shape) > 1:
            for j in range(axs.shape[1]):
                axs[i, j].tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
        else:
            axs[i].tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)

    plt.show()
    return avg_power_difference

'''
path = "D:/USYD/BMET4111/Electrode/data_collected/Extend_electrode/Straight_4_electride+2_fixed_reference_silver/Alpha_2023-04-28_15-15-51.bdf"

hdl = edfreader.EDFreader(path)

time_list = ["0.10", "1.10", "2.10", "3.10", "4.10"]
sampling_rate = 5000
last = 40
power_diff_list = []
for i in time_list:
    average_diff = alpha_power_all(sampling_rate, i, last, hdl)
    power_diff_list.append(average_diff)
    print(average_diff)

# Calculate the average value difference
avg_diff_10_23 = np.mean(power_diff_list)
'''