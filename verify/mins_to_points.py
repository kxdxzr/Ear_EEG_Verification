# -*- coding: utf-8 -*-
"""
Created on Wed Mar 29 12:11:36 2023

@author: yulep
"""

def mins_to_points(time_str, sampling_rate):
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
