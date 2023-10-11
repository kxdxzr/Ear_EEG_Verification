# -*- coding: utf-8 -*-
"""
Created on Sat Sep  9 14:39:02 2023

@author: yulep
"""

import numpy as np
import wave
import struct

# Set parameters
carrier_frequency = 1000  # Hz
duration = 100  # seconds
sample_rate = 10000  # samples per second
num_samples = int(duration * sample_rate)

# Generate the carrier signal
carrier = np.sin(2 * np.pi * carrier_frequency * np.arange(num_samples) / sample_rate)

# Define the modulation frequencies for each part
modulation_frequencies = [5, 10, 20, 30, 40]  # Example modulation frequencies for N parts

# Divide the duration into equal parts based on the number of modulation frequencies
num_parts = len(modulation_frequencies)  # You can change this to the desired number of parts
part_duration = duration / num_parts
part_num_samples = int(part_duration * sample_rate)

# Initialize an empty array for the full modulation signal
modulation = np.zeros(num_samples)

# Generate the modulating signals for each part and combine them
for i, modulation_frequency in enumerate(modulation_frequencies):
    modulation_segment = 0.5 * (1 + np.sin(2 * np.pi * modulation_frequency * np.arange(part_num_samples) / sample_rate))
    start_sample = i * part_num_samples
    end_sample = (i + 1) * part_num_samples
    modulation[start_sample:end_sample] = modulation_segment

# Apply the modulation to the carrier signal
modulated_signal = (1 + modulation) * carrier

# Scale the samples to fit within the range of a signed 16-bit integer
modulated_signal /= np.max(np.abs(modulated_signal))
scaled_samples = (modulated_signal * 32767).astype(np.int16)

# Convert the samples to bytes
sample_format = "<" + "h" * len(scaled_samples)
byte_array = struct.pack(sample_format, *scaled_samples)

# Create the wave file with a dynamic name
file_name = "{}.wav".format("-".join(map(str, modulation_frequencies[:num_parts])))
with wave.open(file_name, "wb") as wave_file:
    wave_file.setnchannels(1)
    wave_file.setsampwidth(2)
    wave_file.setframerate(sample_rate)
    wave_file.writeframes(byte_array)

