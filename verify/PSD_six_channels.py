# -*- coding: utf-8 -*-
"""
Created on Tue Apr 11 10:49:05 2023

@author: yulep
"""

import numpy as np
import scipy.signal as signal
import matplotlib.pyplot as plt
import math
import matplotlib.image as mpimg
from SNR import find_SNR
from montage.mean_and_replace import mean_and_replace
from montage.subtract_and_replace import subtract_and_replace
from load_EEG_all_channels import load_EEG_all_channels
from mins_to_points import mins_to_points
from extract_arrays import extract_arrays

#img1 = mpimg.imread('D:/USYD/BMET4111/Electrode/1200px-21_electrodes_of_International_10-20_system_for_EEG.svg.png')
#img2 = mpimg.imread('D:/USYD/BMET4111/Electrode/data_collected/Silver Ink/Silver_three_lines/silver_ink_electrode.jpg')

path = "Z:/data_collected/ASSR_2023-08-14_16-09-05.bdf"

def PD_EEG(sampling_rate, 
           time,
           last, 
           EEG_data, 
           channel_names = [],
           vertial_line = [40],
           horizontal_line = [],
           xlim = [0, 90],
           nperseg = 10000,
           extra_title = ''):
    first_point = mins_to_points(time, sampling_rate)

    #EEG_data = extract_arrays(EEG_data, [0,6])
    number_of_signals = EEG_data.shape[0]

    ncols = 3

    if number_of_signals <= ncols:
        nrows = 1
        fig, axs = plt.subplots(nrows=1, ncols=number_of_signals, figsize=(10, 4))
    else:
        nrows = math.ceil(number_of_signals / ncols)
        fig, axs = plt.subplots(nrows=nrows, ncols=ncols, figsize=(10, 10))

    fig.canvas.manager.set_window_title("{}_{}".format(time, extra_title))

    for channel in range(number_of_signals):
        row = channel // ncols
        col = channel % ncols

        EEG_data_single = EEG_data[channel][first_point:first_point + last * sampling_rate]

        # Calculate the power spectral density using Welch's method
        f, Pxx = signal.welch(EEG_data_single, sampling_rate, nperseg=nperseg)
        SNR = find_SNR(sampling_rate, channel_names[channel], f, Pxx)
        mean_Pxx = np.mean(Pxx)
        Pxx = 10 * np.log10(Pxx) - 10 * np.log10(mean_Pxx)

        xlim_idx = np.logical_and(f >= xlim[0], f <= xlim[1])
        max_Pxx = np.max(Pxx[xlim_idx])
        min_Pxx = np.min(Pxx[xlim_idx])

        if nrows == 1:
            for i in vertial_line:
                axs[col].axvline(x=i, color="Red", linestyle='--')
            for i in horizontal_line:
                axs[col].axhline(y=i, color="Red", linestyle='--')
            axs[col].plot(f, Pxx)  # dB
            axs[col].set_title('{}, SNR: {:.2f} dB'.format(channel_names[channel], SNR))
            axs[col].set_xlim(xlim)

            if min_Pxx < 0:
                axs[col].set_ylim([min_Pxx * 1.1, max_Pxx * 1.1])  # Set y-limit to be a multiple of max_Pxx
            elif min_Pxx >= 0:
                axs[col].set_ylim([min_Pxx * 0.5, max_Pxx * 1.1])  # Set y-limit to be a multiple of max_Pxx
        else:
            for i in vertial_line:
                axs[row, col].axvline(x=i, color="Red", linestyle='--')
            for i in horizontal_line:
                axs[row, col].axhline(y=i, color="Red", linestyle='--')
            axs[row, col].plot(f, Pxx)  # dB
            axs[row, col].set_title('{}, SNR: {:.2f} dB'.format(channel_names[channel], SNR))
            axs[row, col].set_xlim(xlim)
            
            if min_Pxx < 0:
                axs[row, col].set_ylim([min_Pxx * 1.1, max_Pxx * 1.1])  # Set y-limit to be a multiple of max_Pxx
            elif min_Pxx >= 0:
                axs[row, col].set_ylim([min_Pxx * 0.5, max_Pxx * 1.1])  # Set y-limit to be a multiple of max_Pxx

    fig.text(0.5, 0.04, 'Frequency (Hz)', ha='center', va='center')
    fig.text(0.06, 0.5, 'Power spectral density (dB)', ha='center', va='center', rotation='vertical')


if __name__ == "__main__":
    sampling_rate = 5000
    last = 100
    EEG_data, channel_names = load_EEG_all_channels(path = path,
                                     sampling_rate = sampling_rate)
    EEG_data = mean_and_replace(EEG_data, [6,7,8])
    PD_EEG(sampling_rate, "0:15", last, EEG_data, channel_names = channel_names)
