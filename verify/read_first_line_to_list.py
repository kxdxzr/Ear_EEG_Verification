# -*- coding: utf-8 -*-
"""
Created on Tue Oct 17 15:51:23 2023

@author: leyu3109
"""

def read_first_line_to_list(file_path, line_number):
    try:
        # Open the file for reading
        with open(file_path, 'r') as file:
            # Read lines from the file into a list
            lines = file.readlines()

        if line_number < len(lines):
            # Split the specified line into a list using a comma as the delimiter
            values_list = lines[line_number].strip().split(',')
            return values_list
        else:
            print(f"Line {line_number} does not exist in the file.")
            return []

    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return []
    
if __name__ == "__main__":
    # Example usage:
    file_path = '../test/2023_10_15_16_24_12.txt'  # Replace with the path to your text file
    values_list = read_first_line_to_list(file_path, 1)
    print(values_list)
