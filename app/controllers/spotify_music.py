import random
import os
import pygame
from youtubesearchpython import VideosSearch
import threading
import speech_recognition as sr

from audio_functions import voice_to_text

# Initialize the recognizer
recognizer = sr.Recognizer()

# Path to the directory with music files
music_directory = "C:/Users/sairo/Music"

# Initialize Pygame Mixer
pygame.mixer.init()


# Function to play a random song
def play_random_song():
    songs = [song for song in os.listdir(music_directory) if song.endswith(".mp3")]
    if songs:
        random_song = random.choice(songs)
        song_path = os.path.join(music_directory, random_song)
        print(f"Now playing: {random_song}")
        pygame.mixer.music.load(song_path)
        pygame.mixer.music.play()
    else:
        print("No songs found in the directory.")


# Function to stop the music
def stop_music():
    pygame.mixer.music.stop()
    print("Music stopped.")


def search_youtube(query):
    videos_search = VideosSearch(query, limit=1)
    search_result = videos_search.result()

    if search_result["result"]:
        video_info = search_result["result"][0]
        video_link = video_info["link"]
        return video_link
    else:
        return None


# Function to process the recognized command
def process_command(command):
    if "play music" in command:
        play_random_song()
    elif "stop music" in command:
        stop_music()
    elif "exit" in command or "quit" in command:
        print("Exiting the program.")
        # Implement a way to safely terminate the listening thread.
    else:
        print("Command not recognized.")


# Flag to indicate that the application is running
running = True


# Function to handle voice commands using threading
def handle_voice_commands():
    global running
    while running:
        # Call your existing voice_to_text() function
        result = voice_to_text()
        if result.get("transcription"):
            process_command(result["transcription"])
        if result.get("transcription") in ["exit", "quit"]:
            break


# Start the voice command handling thread
voice_thread = threading.Thread(target=handle_voice_commands)
voice_thread.start()

# Main program loop (for example, a simple text interface)
while running:
    user_input = input("Enter a command: ")
    if user_input.lower() == "play":
        play_random_song()
    elif user_input.lower() == "stop":
        stop_music()
    elif user_input.lower() in ["exit", "quit"]:
        running = False  # Set the running flag to False to stop the threads
        print("Exiting the program.")

# Wait for the voice command thread to finish
voice_thread.join()
# Stop any music that is playing
stop_music()
