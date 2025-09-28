🐱 MeowCensor
A Python application that automatically replaces profanity in audio files with cat "meow" sounds. The system uses a multi-agent AI pipeline to transcribe audio, identify naughty words, and perform audio surgery to replace them with dynamically volume-matched meows.

It features a friendly web UI for easy use and a command-line interface for scripting.

Features
Dual Input: Upload an existing audio file (.mp3, .wav) or record audio directly in the browser.

AI-Powered Censorship: Utilizes the Google Gemini model to intelligently identify a wide range of profane words, not just a fixed keyword list.

Natural Sound Replacement: Each meow is selected from a library based on duration and is dynamically adjusted to match the peak volume of the word it's replacing, ensuring a seamless and natural blend.

Web & Command-Line Interface: Use the simple Streamlit web app for ease of use or run the script from the command line for automation.

How It Works
The application operates as a three-stage pipeline:

Transcriber Agent: openai-whisper transcribes the source audio, generating word-level timestamps.

Censor Agent: The transcript is sent to a Google Gemini model via the Agent Development Kit (google-adk) to identify the timestamps of profane words.

Audio Surgeon Agent: pydub slices the original audio, finds the best-fitting meow from a pre-analyzed library, normalizes its volume, time-stretches it, and splices it into the final audio track.

Setup and Installation
Follow these steps to get the project running on your local machine.

1. Prerequisites
Python (v3.10 or higher)

Git

FFmpeg: This is required by pydub for audio processing. You can download it from ffmpeg.org or install it with a package manager like Chocolatey (choco install ffmpeg) on Windows.

2. Clone the Repository
git clone <your-repository-url>
cd meowCensor

3. Set Up the Virtual Environment
This creates an isolated environment for the project's Python packages.

# Create the virtual environment
python -m venv venv

# Activate it (you must do this every time you open a new terminal)
./venv/Scripts/activate

Your terminal prompt should now start with (venv).

4. Install Dependencies
Install all the required Python packages using the requirements.txt file.

pip install -r requirements.txt

5. Configure API Keys
The project requires API keys for Freesound (to build the meow library) and Google Gemini (for the Censor Agent).

Create a file named .env in the root of the project directory (meowCensor/.env).

Add your API keys to this file. Do not include quotes.

FREESOUND_API_KEY="cRJ9PFrxQ6R4U6TIIvUlbSAP9cqW31cVSAQoz8GL"
GEMINI_API_KEY="AIzaSyDDgzNb_dHv3J-d7eIIA8sqIsVNWFZm5lg"

(Note: You should generate your own keys for a real application.)

6. Build the Meow Library
This is a one-time step. Run the prepare-library.py script to download and process the meow sounds from Freesound.org.

python prepare-library.py

This will create the meow_library folder and the meow_database.csv file.

Usage
You can run the application in two ways:

1. Web Interface (Streamlit)
Launch the web application with the following command:

streamlit run app.py

This will open the MeowCensor UI in your web browser.

2. Command-Line Interface (CLI)
To process a file directly from your terminal:

python app.py your_audio_file.mp3

Replace your_audio_file.mp3 with the path to the audio file you want to censor. The output file will be saved in the root directory.