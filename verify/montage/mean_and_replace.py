# -*- coding: utf-8 -*-
"""
Created on Tue Aug 22 15:16:36 2023

@author: yulep
"""

import numpy as np

def mean_and_replace(arr, indices):
    selected_arrays = arr[indices]
    mean_array = np.mean(selected_arrays, axis=0)
    
    arr[indices[0]] = mean_array
    arr = np.delete(arr, indices[1:], axis=0)
    
    return arr