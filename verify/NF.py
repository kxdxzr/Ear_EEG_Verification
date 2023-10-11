# -*- coding: utf-8 -*-
"""
Created on Fri Sep  8 18:58:52 2023

@author: yulep
"""
import numpy as np
from scipy.signal import iirnotch, lfilter

def notch_filter(data, fs=5000, Q=30, f0=50):
    """
    Apply a notch filter to remove a specific frequency from a signal.

    Parameters:
        - data: Input signal (numpy array).
        - fs: Sampling frequency (default is 1000 Hz).
        - Q: Quality factor of the filter (default is 30).
        - f0: Center frequency to be removed (default is 50 Hz).

    Returns:
        - Filtered signal (numpy array).
    """
    w0 = f0 / (0.5 * fs)  # Normalize the frequency
    b, a = iirnotch(w0, Q)
    filtered_signal = lfilter(b, a, data)
    return filtered_signal