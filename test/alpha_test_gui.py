# -*- coding: utf-8 -*-
"""
Created on Fri Sep 29 16:40:12 2023

@author: leyu3109
"""

import PySimpleGUI as sg
import time
import winsound
from pulse_generator import pulse_generator
import threading

# Constants
WAITING_TIME_INITIAL = 15
TEST_TOTAL = 5
TEST_LENGTH = 20
TEST_INTERVAL = 40

def update_gui(window, remaining_time, eye_close, test_number, counting, started):
    window["Timing Counting"].update(value=remaining_time)
    window["Eye Control"].update(value="Eye Close" if eye_close else "Eye Open", text_color="Red" if eye_close else "Black")
    window["Test_number"].update(value=test_number)
    window["Start_BUTTON"].update(text="Stop" if started else "Start")

def main_gui():
    sg.theme("Default1")
    
    layout = [
        [sg.Text("Test: ", font=("Times New Roman", 52)), sg.Text("1", key="Test_number", font=("Times New Roman", 52))],
        [sg.Text(WAITING_TIME_INITIAL, key="Timing Counting", font=("Times New Roman", 52))],
        [sg.Text("Eye Open", key="Eye Control", font=("Times New Roman", 52))],
        [sg.Button('Start', key='Start_BUTTON', size=(5, 2)), sg.Button('Exit', key='EXIT_BUTTON', size=(5, 2))]
    ]

    window = sg.Window("Counting", layout, finalize=True, resizable=True)
    
    counting = False
    eye_close = False
    test_number = 1
    started = False
    testing_finialize = False
    remaining_time = WAITING_TIME_INITIAL
    #pulse_thread = threading.Thread(target=pulse_generator)
    
    while True:
        event, values = window.read(timeout=0.1)

        if event in ['EXIT_BUTTON', sg.WIN_CLOSED]:
            window.close()
            return

        if event == 'Start_BUTTON':
            if started:
                remaining_time = WAITING_TIME_INITIAL
                test_number = 1
                counting = False
                started = False
                eye_close = False
            else:
                counting = True
                waiting_time = WAITING_TIME_INITIAL
                started = True
                start_time = time.time()

        if counting:
            elapsed_time = time.time() - start_time
            remaining_time = max(0, waiting_time - int(elapsed_time))

            if remaining_time == 0:
                #pulse_thread.start()
                pulse_generator()
                counting = False
                waiting_time = TEST_LENGTH
                eye_close = True
                start_time = time.time()

        if eye_close:
            elapsed_time = time.time() - start_time
            remaining_time = max(0, TEST_LENGTH - int(elapsed_time))

            if remaining_time == 0:
                eye_close = False
                counting = True
                waiting_time = TEST_INTERVAL
                start_time = time.time()
                winsound.Beep(440, 1000)
                if test_number >= TEST_TOTAL:
                    testing_finialize = True
                    start_time = time.time()
                    counting = False
                    eye_close = False
                else:
                    test_number += 1
                    
        if testing_finialize:
             elapsed_time = time.time() - start_time
             remaining_time = max(0, 10 - int(elapsed_time))

        update_gui(window, remaining_time, eye_close, test_number, counting, started)

if __name__ == "__main__":
    main_gui()