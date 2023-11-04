# -*- coding: utf-8 -*-
"""
Created on Wed Oct 11 17:09:53 2023

@author: leyu3109
"""

import PySimpleGUI as sg
import time
import numpy as np
from save_txt import save_lists_to_txt
from datetime import datetime
import random
from play_sound import play_sound
from N400_sound_generator import generate_and_save_sentence_audio
from pulse_generator import pulse_generator, pulse_generator_standard

attention_record_list = []
generate_record_list = []
Response_record_list = []
path = "D:/USYD/BMET4111/Electrode/data_collected/Code/test/output.txt"

def get_line_from_file(line_index, filename = path):
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
            if 0 <= line_index < len(lines):
                return lines[line_index]
            else:
                return "Line index is out of range."
    except FileNotFoundError:
        return "File not found."

def play_sound_rand(i):
    if i % 2 == 0:
        generate_record_list.append("Con")
    else:
        generate_record_list.append("Incon")
    print(i)
    sentence = get_line_from_file(line_index = i)
    print(sentence)
    generate_and_save_sentence_audio(sentence)

def random_order_list(n):
    # Create a list of numbers from 0 to n
    num_list = list(range(n + 1))
    
    # Shuffle the list to randomize the order
    random.shuffle(num_list)
    
    return num_list

def Main_GUI(test_id):
    
    ##################### initial value ####################
    sg_theme = sg.theme("Default1")
    waiting_time = 60
    counting = False
    length_of_test = 190
    order_list = random_order_list(length_of_test)
    ##################### initial value ####################
    
    ##################### layout ###########################
    layout_1 = [
        [sg.Text(waiting_time,key = "Timing Counting", font = ("Times New Roman",52))],
        [sg.Button('Start', key='Start_BUTTON',size = (5,2)),sg.Button('Exit', key='EXIT_BUTTON',size = (5,2))]
    ]
    
    layout_2 = [
        [sg.Button('Congr', key='Congr_BUTTON',size = (5,2)),sg.Button('Incongr', key='Incongr_BUTTON',size = (5,2))],
        [sg.Button('Exit', key='EXIT_BUTTON',size = (5,2))]
    ]
    
    window = sg.Window("Counting", layout_1, finalize=True,resizable=True)
    time_window = window["Timing Counting"]
    ##################### layout ###########################
    
    ##################### GUI Handling #####################
    while True:
        event, values = window.read(timeout=0.1)
        if event in ['EXIT_BUTTON', sg.WIN_CLOSED]:
            window.close()
            return
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
                window2 = sg.Window("Choice", layout_2, finalize=True,resizable=True)
                break
                counting = False
    
    play_sound_rand(order_list[0])
    pulse_generator()
    i = 1
    while i < length_of_test + 1:
        event, values = window2.read()
        if event in ['EXIT_BUTTON', sg.WIN_CLOSED]:
            window2.close()
            #window2.close()
            return
        elif event == 'Congr_BUTTON':
            attention_record_list.append("Con")
            play_sound_rand(order_list[i])
            pulse_generator()
        elif event == 'Incongr_BUTTON':
            attention_record_list.append("InCon")
            play_sound_rand(order_list[i])
            pulse_generator()
        else:
            pass
        i += 1
    ##################### GUI Handling #####################
for i in range(1,2):
    Main_GUI(i)
now = datetime.now()
formatted_date_time = now.strftime("%Y_%m_%d_%H_%M_%S.txt")
save_lists_to_txt([attention_record_list,generate_record_list, Response_record_list], formatted_date_time)