# -*- coding: utf-8 -*-
"""
Created on Fri Oct  6 18:20:38 2023

@author: leyu3109
"""

import time
import random
import datetime
from pulse_generator import pulse_generator

def run_pulse_generator():
    # Record the start time
    start_time = time.time()
    for i in range(10):
        # Call the pulse_generator function
        pulse_generator()

        # Calculate the time elapsed
        end_time = time.time()
        elapsed_time = end_time - start_time

        # Convert elapsed time to "MM:SS:ms" format
        elapsed_time_str = str(datetime.timedelta(seconds=elapsed_time))

        print(f"Run {i + 1}: {elapsed_time_str}")

        # Generate a random pause duration between 1 and 5 seconds
        pause_duration = random.uniform(800,1000)
        time.sleep(pause_duration/1000)

if __name__ == "__main__":
    run_pulse_generator()
