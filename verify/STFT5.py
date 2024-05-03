# -*- coding: utf-8 -*-
"""
Created on Wed Aug 16 12:36:26 2023

@author: yulep
"""

import numpy as np
import matplotlib.pyplot as plt 
from scipy.signal import stft
from mins_to_points import mins_to_points
import math
from load_EEG_all_channels import load_EEG_all_channels

plt.rcParams.update({'font.size': 10})

channel_name_1 = ["T3", "T4", "T5", "T6", "O1", "O2", "1", "2", "3", "4", "Ref1", "Ref2"]
channel_name_2 = ["a)", "b)"]

Sampling_rate = 5000

def STFT(sampling_rate, 
         time, 
         last, 
         EEG_data2, 
         set_ylim=[1, 20],
         channel_names=[]):
    time_point = mins_to_points(time, sampling_rate)  # You need to define mins_to_points function
    window = 'hann'
    nperseg = int(sampling_rate * 1.5)
    noverlap = int(sampling_rate * 1.4)

    number_of_signals = EEG_data2.shape[0]
    ncols = 3
    nrows = math.ceil(number_of_signals / ncols)

    if number_of_signals <= ncols:
        fig, axs = plt.subplots(nrows=1, ncols=number_of_signals, figsize=(18, 5))
        channel_name = channel_name_2
    else:
        fig, axs = plt.subplots(nrows=nrows, ncols=ncols, figsize=(10, 10))
        channel_name = channel_names
    
    fig.canvas.manager.set_window_title("{} STFT".format(time))

    for i in range(number_of_signals):
        channel = i
        EEG_data = EEG_data2[i][time_point:time_point + last * sampling_rate]

        f, t, Zxx = stft(EEG_data, fs=sampling_rate, window=window, nperseg=nperseg, noverlap=noverlap)
        row = i // ncols
        col = i % ncols

        if number_of_signals <= ncols:
            axs[col].pcolormesh(t, f, np.abs(Zxx), vmin=0, vmax=np.max(np.abs(Zxx)[f < 47]), shading='gouraud')
            axs[col].set_ylim(set_ylim)
            axs[col].set_title('{}'.format(channel_names[channel]), loc='left')
            #axs[col].set_xlabel('Time [sec]')
            if col != 0:
                axs[col].set_yticklabels([])  # Remove y-label for figures not in the first column
            if last == 40:
                axs[col].axvline(x=32, color='red', linestyle='--')
                axs[col].axvline(x=10, color='red', linestyle='--')
            elif last == 100:
                axs[col].axvline(x=20, color='red', linestyle='--')
                axs[col].axvline(x=40, color='red', linestyle='--')
                axs[col].axvline(x=60, color='red', linestyle='--')
                axs[col].axvline(x=80, color='red', linestyle='--')
                axs[col].axhline(y=35, color='green', linestyle='--', xmin=0, xmax=20/last)
                axs[col].axhline(y=37, color='green', linestyle='--', xmin=20/last, xmax=40/last)
                axs[col].axhline(y=40, color='green', linestyle='--', xmin=40/last, xmax=60/last)
                axs[col].axhline(y=43, color='green', linestyle='--', xmin=60/last, xmax=80/last)
                axs[col].axhline(y=45, color='green', linestyle='--', xmin=80/last, xmax=100/last)
        else:
            axs[row, col].pcolormesh(t, f, np.abs(Zxx), vmin=0, vmax=np.max(np.abs(Zxx)[f < 47]), shading='gouraud')
            axs[row, col].set_ylim(set_ylim)
            axs[row, col].set_title('{}'.format(channel_name[channel]), loc='left')
            axs[row, col].set_xlabel('Time [sec]')
            if col != 0:
                axs[row, col].set_yticklabels([])  # Remove y-label for figures not in the first column
            if last == 40:
                axs[row, col].axvline(x=32, color='red', linestyle='--')
                axs[row, col].axvline(x=10, color='red', linestyle='--')
            elif last == 100:
                axs[row, col].axvline(x=20, color='red', linestyle='--')
                axs[row, col].axvline(x=40, color='red', linestyle='--')
                axs[row, col].axvline(x=60, color='red', linestyle='--')
                axs[row, col].axvline(x=80, color='red', linestyle='--')
                # 
                axs[row, col].axhline(y=35, color='green', linestyle='--', xmin=0, xmax=20/last)
                axs[row, col].axhline(y=37, color='green', linestyle='--', xmin=20/last, xmax=40/last)
                axs[row, col].axhline(y=40, color='green', linestyle='--', xmin=40/last, xmax=60/last)
                axs[row, col].axhline(y=43, color='green', linestyle='--', xmin=60/last, xmax=80/last)
                axs[row, col].axhline(y=45, color='green', linestyle='--', xmin=80/last, xmax=100/last)
    fig.text(0.5, 0.04, 'Time (s)', ha='center', va='center')
    fig.text(0.01, 0.5, 'Frequency(Hz)', ha='center', va='center', rotation='vertical')

    fig.tight_layout()
    plt.savefig('output_plot.png', format='png', dpi=100)  # Adjust the dpi
    plt.show()
