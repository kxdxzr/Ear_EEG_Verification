# -*- coding: utf-8 -*-
"""
Created on Fri Sep 22 12:04:16 2023

@author: leyu3109
"""

import PySimpleGUI as sg
import time
import numpy as np
from save_txt import save_lists_to_txt
from datetime import datetime
import random
from play_sound import play_sound
from pulse_generator import pulse_generator, pulse_generator_standard

attention_record_list = []
generate_record_list = []
Response_record_list = []
waiting_time = 5
counting = False
sound_name = ["cello_stream.wav","clarinet_stream.wav","oboe_stream.wav"]
def play_sound_rand():
    random_number = random.randint(0, 2)
    generate_record_list.append(random_number)
    sound_file = sound_name[random_number]
    play_sound(sound_file)

def Main_GUI(test_id):
    
    ##################### initial value ####################
    sg_theme = sg.theme("Default1")
    waiting_time = 5
    ##################### initial value ####################
    
    ##################### layout ###########################
    
    layout_2 = [
        [sg.Button('Left', key='Left_BUTTON',size = (5,2)),sg.Button('Right', key='Right_BUTTON',size = (5,2))],
        [sg.Button('Exit', key='EXIT_BUTTON',size = (5,2))]
    ]
    
    layout_3 = [
        [sg.Button('HIGH', key='HIGH_BUTTON',size = (5,2))],
        [sg.Button('MID', key='MIDDLE_BUTTON',size = (5,2))],
        [sg.Button('LOW', key='LOW_BUTTON',size = (5,2))],
        [sg.Button('Exit', key='EXIT_BUTTON',size = (5,2))]
    ]
    
    window2 = sg.Window("Choice", layout_2, finalize=True,resizable=True)
    ##################### layout ###########################
    
    ##################### GUI Handling #####################
    while True:
        event, values = window2.read(timeout=0.1)
        if event in ['EXIT_BUTTON', sg.WIN_CLOSED]:
            window2.close()
            #window2.close()
            return
        elif event == 'Left_BUTTON':
            attention_record_list.append("L")
            break
        elif event == 'Right_BUTTON':
            attention_record_list.append("R")
            break
        else:
            pass
    window2.close()
    window3 = sg.Window("Response", layout_3, finalize=True,resizable=True)    
    play_sound_rand()
    pulse_generator()
    while True:
        event, values = window3.read()
        if event in ['EXIT_BUTTON', sg.WIN_CLOSED]:
            window3.close()
            #window2.close()
            return
        elif event == 'HIGH_BUTTON':
            Response_record_list.append("L")
            window3.close()
        elif event == 'MIDDLE_BUTTON':
            Response_record_list.append("M")
            window3.close()
        elif event == 'LOW_BUTTON':
            Response_record_list.append("R")
            window3.close()
        else:
            pass
    ##################### GUI Handling #####################
layout_1 = [
    [sg.Text(waiting_time,key = "Timing Counting", font = ("Times New Roman",52))],
    [sg.Button('Start', key='Start_BUTTON',size = (5,2)),sg.Button('Exit', key='EXIT_BUTTON',size = (5,2))]
]    
sg_theme = sg.theme("Default1")
window = sg.Window("Counting", layout_1, finalize=True,resizable=True)
time_window = window["Timing Counting"]

while True:
    event, values = window.read(timeout=0.1)
    if event in ['EXIT_BUTTON', sg.WIN_CLOSED]:
        window.close()
    if event == 'Start_BUTTON':
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
            break
            counting = False
for i in range(1,10):
    Main_GUI(i)
now = datetime.now()
formatted_date_time = now.strftime("%Y_%m_%d_%H_%M_%S.txt")
save_lists_to_txt([attention_record_list,generate_record_list, Response_record_list], formatted_date_time)