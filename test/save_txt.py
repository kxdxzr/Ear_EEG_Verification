# -*- coding: utf-8 -*-
"""
Created on Wed Sep 27 11:58:07 2023

@author: leyu3109
"""

def save_lists_to_txt(data_list, title):
    with open(title, 'w') as f:
        for data in data_list:
            f.write(','.join(map(str, data)) + '\n')

data_list = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
save_lists_to_txt(data_list, 'output.txt')
