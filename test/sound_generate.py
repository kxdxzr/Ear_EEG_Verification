# -*- coding: utf-8 -*-
"""
Created on Wed Sep 27 11:29:19 2023

@author: leyu3109
"""

import numpy as np
from pydub import AudioSegment
from pydub.playback import play

# Constants
duration = 2  # Duration of the piano sound in seconds
sample_rate = 44100  # Sample rate in Hz (standard for audio)

# Generate a piano-like sound
def generate_piano_sound(frequency):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)  # Time values
    piano_sound = np.sin(2 * np.pi * frequency * t)  # Generate a sine wave for the given frequency
    return piano_sound

# Create a chord (You can change the frequencies to create different notes)
note_frequencies = [261.63, 329.63, 392.00]  # C4, E4, G4
chord = np.zeros(int(sample_rate * duration))

for freq in note_frequencies:
    chord += generate_piano_sound(freq)

# Normalize the audio
chord /= np.max(np.abs(chord))

# Convert to PyDub AudioSegment
chord_audio = AudioSegment(
    chord.tobytes(),
    frame_rate=sample_rate,
    sample_width=chord.dtype.itemsize,
    channels=1
)

# Play the piano chord
play(chord_audio)
