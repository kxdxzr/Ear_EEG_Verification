# -*- coding: utf-8 -*-
"""
Created on Fri Oct 13 21:42:09 2023

@author: leyu3109
"""

def process_file(input_file, output_file):
    lines_seen = set()
    lines_to_remove = set()
    deleted_sentences = []

    with open(input_file, 'r') as infile:
        for index, line in enumerate(infile):
            line = line.strip()
            if line in lines_seen:
                deleted_sentences.append(line)
                lines_to_remove.add(index)
                if index % 2 == 0:
                    lines_to_remove.add(index + 1)
                else:
                    lines_to_remove.add(index - 1)
            else:
                lines_seen.add(line)
    print(lines_to_remove)
    print(len(lines_to_remove))
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for index, line in enumerate(infile):
            if index not in lines_to_remove:
                outfile.write(line)

    return deleted_sentences

# Specify the input and output filenames
input_filename = "C:/Users/leyu3109/OneDrive - The University of Sydney (Staff)/Desktop/Thesis/BMET4111/Electrode/data_collected/Code/test/sentences.txt"
output_filename = "output.txt"


deleted_sentences = process_file(input_filename, output_filename)

print("Deleted sentences:")
for sentence in deleted_sentences:
    print(sentence)

