# -*- coding: utf-8 -*-
"""
Created on Fri Oct  6 17:34:57 2023

@author: leyu3109
"""

import scipy.signal as sig
import numpy as np
from load_EEG_all_channels import load_EEG_all_channels
from extract_arrays import extract_arrays

def detect_spikes(signal, threshold, sampling_rate,before_spike = 0):
    # Find the spikes in the signal
    spike_indices, _ = sig.find_peaks(signal, height=threshold)

    # Convert spike indices to time points in the format "MM:SS:ms"
    time_points = []
    prev_index = None
    for index in spike_indices:
        if prev_index is None or index - prev_index > sampling_rate/10:  # Check if it's a new spike
            
            time_in_seconds = index / sampling_rate - before_spike
            minutes = int(time_in_seconds / 60)
            seconds = int(time_in_seconds % 60)
            milliseconds = int((time_in_seconds * 1000) % 1000)
            time_points.append(f"{minutes:02d}:{seconds:02d}:{milliseconds:03d}")
        prev_index = index

    return time_points

# Example usage:
if __name__ == "__main__":
    path = 'Z:/data_collected/NeoRec_2023-10-09_14-57-30.bdf'
    sampling_rate = 1e6
    # Simulated spike signal (replace with your actual signal)
    signal = load_EEG_all_channels(path=path,
                                   sampling_rate=sampling_rate)
    # Set the detection threshold and sampling rate
    threshold = 5e5  # Adjust this threshold as needed
    
    # Detect spikes and print the time points
    spike_time_points = detect_spikes(signal[-1], threshold, sampling_rate)
    print("Spike Time Points:")
    for time_point in spike_time_points:
        print(time_point)
        print(type(time_point))
