# -*- coding: utf-8 -*-
"""
Created on Mon Mar 13 13:20:37 2023

@author: yulep
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

# Set the frequency of the flashing in Hz
FLASH_FREQ = 8

# Set the duration of the flashing in seconds
FLASH_DURATION = 20

# Calculate the time interval between each flash in seconds
FLASH_INTERVAL = 1 / FLASH_FREQ

# Get the current time in seconds
start_time = time.time()

# Set the initial screen color to black
screen_color = (0, 0, 0)

# Define the cross color
cross_color = (0, 0, 0)  # Red cross color

# Start the main loop
while True:
    # Get the current time in seconds
    current_time = time.time()

    # Calculate the elapsed time in seconds
    elapsed_time = current_time - start_time

    # Check if the flashing duration has passed
    if elapsed_time > FLASH_DURATION:
        break

    # Check if it's time to flash the screen
    if elapsed_time % FLASH_INTERVAL < (FLASH_INTERVAL / 2):
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
