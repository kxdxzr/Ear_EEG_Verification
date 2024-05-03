# -*- coding: utf-8 -*-
"""
Created on Tue Nov 28 16:23:53 2023

@author: leyu3109
"""

import numpy as np
import scipy.signal as signal
import matplotlib.pyplot as plt
import math
from SNR import find_SNR
from montage.mean_and_replace import mean_and_replace
from montage.subtract_and_replace import subtract_and_replace
from load_EEG_all_channels import load_EEG_all_channels
from mins_to_points import mins_to_points
from extract_arrays import extract_arrays

path = "Z:/data_collected/ASSR_2023-08-14_16-09-05.bdf"


def PD_EEG(sampling_rate, 
           time,
           last, 
           EEG_data, 
           channel_names=[],
           vertial_line=[40],
           horizontal_line=[],
           xlim=[0, 90],
           nperseg=10000,
           resolution=1,  # Number of points per Hz in the output
           extra_title='',
           show_SNR=True):
    first_point = mins_to_points(time, sampling_rate)

    number_of_signals = EEG_data.shape[0]

    ncols = 3

    if number_of_signals <= ncols:
        nrows = 1
        fig, axs = plt.subplots(nrows=1, ncols=number_of_signals, figsize=(16, 8), sharey=True)  # Set sharey=True
    else:
        nrows = math.ceil(number_of_signals / ncols)
        fig, axs = plt.subplots(nrows=nrows, ncols=ncols, figsize=(10, 10), sharey=True)  # Set sharey=True
    plt.rcParams.update({'font.size': 30})
    fig.canvas.manager.set_window_title("{}_{}".format(time, extra_title))

    for channel in range(number_of_signals):
        row = channel // ncols
        col = channel % ncols

        EEG_data_single = EEG_data[channel][first_point:first_point + last * sampling_rate]

        # Calculate the power spectral density using Welch's method
        f, Pxx_orig = signal.welch(EEG_data_single, sampling_rate, nperseg=nperseg)
        if show_SNR:
            SNR = find_SNR(sampling_rate, channel_names[channel], f, Pxx_orig)
        mean_Pxx = np.mean(Pxx_orig)
        Pxx_orig = 10 * np.log10(Pxx_orig) - 10 * np.log10(mean_Pxx)

        # Adjust the number of points based on the resolution
        f_resampled = np.linspace(f[0], f[-1], int((f[-1] - f[0]) * resolution) + 1)
        Pxx_resampled = np.zeros_like(f_resampled)
        for i in range(len(f_resampled)-1):
            segment_mask = np.logical_and(f >= f_resampled[i], f < f_resampled[i+1])
            mid_value = np.median(Pxx_orig[segment_mask])
            Pxx_resampled[i] = mid_value
        Pxx_resampled[-1] = np.median(Pxx_orig[f >= f_resampled[-1]])

        xlim_idx = np.logical_and(f_resampled >= xlim[0], f_resampled <= xlim[1])
        max_Pxx = np.max(Pxx_resampled[xlim_idx])
        min_Pxx = np.min(Pxx_resampled[xlim_idx])

        if nrows == 1:
            for i in vertial_line:
                axs[col].axvline(x=i, color="Red", linestyle='--')
            for i in horizontal_line:
                axs[col].axhline(y=i, color="Red", linestyle='--')

            axs[col].plot(f_resampled, Pxx_resampled)  # dB
            if show_SNR:
                axs[col].set_title('{}, SNR: {:.2f} dB'.format(channel_names[channel], SNR))
            else:
                axs[col].set_title('{}'.format(channel_names[channel]), loc='left')
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

            axs[row, col].plot(f_resampled, Pxx_resampled)  # dB
            if show_SNR:
                axs[row, col].set_title('{}, SNR: {:.2f} dB'.format(channel_names[channel], SNR))
            else:
                axs[row, col].set_title('{}'.format(channel_names[channel]))
            axs[row, col].set_xlim(xlim)
            
            if min_Pxx < 0:
                axs[row, col].set_ylim([min_Pxx * 1.1, max_Pxx * 1.1])  # Set y-limit to be a multiple of max_Pxx
            elif min_Pxx >= 0:
                axs[row, col].set_ylim([min_Pxx * 0.5, max_Pxx * 1.1])  # Set y-limit to be a multiple of max_Pxx

    fig.text(0.5, 0.025, 'Frequency (Hz)', ha='center', va='center')
    fig.text(0.055, 0.5, 'Power spectral density (dB)', ha='center', va='center', rotation='vertical')

if __name__ == "__main__":
    sampling_rate = 5000
    last = 100
    resolution = 1  # Change this to your desired resolution (points per Hz)
    EEG_data, channel_names = load_EEG_all_channels(path=path, sampling_rate=sampling_rate)
    EEG_data = mean_and_replace(EEG_data, [6, 7, 8])
    PD_EEG(sampling_rate, "0:15", last, EEG_data, channel_names=channel_names, resolution=resolution)
    plt.show()  # Add this line to display the plot
