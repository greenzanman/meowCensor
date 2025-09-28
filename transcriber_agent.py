# MeowCensor Project
# Phase 2, Step 2.1: Transcriber Agent
# This script is responsible for transcribing audio files and providing word-level timestamps.

# --- 1. IMPORTS & SETUP ---
import whisper
import os

# --- 2. MODEL INITIALIZATION ---
# Load the Whisper model once when the script starts. This is a performance optimization
# to avoid reloading the model every time the transcription function is called.
# The 'base' model offers a good balance between speed and accuracy for this project.
print("Initializing the Transcriber Agent...")
try:
    model = whisper.load_model("base")
    print("Whisper 'base' model loaded successfully. Agent is ready. 🚀")
except Exception as e:
    print(f"Fatal Error: Could not load Whisper model. {e}")
    model = None

# --- 3. CORE TRANSCRIPTION LOGIC ---
def transcribe_audio(file_path: str) -> list[dict]:
    """
    Transcribes an audio file using Whisper to generate word-level timestamps.

    This function takes the path to an audio file, processes it, and returns a
    structured list of every word spoken along with its start and end time.

    Args:
        file_path (str): The full path to the audio file (e.g., .mp3, .wav).

    Returns:
        list[dict]: A list of dictionaries, where each dictionary represents a word
                    and contains {'word': str, 'start': float, 'end': float}.
                    Returns an empty list if the model isn't loaded or an error occurs.
    """
    # Pre-computation check: Ensure the model is available.
    if not model:
        print("Whisper model is not available. Cannot transcribe.")
        return []
    
    # Pre-computation check: Ensure the audio file exists before processing.
    if not os.path.exists(file_path):
        print(f"Error: Audio file not found at '{file_path}'")
        return []

    print(f"Starting transcription for: {os.path.basename(file_path)}...")
    
    try:
        # Perform the transcription. 'word_timestamps=True' is crucial for this project.
        result = model.transcribe(file_path, word_timestamps=True)
        
        # Extract and format the word data from the raw result into a clean list.
        word_list = []
        for segment in result['segments']:
            for word_data in segment['words']:
                word_list.append({
                    'word': word_data['word'].strip(),
                    'start': word_data['start'],
                    'end': word_data['end']
                })
                
        print("Transcription completed successfully.")
        return word_list

    except Exception as e:
        print(f"An unexpected error occurred during transcription: {e}")
        return []

# --- 4. DIRECT EXECUTION FOR TESTING ---
# This block runs only when you execute the script directly (e.g., `python transcriber_agent.py`).
# It's used for testing the `transcribe_audio` function in isolation.
if __name__ == '__main__':
    # --- Test Setup ---
    # To test, place an audio file (e.g., 'test.mp3') in the same directory as this script.
    sample_file_to_test = "test.mp3" 
    
    print("\n--- [Running Standalone Test] ---")
    if os.path.exists(sample_file_to_test):
        # --- Function Call ---
        transcript = transcribe_audio(sample_file_to_test)
        
        # --- Test Results ---
        if transcript:
            print("\n✅ Test Passed. Transcription Result (first 15 words):")
            for item in transcript[:15]:
                # The .2f formats the time to two decimal places for readability.
                print(f"  - Word: \"{item['word']:<15}\" Start: {item['start']:.2f}s, End: {item['end']:.2f}s")
        else:
            print("\n❌ Test Failed. Transcription returned an empty list.")
    else:
        print(f"\n🟡 Test Skipped. Please create a file named '{sample_file_to_test}' to run the test.")