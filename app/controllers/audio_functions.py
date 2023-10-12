import os
from pydub import AudioSegment
import speech_recognition as sr
from pydub.silence import split_on_silence

recognizer = sr.Recognizer()


def voice_to_text():
    """recording the sound"""
    with sr.Microphone() as source:
        print("Adjusting noise ")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("Recording for 4 seconds")
        recorded_audio = recognizer.listen(source, timeout=4)
        print("Done recording")
    """ Recorgnizing the Audio """
    try:
        print("Recognizing the text")
        text = recognizer.recognize_google(recorded_audio, language="en-US")
        print("Decoded Text : {}".format(text))

    except Exception as ex:
        print(ex)


def load_chunks(filename):
    long_audio = AudioSegment.from_mp3(filename)
    audio_chunks = split_on_silence(
        long_audio, min_silence_len=1800, silence_thresh=-17
    )
    return audio_chunks


def get_audio_lyrics(audio_file):
    for audio_chunk in load_chunks(audio_file):
        audio_chunk.export("temp", format="wav")
        with sr.AudioFile("temp") as source:
            audio = recognizer.listen(source)
            try:
                text = recognizer.recognize_google(audio)
                print("Chunk : {}".format(text))
            except Exception as ex:
                print("Error occured")
                print(ex)
    print("++++++")
