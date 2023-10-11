# -*- coding: utf-8 -*-
"""
Created on Fri Sep 29 14:41:43 2023

@author: leyu3109
"""

import PySimpleGUI as sg
import time
from save_txt import save_lists_to_txt
from datetime import datetime
import cv2
from play_sound import play_sound
import numpy as np
import wave
import winsound
import tempfile
import os

attention_record_list = []
generate_record_list = []
Response_record_list = []
sound_name = ["cello_stream.wav","clarinet_stream.wav","oboe_stream.wav"]

######################## Generate single Tone ########################
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

######################## Generate single Tone ########################

# Initialize video capture using OpenCV
cap = cv2.VideoCapture('C:/Users/leyu3109/OneDrive - The University of Sydney (Staff)/Desktop/Thesis/BMET4111/Electrode/SAND ART Return to Yourself by Kseniya Simonova - Песочная анимация Путь к Себе.mp4')

def Main_GUI():
    
    ##################### initial value ####################
    sg_theme = sg.theme("Default1")
    waiting_time = 5
    counting = False
    ##################### initial value ####################
    
    ##################### layout ###########################
    layout_1 = [
        [sg.Text(waiting_time,key = "Timing Counting", font = ("Times New Roman",256))],
        [sg.Button('Target', key='Target_BUTTON',size = (10,4)),sg.Button('Standard', key='Standard_BUTTON',size = (10,4))],
        [sg.Button('Start', key='Start_BUTTON',size = (10,4)),sg.Button('Exit', key='EXIT_BUTTON',size = (10,4))]
    ]
    
    layout_2 = [
        [sg.Image(filename='', key='-VIDEO-', size = (960, 480))],
        [sg.Button('Stop', key='Start_BUTTON',size = (10,4)),sg.Button('Exit', key='EXIT_BUTTON',size = (10,4))]
    ]
    
    window = sg.Window("Counting", layout_1, finalize=True,resizable=True, size = (1280, 960))
    time_window = window["Timing Counting"]
    ##################### layout ###########################
    
    ##################### GUI Handling #####################
    while True:
        event, values = window.read(timeout=0.1)
        if event in ['EXIT_BUTTON', sg.WIN_CLOSED]:
            window.close()
            return
        elif event == 'Target_BUTTON':
            winsound.PlaySound(tmp_target_wav_file, winsound.SND_FILENAME)
        elif event == 'Standard_BUTTON':
            winsound.PlaySound(tmp_standard_wav_file, winsound.SND_FILENAME)
        elif event == 'Start_BUTTON':
            counting = True
            start_time = time.time()
        else:
            pass
        if counting:
            # Calculate the elapsed time
            elapsed_time = time.time() - start_time
            
            # Calculate the remaining time in the countdown
            remaining_time = max(0, waiting_time - int(elapsed_time))
            
            time_window.update(value = remaining_time)
            
            # Check if the countdown has reached 0
            if remaining_time == 0:
                window.close()
                window2 = sg.Window("Video", layout_2, finalize=True,resizable=True)
                counting = False
                break
    last_playback_time = time.time()
    i = 0
    while True:
        event, values = window2.read(timeout=0.0001)
        if event in ['EXIT_BUTTON', sg.WIN_CLOSED]:
            window2.close()
            #window2.close()
            return
        
        ret, frame = cap.read()
        if ret:
            # Convert OpenCV BGR image to PySimpleGUI format
            imgbytes = cv2.imencode('.png', frame)[1].tobytes()
            window2['-VIDEO-'].update(data=imgbytes)
    #play_sound()
    
    ##################### GUI Handling #####################
Main_GUI()
now = datetime.now()

# Clean up the temporary WAV files
os.remove(tmp_standard_wav_file)
os.remove(tmp_target_wav_file)