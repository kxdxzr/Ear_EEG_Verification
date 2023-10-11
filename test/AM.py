# -*- coding: utf-8 -*-
"""
Created on Tue Mar 28 12:52:50 2023

@author: yulep
"""

import numpy as np
import wave
import struct

# Set parameters
modulation_frequency = 40  # Hz
carrier_frequency = 1000  # Hz
duration = 100  # seconds
sample_rate = 10000  # samples per second
num_samples = int(duration * sample_rate)

# Generate the modulating signal
modulation = 0.5 * (1 + np.sin(2 * np.pi * modulation_frequency * np.arange(num_samples) / sample_rate))

# Generate the carrier signal
carrier = np.sin(2 * np.pi * carrier_frequency * np.arange(num_samples) / sample_rate)

# Apply the modulation to the carrier signal
modulated_signal = (1 + modulation) * carrier

# Scale the samples to fit within the range of a signed 16-bit integer
modulated_signal /= np.max(np.abs(modulated_signal))
scaled_samples = (modulated_signal * 32767).astype(np.int16)

# Convert the samples to bytes
sample_format = "<" + "h" * len(scaled_samples)
byte_array = struct.pack(sample_format, *scaled_samples)

# Create the wave file
with wave.open("{}Hz.wav".format(modulation_frequency), "wb") as wave_file:
    wave_file.setnchannels(1)
    wave_file.setsampwidth(2)
    wave_file.setframerate(sample_rate)
    wave_file.writeframes(byte_array)
    wave_file.close()
