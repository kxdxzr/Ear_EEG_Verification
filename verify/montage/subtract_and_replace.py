# -*- coding: utf-8 -*-
"""
Created on Tue Aug 22 15:22:29 2023

@author: yulep
"""

import numpy as np

def subtract_and_replace(arr, indices):
    selected_arrays = arr[indices]
    for i in range(1, len(selected_arrays)):
        selected_arrays[0] -= selected_arrays[i]
    
    arr[indices[0]] = selected_arrays[0]
    arr = np.delete(arr, indices[1:], axis=0)
    
    return arr
