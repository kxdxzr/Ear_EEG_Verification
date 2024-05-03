# -*- coding: utf-8 -*-
"""
Created on Fri Dec 15 14:33:26 2023

@author: leyu3109
"""

from plot_Raw_EEG import plot_All_Channels_EEG
from load_EEG_all_channels_uV import load_EEG_all_channels
from spiking_detection import detect_spikes
from read_first_line_to_list import read_first_line_to_list
from PSD_six_channels_resampling import PD_EEG
from extract_only_signal import extract_only_signal
from montage.mean_and_replace import mean_and_replace
from extract_arrays import extract_arrays
from scipy import signal
import numpy as np
import matplotlib.pyplot as plt
import math
from mins_to_points import mins_to_points

def mins_to_points(time_str, sampling_rate):
    # Convert time_str to string if it's not already
    if not isinstance(time_str, str):
        time_str = str(time_str)

    # Split the time string based on ":"
    time_parts = time_str.split(":")
    
    # Calculate total points based on the number of parts in the time string
    if len(time_parts) == 2:
        # Format is "xx:xx" (minute:second)
        minutes = int(time_parts[0])
        seconds = int(time_parts[1])
        total_points = int((minutes * 60 + seconds) * sampling_rate)
    elif len(time_parts) == 3:
        # Format is "xx:xx:xxx" (minute:second:millisecond)
        minutes = int(time_parts[0])
        seconds = int(time_parts[1])
        milliseconds = int(time_parts[2])
        total_points = int((minutes * 60 + seconds + milliseconds / 1000) * sampling_rate)
    else:
        raise ValueError("Invalid time format. Expected 'xx:xx' or 'xx:xx:xxx'.")
    
    return total_points

