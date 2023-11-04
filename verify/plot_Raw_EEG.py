# -*- coding: utf-8 -*-
"""
Created on Wed Mar 29 12:11:16 2023

@author: yulep
"""
from mins_to_points import mins_to_points
import numpy as np
import matplotlib.pyplot as plt
from EDFlib import edfreader
import math
from load_EEG_all_channels import load_EEG_all_channels

def plot_All_Channels_EEG(sampling_rate, 
                          time, 
                          last, 
                          EEG_data2, 
                          start_point = 0, 
                          vertial_line = [],
                          channel_names = ["T3", "T4", "T5", "T6", "O1", "O2", "1", "2", "3", "4", "Ref1", "Ref2"],
                          vertical_color = [],
                          extra_title = ""):
    time_point = mins_to_points(time, sampling_rate)  # Define mins_to_points function
    
    number_of_channels = EEG_data2.shape[0]
    ncols = 3
    nrows = math.ceil(number_of_channels / ncols)
    
    if number_of_channels <= ncols:
        fig, axs = plt.subplots(nrows=1, ncols=number_of_channels, figsize=(15, 5))
    else:
        fig, axs = plt.subplots(nrows=nrows, ncols=ncols, figsize=(15, 5))

    fig.canvas.manager.set_window_title("{} {}".format(time, extra_title))
    channel_name = ["PPG", "EEG"]
    
    siganl_list = range(EEG_data2.shape[0])
    
    for i in siganl_list:
        channel = i
        EEG_data = EEG_data2[channel][time_point:time_point + last * sampling_rate]

        x = np.linspace(0 - start_point, last - start_point, last * sampling_rate)
        
        row = i // ncols
        col = i % ncols

        if number_of_channels <= ncols:
            for i in vertial_line:
                axs[col].axvline(x=i, color="Red", linestyle='--')
            axs[col].plot(x, EEG_data)
            axs[col].set_title('Channel {}'.format(channel_names[channel]))
            axs[col].set_ylabel('EEG Value')
            axs[col].set_xlabel('Time [sec]')
        else:
            for i in vertial_line:
                axs[row, col].axvline(x=i, color="Red", linestyle='--')
            axs[row, col].plot(x, EEG_data)
            axs[row, col].set_title('Channel {}'.format(channel_names[channel]))
            axs[row, col].set_ylabel('EEG Value')
            axs[row, col].set_xlabel('Time [sec]')
        '''
        for peak_position in peak_list:
            if number_of_channels <= ncols:
                axs[col].axvline(x=peak_position / sampling_rate, color='black', linestyle='--')
            else:
                axs[row, col].axvline(x=peak_position / sampling_rate, color='black', linestyle='--')
        '''


    fig.tight_layout()
    plt.show()

if __name__ == "__main__":
    path = "Z:/data_collected/NeoRec_2023-10-09_21-32-23.bdf"
    sampling_rate = 5000
    time = '1:30'
    last = 10
    before_spike = 0.2
    EEG_data, channel_names = load_EEG_all_channels(path = path, 
                                     BPFfc = [1,30],
                                     sampling_rate = sampling_rate)
    plot_All_Channels_EEG(sampling_rate,
                          time,
                          last,
                          EEG_data,
                          channel_names = channel_names)