# -*- coding: utf-8 -*-
"""
Created on Fri Sep 29 16:30:36 2023

@author: leyu3109
"""

import pygame

def play_sound(sound_file):
    # Initialize the pygame mixer
    pygame.mixer.init()
    
    # Create a pygame sound object from the saved sound file
    sound = pygame.mixer.Sound(sound_file)
    
    # Play the sound
    sound.play()
    
    # You can add a delay if you want to play the sound for a specific duration
    # pygame.time.delay(5000)  # This would play the sound for 5 seconds (5000 milliseconds)
    
    # Wait for the sound to finish playing
    pygame.time.wait(int(sound.get_length() * 1000))  # Convert sound duration to milliseconds
    
    # Quit the pygame mixer (clean up resources)
    pygame.quit()