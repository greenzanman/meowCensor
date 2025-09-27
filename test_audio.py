import speech_recognition as sr
from pydub import AudioSegment
import os

# Name of your audio file
AUDIO_FILE = "test.mp3" # Change this to your file name

# Convert mp3 to wav if needed (pydub requires ffmpeg for this)
if AUDIO_FILE.endswith(".mp3"):
    sound = AudioSegment.from_mp3(AUDIO_FILE)
    wav_file = "temp.wav"
    sound.export(wav_file, format="wav")
else:
    wav_file = AUDIO_FILE

# Use the SpeechRecognition library
r = sr.Recognizer()
with sr.AudioFile(wav_file) as source:
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

# Clean up temp file
if os.path.exists("temp.wav"):
    os.remove("temp.wav")