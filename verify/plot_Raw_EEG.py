# -*- coding: utf-8 -*-
"""
Created on Wed Mar 29 12:11:16 2023

@author: yulep
"""
import numpy as np
import matplotlib.pyplot as plt
from EDFlib import edfreader
import math
from load_EEG_all_channels import load_EEG_all_channels
from mins_to_points import mins_to_points

def plot_All_Channels_EEG(sampling_rate, 
                          time, 
                          last, 
                          EEG_data2, 
                          start_point=0, 
                          vertial_line=[],
                          channel_names=["T3", "T4", "T5", "T6", "O1", "O2", "1", "2", "3", "4", "Ref1", "Ref2"],
                          vertical_color=[],
                          extra_title=""):
    plt.rcParams.update({'font.size': 30})
    time_point = mins_to_points(time, sampling_rate)  # Define mins_to_points function
    
    number_of_channels = EEG_data2.shape[0]
    ncols = 3
    nrows = math.ceil(number_of_channels / ncols)
    
    if number_of_channels <= ncols:
        fig, axs = plt.subplots(nrows=1, ncols=number_of_channels, figsize=(15, 7), sharey=True)
    else:
        fig, axs = plt.subplots(nrows=nrows, ncols=ncols, figsize=(15, 7), sharey=True)
    
    #plt.rcParams.update({'font.size': 30})

    fig.canvas.manager.set_window_title("{} {}".format(time, extra_title))
    channel_name = ["PPG", "EEG"]
    
    signal_list = range(EEG_data2.shape[0])
    
    for i in signal_list:
        channel = i
        EEG_data = EEG_data2[channel][time_point:time_point + last * sampling_rate]

        x = np.linspace(0 - start_point, last - start_point, last * sampling_rate)
        
        row = i // ncols
        col = i % ncols

        if number_of_channels <= ncols:
            for i in vertial_line:
                axs[col].axvline(x=i, color="Red", linestyle='--')
            axs[col].plot(x, EEG_data)
            axs[col].set_title('{}'.format(channel_names[channel]), loc='left')
            interval = 0.2
            axs[col].set_xticks(np.arange(0 - start_point, last - start_point + interval, interval))  # Adjust tick frequency
        else:
            for i in vertial_line:
                axs[row, col].axvline(x=i, color="Red", linestyle='--')
            axs[row, col].plot(x, EEG_data)
            axs[row, col].set_title('Channel {}'.format(channel_names[channel]))
            axs[row, col].set_xticks(np.arange(0 - start_point, last - start_point + 1, 1))  # Adjust tick frequency
        
    fig.text(0.5, 0.035, 'Time (s)', ha='center', va='center')
    fig.text(0.02, 0.5, 'EEG Signal (uV)', ha='center', va='center', rotation='vertical')

    fig.tight_layout()
    plt.show()


if __name__ == "__main__":
    path = "your_EDF_file_path_here"  # replace with your actual EDF file path
    hdl = edfreader.EDFreader(path)
    
    sampling_rate = 5000
    last = 40
    time = "0:15"  # replace with your desired time
    plot_All_Channels_EEG(sampling_rate, time, last, hdl)

    plt.show()
