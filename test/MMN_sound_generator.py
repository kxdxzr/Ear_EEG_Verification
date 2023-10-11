# -*- coding: utf-8 -*-
"""
Created on Fri Sep 29 15:13:38 2023

@author: leyu3109
"""

import numpy as np
import wave
import winsound
import tempfile
import os

# Constants
duration = 124  # Duration of each tone in milliseconds (124 ms)
sample_rate = 44100  # Sample rate in Hz (standard for audio)
target_ratio = 0.2  # 20% of the tones will be target tones

# Generate time points
t = np.linspace(0, duration / 1000.0, int(sample_rate * duration / 1000), endpoint=False)

# Generate standard tone at 800 Hz
standard_tone = np.sin(2 * np.pi * 800 * t)

# Normalize the audio to fit within the -32768 to 32767 range (16-bit PCM)
standard_tone = (standard_tone * 32767).astype(np.int16)

# Generate target tone at 1000 Hz
target_tone = np.sin(2 * np.pi * 1000 * t)

# Normalize the audio to fit within the -32768 to 32767 range (16-bit PCM)
target_tone = (target_tone * 32767).astype(np.int16)

# Create a list to store the target sound start times in milliseconds
target_start_times_ms = []

# Save the standard tone as a temporary WAV file
tmp_standard_wav_file = tempfile.mktemp(suffix=".wav")

# Create a WAV file and write the audio data
with wave.open(tmp_standard_wav_file, 'wb') as wf:
    wf.setnchannels(1)  # Mono audio
    wf.setsampwidth(2)  # 16-bit audio
    wf.setframerate(sample_rate)
    wf.writeframes(standard_tone.tobytes())

# Save the target tone as a temporary WAV file
tmp_target_wav_file = tempfile.mktemp(suffix=".wav")

# Create a WAV file and write the audio data
with wave.open(tmp_target_wav_file, 'wb') as wf:
    wf.setnchannels(1)  # Mono audio
    wf.setsampwidth(2)  # 16-bit audio
    wf.setframerate(sample_rate)
    wf.writeframes(target_tone.tobytes())

# Play the tones and record target sound start times
for i in range(1000):
    if i % int(1 / target_ratio) == 0:
        # This is a target tone
        print(f"Playing target tone {i + 1}...")
        winsound.PlaySound(tmp_target_wav_file, winsound.SND_FILENAME)
        target_start_times_ms.append(i * duration)
    else:
        # This is a standard tone
        print(f"Playing standard tone {i + 1}...")
        winsound.PlaySound(tmp_standard_wav_file, winsound.SND_FILENAME)

# Clean up the temporary WAV files
os.remove(tmp_standard_wav_file)
os.remove(tmp_target_wav_file)

# Save the target sound start times to a text file
with open("target_start_times.txt", "w") as file:
    for time_ms in target_start_times_ms:
        file.write(f"{time_ms} ms\n")

print("Target sound start times saved to 'target_start_times.txt'.")
