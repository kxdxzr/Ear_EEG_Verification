# -*- coding: utf-8 -*-
"""
Created on Mon Aug 21 11:30:08 2023

@author: yulep
"""

import numpy as np

def mean_arrays(input_array, xy):
    if sum(xy) != len(input_array):
        raise ValueError("Sum of the elements in 'xy' should be equal to the number of rows in the input array.")

    result = []
    i = 0
    for val in xy[:-1]:
        if val > 0:
            mean = np.mean(input_array[i:i+val], axis=0)
            result.append(mean)
            i += val
        else:
            result.append(np.zeros_like(input_array[0]))  # If val is 0 or negative, use zero array
    
    last_val = xy[-1]
    if last_val > 0:
        mean = np.mean(input_array[-last_val:], axis=0)
        result.append(mean)
    else:
        result.append(np.zeros_like(input_array[0]))  # If last_val is 0 or negative, use zero array
    
    return np.array(result)