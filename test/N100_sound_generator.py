# -*- coding: utf-8 -*-
"""
Created on Fri Oct  6 11:12:05 2023

@author: yulep
"""
from pydub import AudioSegment
import numpy as np
import array

# Function to generate a sine wave tone
def generate_tone(duration, frequency):
    t = np.linspace(0, duration, int(44100 * duration), False)
    tone = 0.5 * np.sin(2 * np.pi * frequency * t)
    tone = (tone * 32767.0).astype(np.int16)
    return AudioSegment(array.array('h', tone).tobytes(), frame_rate=44100, sample_width=2, channels=1)

# Define parameters for each stream
streams = [
    {'tones': 4, 'durations': [0.75, 1.0, 0.75, 1.0], 'instruments': ['cello', 'cello', 'cello', 'cello'], 'pitches': [(220, 440), (220, 440), (440, 880), (440, 880)], 'pan': [-1, -1, -1, -1]},
    {'tones': 3, 'durations': [1.0, 1.0, 1.0], 'instruments': ['clarinet', 'clarinet', 'clarinet'], 'pitches': [(261.63, 523.25), (523.25, 1046.5), (261.63, 523.25)], 'pan': [0, 0, 0]},
    {'tones': 5, 'durations': [0.6, 0.6, 0.6, 0.6, 0.6], 'instruments': ['oboe', 'oboe', 'oboe', 'oboe', 'oboe'], 'pitches': [(523.25, 261.63), (523.25, 261.63), (261.63, 130.81), (261.63, 130.81), (261.63, 130.81)], 'pan': [1, 1, 1, 1, 1]},
]

# Generate and play the audio streams
for stream in streams:
    left_channel = AudioSegment.empty()
    right_channel = AudioSegment.empty()
    center_channel = AudioSegment.empty()
    for i in range(stream['tones']):
        tone = generate_tone(stream['durations'][i], stream['pitches'][i][0])
        
        # Apply panning to separate left and right channels
        if stream['pan'][i] == -1:
            left_channel += tone
        elif stream['pan'][i] == 1:
            right_channel += tone
        else:
            center_channel += tone

    # Combine left and right channels into a stereo audio stream
    stereo_audio = left_channel.pan(-1) + right_channel.pan(1) + center_channel.pan(0)
    
    print(f"Playing {stream['instruments'][0]} stream with {stream['tones']} tones.")
    stereo_audio.export(f"{stream['instruments'][0]}_stream.wav", format="wav")