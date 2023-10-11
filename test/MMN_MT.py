# -*- coding: utf-8 -*-
"""
Created on Mon Oct  2 16:03:40 2023

@author: leyu3109
"""

import PySimpleGUI as sg
import time
import cv2
import numpy as np
import tempfile
import threading
import winsound
import wave
import random
from pulse_generator import pulse_generator, pulse_generator_standard

attention_record_list = []
generate_record_list = []
Response_record_list = []

# Constants for audio tones
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

# Initialize video capture using OpenCV
cap = cv2.VideoCapture('D:/USYD/BMET4111/Electrode/SAND ART Return to Yourself by Kseniya Simonova - Песочная анимация Путь к Себе.mp4')

def play_audio(exit_flag):
    tones_played = 0
    total_tones = 1000
    last_playback_time = time.time()
    min_interval = 800
    max_interval = 1000
    target_number = 0
    standad_number = 0
    while tones_played < total_tones:
        if exit_flag.is_set():
            break
        
        current_time = time.time()

        if current_time - last_playback_time >= duration / 1000.0:
            if random.random() < target_ratio:
                winsound.PlaySound(tmp_target_wav_file, winsound.SND_FILENAME)
                pulse_generator()
                target_number += 1
                print("Playing target tone {}".format(target_number))
            else:
                winsound.PlaySound(tmp_standard_wav_file, winsound.SND_FILENAME)
                standad_number += 1
                pulse_generator_standard()
                print("Playing standard tone {}".format(standad_number))
            last_playback_time = current_time
            tones_played += 1

        interval = random.randint(min_interval, max_interval)
        time.sleep(interval / 1000.0)

def Main_GUI():
    ##################### initial value ####################
    sg_theme = sg.theme("Default1")
    waiting_time = 60
    counting = False
    exit_flag = threading.Event()
    ##################### initial value ####################
    
    ##################### layout ###########################
    layout_1 = [
        [sg.Text(waiting_time,key = "Timing Counting", font = ("Times New Roman",256))],
        [sg.Button('Target', key='Target_BUTTON',size = (10,4)),sg.Button('Standard', key='Standard_BUTTON',size = (10,4))],
        [sg.Button('Start', key='Start_BUTTON',size = (10,4)),sg.Button('Exit', key='EXIT_BUTTON',size = (10,4))]
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
                counting = False
                break
    
    # Create and start a thread for audio playback
    audio_thread = threading.Thread(target=play_audio, args=(exit_flag,))
    audio_thread.start()

    # Play video in the main thread
    layout_2 = [
        [sg.Image(filename='', key='-VIDEO-', size=(960, 480))],
        [sg.Button('Stop', key='Start_BUTTON', size=(10, 4)), sg.Button('Exit', key='EXIT_BUTTON', size=(10, 4))]
    ]
    window2 = sg.Window("Video", layout_2, finalize=True, resizable=True)
    while True:
        event, values = window2.read(timeout=0.0001)
        if event in ['EXIT_BUTTON', sg.WIN_CLOSED]:
            window2.close()
            exit_flag.set()
            return
        
        ret, frame = cap.read()
        if ret:
            # Convert OpenCV BGR image to PySimpleGUI format
            imgbytes = cv2.imencode('.png', frame)[1].tobytes()
            window2['-VIDEO-'].update(data=imgbytes)

Main_GUI()
