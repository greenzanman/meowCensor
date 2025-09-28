import speech_recognition as sr
from pydub import AudioSegment
import os
import subprocess
import sys

AUDIO_FILE = 'temp_audio/audio.wav'

# Use the SpeechRecognition library
r = sr.Recognizer()
with sr.AudioFile(AUDIO_FILE) as source:
    print("Listening to audio file...")
    audio = r.record(source) # Read the entire audio file

    try:
        # Using Google's free web-speech API for a quick test
        text = r.recognize_google(audio)
        print(f"Transcription: {text}")
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")

# Clean up files
if os.path.exists("temp.wav"):
    os.remove("temp.wav")
    