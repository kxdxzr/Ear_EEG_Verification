# -*- coding: utf-8 -*-
"""
Created on Fri Sep 29 15:20:04 2023

@author: leyu3109
"""

from gtts import gTTS
import pygame
import wave

def generate_and_save_sentence_audio(sentence, output_filename="output.wav"):
    # Generate speech from the given sentence
    tts = gTTS(text=sentence, lang="en")

    # Save the speech as a temporary MP3 file
    tts.save("temp.mp3")

    # Initialize pygame mixer
    pygame.mixer.init()

    # Load the temporary MP3 file
    pygame.mixer.music.load("temp.mp3")

    # Initialize the WAV file
    wave_output = wave.open(output_filename, 'w')
    wave_output.setnchannels(1)  # Mono audio
    wave_output.setsampwidth(2)  # 16-bit audio
    wave_output.setframerate(44100)  # 44.1 kHz sample rate

    # Play the audio and write it to the WAV file simultaneously
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pass  # Wait for audio to finish playing

    # Open the temporary MP3 file and read its audio data
    with open("temp.mp3", "rb") as mp3_file:
        mp3_data = mp3_file.read()

    # Write the MP3 audio data to the WAV file
    wave_output.writeframes(mp3_data)

    # Close the WAV file
    wave_output.close()

if __name__ == "__main__":
    sentence = "Hello, this is a test sentence."
    generate_and_save_sentence_audio(sentence)

