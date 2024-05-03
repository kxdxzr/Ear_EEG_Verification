# -*- coding: utf-8 -*-
"""
Created on Fri Sep 29 15:20:04 2023

@author: leyu3109
"""
from gtts import gTTS
import pygame
import wave
import os

def generate_and_save_sentence_audio(sentence, output_filename="output.wav"):
    # Generate speech from the given sentence
    tts = gTTS(text=sentence, lang="en")

    # Specify the full path for the temporary MP3 file
    temp_mp3_path = os.path.join(os.path.dirname(__file__), "temp.mp3")

    # Save the speech as a temporary MP3 file
    tts.save(temp_mp3_path)

    # Initialize pygame mixer
    pygame.mixer.init()

    # Load the temporary MP3 file
    pygame.mixer.music.load(temp_mp3_path)

    # Initialize the WAV file
    wave_output = wave.open(output_filename, 'w')
    wave_output.setnchannels(1)  # Mono audio
    wave_output.setsampwidth(2)  # 16-bit audio
    wave_output.setframerate(44100)  # 44.1 kHz sample rate

    # Play the audio and write it to the WAV file simultaneously
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pass  # Wait for audio to finish playing

    # Close the WAV file
    wave_output.close()

    # Wait for the temporary MP3 file to be released by the mixer
    pygame.mixer.quit()

    # Delete the temporary MP3 file
    os.remove(temp_mp3_path)

if __name__ == "__main__":
    sentence = "Hello, this is a test sentence."
    generate_and_save_sentence_audio(sentence)