def format_seconds_to_time(seconds):
    minutes = int(seconds // 60)
    seconds = int(seconds % 60)
    milliseconds = int((seconds % 1) * 1000)
    return f"{minutes:02d}:{seconds:02d}:{milliseconds:03d}"


def time_str_to_seconds(time_str):
    if not isinstance(time_str, str):
        raise ValueError("time_str should be a string in the format 'mm:ss:fff'")

    time_parts = time_str.split(":")
    if len(time_parts) != 3:
        raise ValueError("Invalid time format. Use 'mm:ss:fff'.")

    minutes, seconds, milliseconds = map(int, time_parts)
    total_seconds = minutes * 60 + seconds + milliseconds / 1000.0
    return total_seconds


def average_PSD_across_times(sampling_rate, times, last, EEG_data, channel_names, vertial_line, horizontal_line, xlim, nperseg, resolution, show_SNR):
    average_Pxx = 0
    total_iterations = len(times)

    for i, time_str in enumerate(times):
        time_seconds = time_str_to_seconds(time_str) + (2 * i)
        time_seconds = format_seconds_to_time(time_seconds)
        first_point = mins_to_points(time_seconds, sampling_rate)

        for channel in range(EEG_data.shape[0]):
            EEG_data_single = EEG_data[channel][first_point:first_point + last * sampling_rate]

            f, Pxx_orig = signal.welch(EEG_data_single, sampling_rate, nperseg=nperseg)
            print(f, Pxx_orig)
            mean_Pxx = np.mean(Pxx_orig)
            Pxx_orig = 10 * np.log10(Pxx_orig) - 10 * np.log10(mean_Pxx)

            # Adjust the number of points based on the resolution
            f_resampled = np.linspace(f[0], f[-1], int((f[-1] - f[0]) * resolution) + 1)
            Pxx_resampled = np.zeros_like(f_resampled)
            for j in range(len(f_resampled) - 1):
                segment_mask = np.logical_and(f >= f_resampled[j], f < f_resampled[j + 1])
                mid_value = np.median(Pxx_orig[segment_mask])
                Pxx_resampled[j] = mid_value
            Pxx_resampled[-1] = np.median(Pxx_orig[f >= f_resampled[-1]])

            average_Pxx += Pxx_resampled

    average_Pxx /= total_iterations

    # Plot the averaged result
    plot_averaged_PSD(f_resampled, average_Pxx, channel_names, vertial_line, horizontal_line, xlim, show_SNR)

def plot_averaged_PSD(f, average_Pxx, channel_names, vertial_line, horizontal_line, xlim, show_SNR):
    number_of_signals = len(channel_names)

    ncols = 3

    if number_of_signals <= ncols:
        nrows = 1
        fig, axs = plt.subplots(nrows=1, ncols=number_of_signals, figsize=(10, 4))
    else:
        nrows = math.ceil(number_of_signals / ncols)
        fig, axs = plt.subplots(nrows=nrows, ncols=ncols, figsize=(10, 10))

    for channel in range(number_of_signals):
        row = channel // ncols
        col = channel % ncols

        Pxx_resampled = average_Pxx[channel]

        xlim_idx = np.logical_and(f >= xlim[0], f <= xlim[1])
        max_Pxx = np.max(Pxx_resampled[xlim_idx])
        min_Pxx = np.min(Pxx_resampled[xlim_idx])

        if nrows == 1:
            for i in vertial_line:
                axs[col].axvline(x=i, color="Red", linestyle='--')
            for i in horizontal_line:
                axs[col].axhline(y=i, color="Red", linestyle='--')

            axs[col].plot(f, Pxx_resampled)  # dB
            if show_SNR:
                axs[col].set_title('{}, SNR: {:.2f} dB'.format(channel_names[channel], 0))  # You can calculate SNR for the averaged result if needed
            else:
                axs[col].set_title('{}'.format(channel_names[channel]))
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

            axs[row, col].plot(f, Pxx_resampled)  # dB
            if show_SNR:
                axs[row, col].set_title('{}, SNR: {:.2f} dB'.format(channel_names[channel], 0))  # You can calculate SNR for the averaged result if needed
            else:
                axs[row, col].set_title('{}'.format(channel_names[channel]))
            axs[row, col].set_xlim(xlim)

            if min_Pxx < 0:
                axs[row, col].set_ylim([min_Pxx * 1.1, max_Pxx * 1.1])  # Set y-limit to be a multiple of max_Pxx
            elif min_Pxx >= 0:
                axs[row, col].set_ylim([min_Pxx * 0.5, max_Pxx * 1.1])  # Set y-limit to be a multiple of max_Pxx

    fig.text(0.5, 0.04, 'Frequency (Hz)', ha='center', va='center')
    fig.text(0.06, 0.5, 'Power spectral density (dB)', ha='center', va='center', rotation='vertical')

# Continue with the rest of your original code...

path = "Z:/data_collected/NeoRec_2023-10-24_13-17-05.bdf"
log_path = '../test/2023_10_22_15_19_43.txt'
sampling_rate = 5000
last = 2
before_spike = 0.5

EEG_data, channel_names = load_EEG_all_channels(path=path,
                                                 BPFfc=[0.5, 100],
                                                 sampling_rate=sampling_rate)
extract_channels = ['pulse', 'standard']
spike_time_points = detect_spikes(EEG_data, 5e5, sampling_rate, channel_names, 'pulse', before_spike)
standard_time_points = detect_spikes(EEG_data, 5e5, sampling_rate, channel_names, 'standard', before_spike)
print(len(spike_time_points))

EEG_data = extract_only_signal(EEG_data, channel_names, extract_channels)
EEG_data = mean_and_replace(EEG_data, [-3, -2, -1])
EEG_data = extract_arrays(EEG_data, [1, -1])
channel_names = ["Scalp", "Ear"]

# Adjust the range of times to average as needed
times_to_average = spike_time_points[:100]

# Call the new function
average_PSD_across_times(sampling_rate, times_to_average, last, EEG_data, channel_names, [7, 12], [], [0, 100], 5000, 1, True)

# Continue with the rest of your original code...
