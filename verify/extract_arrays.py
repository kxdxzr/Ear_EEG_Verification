# -*- coding: utf-8 -*-
"""
Created on Fri Sep  1 11:52:01 2023

@author: yulep
"""

import numpy as np

def extract_arrays(input_array, indices):
    selected_arrays = [input_array[idx] for idx in indices]
    return np.array(selected_arrays)
'''
# Example 2D array
input_array = np.array([[1, 2, 3],
                        [4, 5, 6],
                        [7, 8, 9],
                        [10, 11, 12]])

# List of indices to extract
indices_to_extract = [1, 3]

# Extract arrays based on indices
output_array = extract_arrays(input_array, indices_to_extract)

print("Input Array:")
print(input_array)

print("\nSelected Arrays:")
print(output_array)
'''