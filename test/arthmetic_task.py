# -*- coding: utf-8 -*-
"""
Created on Sat Oct 21 19:17:19 2023

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
from arthmetic_task_generator import arthmetic_task_generator

generate_record_list = []
Response_record_list = []
path = "D:/USYD/BMET4111/Electrode/data_collected/Code/test/output.txt"

def task_order_generator():
    order = [1,2,3,4,5]
    random.shuffle(order)
    while len(order) < 30:
        current_order = [1,2,3,4,5]
        random.shuffle(current_order)
        while current_order[0] == order[-1]:
            random.shuffle(current_order)
        order = order + current_order
    return order

def Main_GUI(test_id):
    
    ##################### initial value ####################
    sg_theme = sg.theme("Default1")
    waiting_time = 20
    counting = False
    length_of_test = 190
    max_age  = 20
    value_list = []
    ##################### initial value ####################
    
    ##################### layout ###########################
    layout_1 = [
        [sg.Text(waiting_time,key = "Timing Counting", font = ("Times New Roman",52))],
        [sg.Button('Start', key='Start_BUTTON',size = (5,2)),sg.Button('Exit', key='EXIT_BUTTON',size = (5,2))]
    ]
    
    layout_2 = [
        [sg.Text("Level: ", font = ("Times New Roman",52)), sg.Text(test_id, font = ("Times New Roman",52))],
        [sg.Text("-",key = "Current_shown", font = ("Times New Roman",52))],
        [sg.Button('Done', key='Done_BUTTON',size = (5,2))],
        [sg.Button('<', key='<',size = (5,2)),
         sg.Button('=', key='=',size = (5,2)),
         sg.Button('>', key='>',size = (5,2))],
        [sg.Text("---%",key = "Accurate_rate", font = ("Times New Roman",52))],
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
            return 1
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
    shown_window = window2["Current_shown"]
    Accurate_window = window2["Accurate_rate"]
    i = 0
    ls, ls_res = arthmetic_task_generator(test_id)
    shown_window.update(value = "{} + {}".format(ls[i][0], ls[i][1]))
    start_time = time.time()
    print(ls)
    print(ls_res)
    while True:
        event, values = window2.read(timeout=0.001)
        if event in ['EXIT_BUTTON', sg.WIN_CLOSED]:
            window2.close()
            #window2.close()
            return 1
        elif event == 'Done_BUTTON':
            shown_window.update(ls[i][2])
            pulse_generator()
        elif event in ['<', '=', '>']:
            Response_record_list.append(event)
            generate_record_list.append(event == ls_res[i])
            new_value = {
                'data': event == ls_res[i],
                'timestamp': time.time()
            }
            value_list.append(new_value)
            i += 1
            shown_window.update(value = "{} + {}".format(ls[i][0], ls[i][1]))
        else:
            pass
        current_time = time.time()
        value_list = [value for value in value_list if current_time - value['timestamp'] <= max_age]
        total = 0
        for value in value_list:
            total += value['data']
        if len(value_list) == 0:
            rate = "---%"
        else:
            rate = "{:.3g}%".format(total/(len(value_list))*100)
        Accurate_window.update(value = rate)
        if time.time() - start_time > 120:
            window2.close()
            return 0
    ##################### GUI Handling #####################
for i in range(1):
    order = task_order_generator()
    print(order)
    for i in range(0,len(order)):
        exit_flag = Main_GUI(order[i])
        if exit_flag:
            break
now = datetime.now()
formatted_date_time = now.strftime("arthmetic_task_%Y_%m_%d_%H_%M_%S.txt")
save_lists_to_txt([order,generate_record_list, Response_record_list], formatted_date_time)