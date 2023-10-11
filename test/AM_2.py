# -*- coding: utf-8 -*-
"""
Created on Fri Sep  8 18:16:01 2023

@author: yulep
"""

import numpy as np
import wave
import struct

# Set parameters
carrier_frequency = 1000  # Hz
duration = 100  # seconds
sample_rate = 44100  # samples per second
num_samples = int(duration * sample_rate)

# Generate the carrier signal
carrier = np.sin(2 * np.pi * carrier_frequency * np.arange(num_samples) / sample_rate)

# Split the duration into two halves
half_duration = duration / 2
half_num_samples = int(half_duration * sample_rate)

# Generate the modulating signal for the first half
modulation_frequency_1 = 35  # Hz for the first half
modulation_1 = 0.5 * (1 + np.sin(2 * np.pi * modulation_frequency_1 * np.arange(half_num_samples) / sample_rate))

# Generate the modulating signal for the second half
modulation_frequency_2 = 45  # Hz for the second half
modulation_2 = 0.5 * (1 + np.sin(2 * np.pi * modulation_frequency_2 * np.arange(half_num_samples) / sample_rate))

# Combine the modulation signals for the full duration
modulation = np.concatenate((modulation_1, modulation_2))

# Apply the modulation to the carrier signal
modulated_signal = (1 + modulation) * carrier

# Scale the samples to fit within the range of a signed 16-bit integer
modulated_signal /= np.max(np.abs(modulated_signal))
scaled_samples = (modulated_signal * 32767).astype(np.int16)

# Convert the samples to bytes
sample_format = "<" + "h" * len(scaled_samples)
byte_array = struct.pack(sample_format, *scaled_samples)

# Create the wave file
with wave.open("ModulatedSignal.wav", "wb") as wave_file:
    wave_file.setnchannels(1)
    wave_file.setsampwidth(2)
    wave_file.setframerate(sample_rate)
    wave_file.writeframes(byte_array)
