# -*- coding: utf-8 -*-
"""
Created on Tue Oct 31 11:08:27 2023

@author: leyu3109
"""
import pygame
import time

# Set the screen size
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

# Initialize pygame
pygame.init()

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Set the maximum intensity (0-255)
MAX_INTENSITY = 255

# Set the list of flash frequencies in Hz
FLASH_FREQ = [5, 8, 10, 12]  # List of frequencies
FLASH_DURATION = 40  # Total duration in seconds

# Calculate the time interval between each flash in seconds
FLASH_INTERVALS = [1 / freq for freq in FLASH_FREQ]

# Get the current time in seconds
start_time = time.time()

# Set the initial screen color to black
screen_color = (0, 0, 0)

# Define the cross color
cross_color = (0, 0, 0)  # Red cross color

# Initialize variables to track the current frequency
current_flash_state = 0

# Divide FLASH_DURATION into equal parts based on the number of frequencies
num_parts = len(FLASH_FREQ)
part_duration = FLASH_DURATION / num_parts
current_part = 0

# Start the main loop
while current_part <= num_parts:
    # Get the current time in seconds
    current_time = time.time()

    # Calculate the elapsed time in seconds within the current part
    elapsed_time = current_time - start_time - current_part * part_duration
    print(elapsed_time)
    # Check if it's time to switch to the next part
    if elapsed_time >= part_duration:
        current_part += 1

    # Calculate the current frequency
    current_frequency = FLASH_FREQ[current_part]
    print(current_frequency)
    # Check if it's time to flash the screen
    if elapsed_time % (1 / current_frequency) < (1 / (2 * current_frequency)):
        # Set the screen color to maximum intensity
        screen_color = (MAX_INTENSITY, MAX_INTENSITY, MAX_INTENSITY)
    else:
        # Set the screen color to black
        screen_color = (0, 0, 0)

    # Fill the screen with the current color
    screen.fill(screen_color)

    # Define the length of the cross lines
    cross_length = min(SCREEN_WIDTH, SCREEN_HEIGHT) // 32

    # Draw a cross in the middle of the screen
    cross_width = 5
    pygame.draw.line(screen, cross_color, (SCREEN_WIDTH // 2 - cross_length, SCREEN_HEIGHT // 2),
                     (SCREEN_WIDTH // 2 + cross_length, SCREEN_HEIGHT // 2), cross_width)
    pygame.draw.line(screen, cross_color, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - cross_length),
                     (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + cross_length), cross_width)

    # Update the screen
    pygame.display.flip()

# Quit pygame
pygame.quit()

