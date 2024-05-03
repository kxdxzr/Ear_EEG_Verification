# -*- coding: utf-8 -*-
"""
Created on Mon Jan 29 18:52:21 2024

@author: leyu3109
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
    time_point = mins_to_points(time, sampling_rate)
    
    number_of_channels = EEG_data2.shape[0]
    ncols = 1  # Set ncols to 1 for a single column layout
    nrows = number_of_channels
    
    fig, axs = plt.subplots(nrows=nrows, ncols=ncols, figsize=(8, 7))

    fig.canvas.manager.set_window_title("{} {}".format(time, extra_title))
    channel_name = ["PPG", "EEG"]
    
    for i in range(number_of_channels):
        channel = i
        EEG_data = EEG_data2[channel][time_point:time_point + last * sampling_rate]

        x = np.linspace(0 - start_point, last - start_point, last * sampling_rate)
        
        if number_of_channels > 1:
            axs[i].axvline(x=vertial_line, color="Red", linestyle='--')
            axs[i].plot(x, EEG_data)
            axs[i].set_title('{}'.format(channel_names[channel]), loc='left')
            interval = 0.2
            axs[i].set_xticks(np.arange(0 - start_point, last - start_point + interval, interval))
        else:
            axs.axvline(x=vertial_line, color="Red", linestyle='--')
            axs.plot(x, EEG_data)
            axs.set_title('{}'.format(channel_names[channel]), loc='left')
            interval = 0.2
            axs.set_xticks(np.arange(0 - start_point, last - start_point + interval, interval))
        
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
