# -*- coding: utf-8 -*-
"""
Created on Fri Mar 31 11:40:44 2023

@author: yulep
"""

import time
import winsound

time.sleep(35)  # Wait for 20 seconds before starting the loop

for i in range(4):
    start_time = time.time()  # Record the start time of the loop
    
    winsound.Beep(440, 1000)  # Play a beep sound (440 Hz for 1 second)
    elapsed_time = time.time() - start_time  # Calculate the elapsed time of the loop
    
    if elapsed_time < 60:  # If the loop took less than 1 minute, wait for the remaining time
        time.sleep(60 - elapsed_time)  # Wait for the remaining time
winsound.Beep(440, 1000)  # Play a beep sound (440 Hz for 1 second)