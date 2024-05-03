# -*- coding: utf-8 -*-
"""
Created on Fri Oct 20 15:59:37 2023

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
from N_back_task_generator import N_back_task_generator

generate_record_list = []
Response_record_list = []
now = datetime.now()
formatted_date_time = now.strftime("N_back_%Y_%m_%d_%H_%M_%S.txt")

def task_order_generator():
    order = [0,1,2]
    random.shuffle(order)
    while len(order) < 30:
        current_order = [0,1,2]
        random.shuffle(current_order)
        while current_order[0] == order[-1]:
            random.shuffle(current_order)
        order = order + current_order
    return order

def duplicate_elements(input_list, times=2):
    duplicated_list = [x for x in input_list for _ in range(times)]
    return duplicated_list

def Main_GUI(test_id):
    
    ##################### initial value ####################
    sg_theme = sg.theme("Default1")
    waiting_time = 15
    counting = True
    length_of_test = 190
    max_age  = 20
    value_list = []
    each_wait = 2.5
    pushed = False
    shown_start = False
    shown_length = 0.5
    blank_length = 2
    ##################### initial value ####################
    
    ##################### layout ###########################
    layout_2 = [
        [sg.Text(waiting_time,key = "Timing Counting", font = ("Times New Roman",52))],
        [sg.Text("Back Number: ", font = ("Times New Roman",52)), sg.Text(test_id, font = ("Times New Roman",52))],
        [sg.Text("-",key = "Current_shown", font = ("Times New Roman",52))],
        [sg.Button('✓', key='Yes_BUTTON',size = (5,2)),sg.Button('X', key='No_BUTTON',size = (5,2))],
        [sg.Text("---%",key = "Accurate_rate", font = ("Times New Roman",52))],
        [sg.Button('Start', key='Start_BUTTON',size = (5,2)),sg.Button('Exit', key='EXIT_BUTTON',size = (5,2))]
    ]
    
    window2 = sg.Window("Counting", layout_2, finalize=True,resizable=True)
    time_window = window2["Timing Counting"]
    ##################### layout ###########################
    
    ##################### GUI Handling #####################
    shown_window = window2["Current_shown"]
    Accurate_window = window2["Accurate_rate"]
    i = 0
    ls, ls_rec = N_back_task_generator(test_id)
    print(ls)
    previous_time = time.time()
    window2.finalize()
    show_start_time = time.time()
    blank_start = False
    start_time = time.time()
    while True:
        event, values = window2.read(timeout=1)
        if event in ['EXIT_BUTTON', sg.WIN_CLOSED]:
            window2.close()
            return 1
        if counting:
            # Calculate the elapsed time
            elapsed_time = time.time() - start_time
            
            # Calculate the remaining time in the countdown
            remaining_time = max(0, waiting_time - int(elapsed_time))
            
            time_window.update(value = remaining_time)
            
            # Check if the countdown has reached 0
            if remaining_time == 0:
                counting = False
                shown_window.update(value = ls[i])
                show_start_time = time.time()
                shown_start = True
                previous_time = time.time()
        else:
            if not pushed:
                if event == 'Yes_BUTTON':
                    Response_record_list.append(1)
                    generate_record_list.append(1 == ls_rec[i])
                    new_value = {
                        'data': 1 == ls_rec[i],
                        'timestamp': time.time()
                    }
                    value_list.append(new_value)
                    pushed = True
                elif event == 'No_BUTTON':
                    Response_record_list.append(0)
                    generate_record_list.append(0 == ls_rec[i])
                    new_value = {
                        'data': 0 == ls_rec[i],
                        'timestamp': time.time()
                    }
                    value_list.append(new_value)
                    pushed = True
            current_time = time.time()
            value_list = [value for value in value_list if current_time - value['timestamp'] <= max_age]
            if len(value_list) == 0:
                rate = "---%"
            else:
                total = 0
                for value in value_list:
                    total += value['data']
                rate = "{:.3g}%".format(total/(len(value_list))*100)
            Accurate_window.update(value = rate)
            current_time = time.time()
            if current_time - previous_time > each_wait and blank_start:
                if not pushed:
                    Response_record_list.append("-")
                    generate_record_list.append("-")
                    new_value = {
                        'data': 0,
                        'timestamp': time.time()
                    }
                    value_list.append(new_value)
                pushed = False
                previous_time = current_time
                i += 1
                if i == 48:
                    window2.close()
                    break
                else:
                    if ls_rec[i]:
                        pulse_generator()
                    else:
                        pulse_generator_standard()
                    shown_window.update(value = ls[i])
                    show_start_time = time.time()
                    shown_start = True
                    blank_start = False
            if current_time - show_start_time > shown_length and shown_start and not blank_start:
                shown_window.update(value = " ")
                shown_start = False
                blank_start = True
    return 0
    ##################### GUI Handling #####################
total_order = []
exit_flag = 0
for i in range(4):
    order = task_order_generator()
    total_order += order
    print(order)
    for i in range(0,6):
        exit_flag = Main_GUI(order[i])
        if exit_flag:
            break
    if exit_flag:
        break


save_lists_to_txt([total_order,generate_record_list, Response_record_list], formatted_date_time)