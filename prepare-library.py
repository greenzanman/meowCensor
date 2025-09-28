"""
Meow Library Preparation Script

This script automates the process of building a library of cat meow sounds for the MeowCensor project.
It performs the following steps:
1. Cleans any previous data.
2. Connects to the Freesound.org API to find and download short audio previews of meow sounds.
3. Processes each downloaded audio file to:
   - Trim leading and trailing silence.
   - Analyze the sound to determine its precise duration and average pitch.
4. Saves the cleaned audio as a WAV file in a '/processed' directory.
5. Catalogs the metadata for each sound (filename, path, duration, pitch) into a CSV database.
"""

# === SECTION 1: IMPORTS ===
# Standard library imports for file and system operations
import os
import shutil

# Third-party imports for data handling, audio processing, and API interaction
import numpy as np
import pandas as pd
import librosa
import soundfile as sf
import freesound
from dotenv import load_dotenv
from tqdm import tqdm


# === SECTION 2: CONFIGURATION ===
# Load environment variables from the .env file (should contain FREESOUND_API_KEY)
load_dotenv()

# --- Script Parameters ---
FREESOUND_API_KEY = os.getenv("FREESOUND_API_KEY")
DOWNLOAD_COUNT = 50  # The target number of meow sounds to download and process.
MAX_DURATION = 3     # The maximum duration (in seconds) of sounds to search for.

# --- Directory and File Paths ---
LIBRARY_DIR = "meow_library"
RAW_AUDIO_DIR = os.path.join(LIBRARY_DIR, "raw")
PROCESSED_AUDIO_DIR = os.path.join(LIBRARY_DIR, "processed")
DATABASE_FILE = "meow_database.csv"


# === SECTION 3: HELPER FUNCTIONS ===
def clean_directories():
    """Deletes and recreates the library directory to ensure a fresh start."""
    if os.path.exists(LIBRARY_DIR):
        print(f"Clearing old files in '{LIBRARY_DIR}'...")
        shutil.rmtree(LIBRARY_DIR)
    
    print("Creating fresh directories...")
    os.makedirs(RAW_AUDIO_DIR, exist_ok=True)
    os.makedirs(PROCESSED_AUDIO_DIR, exist_ok=True)
    print("Directories are clean and ready.")


# === SECTION 4: MAIN EXECUTION LOGIC ===
def main():
    """Main function to run the entire data preparation pipeline."""
    
    # --- Step 1: Initialize and Clean ---
    clean_directories()
    
    # Initialize the Freesound client with the API key
    client = freesound.FreesoundClient()
    client.set_token(FREESOUND_API_KEY, "token")
    
    # --- Step 2: Download Meow Sound Previews ---
    print("\nSearching for meow sounds on Freesound...")
    results = client.text_search(
        query="cat meow",
        filter=f"duration:[0 TO {MAX_DURATION}]",
        fields="id,name,previews,duration",
        page_size=DOWNLOAD_COUNT + 20  # Fetch more than needed to account for potential download failures.
    )

    print(f"Found {results.count} sounds. Downloading the first {DOWNLOAD_COUNT} previews...")
    
    downloaded_sound_paths = []
    # Use tqdm for a visual progress bar
    for sound in tqdm(results, total=DOWNLOAD_COUNT, desc="Downloading sounds"):
        # Stop once we've collected enough sounds
        if len(downloaded_sound_paths) >= DOWNLOAD_COUNT:
            break
        try:
            # Sanitize the sound name to create a valid filename
            safe_name = "".join(c for c in sound.name if c.isalnum() or c in (' ', '_')).rstrip()
            filename = f"{sound.id}_{safe_name.replace(' ', '_')}.mp3"
            output_path = os.path.join(RAW_AUDIO_DIR, filename)
            
            # Download the audio preview (works with simple API key) if it doesn't already exist
            if not os.path.exists(output_path):
                sound.retrieve_preview(RAW_AUDIO_DIR, filename)
                
            downloaded_sound_paths.append(output_path)
        except Exception as e:
            print(f"Could not download preview for sound {sound.id}: {e}")

    # --- Step 3: Process Audio Files and Extract Metadata ---
    print("\nProcessing downloaded audio files...")
    audio_metadata = []
    for raw_path in tqdm(downloaded_sound_paths, desc="Processing audio"):
        try:
            # Load the downloaded .mp3 file using librosa
            y, sr = librosa.load(raw_path, sr=None)
            
            # Automatically trim leading and trailing silence from the audio
            y_trimmed, _ = librosa.effects.trim(y, top_db=20)

            # If the audio is empty after trimming, skip to the next file
            if len(y_trimmed) == 0:
                continue
                
            # Estimate the fundamental frequency (pitch) using the pYIN algorithm
            f0, voiced_flag, _ = librosa.pyin(y_trimmed, fmin=librosa.note_to_hz('C2'), fmax=librosa.note_to_hz('C7'))
            
            # Calculate the average pitch, but only for the parts of the sound that are "voiced" (i.e., not silence)
            average_pitch_hz = np.nanmean(f0) if np.any(voiced_flag) else 0
            
            # Save the processed (trimmed) audio as a high-quality .wav file
            processed_filename = os.path.splitext(os.path.basename(raw_path))[0] + ".wav"
            processed_path = os.path.join(PROCESSED_AUDIO_DIR, processed_filename)
            sf.write(processed_path, y_trimmed, sr)
            
            # Get the exact duration of the trimmed audio
            duration = librosa.get_duration(y=y_trimmed, sr=sr)
            
            # Store all the extracted metadata for this sound
            audio_metadata.append({
                "filename": processed_filename,
                "path": processed_path,
                "duration_seconds": duration,
                "average_pitch_hz": average_pitch_hz
            })
        except Exception as e:
            print(f"Could not process file {raw_path}: {e}")
            print("This might be caused by a missing 'ffmpeg' installation. See https://ffmpeg.org/download.html")

    # --- Step 4: Save Metadata to CSV Database ---
    if audio_metadata:
        # Convert the list of dictionaries into a pandas DataFrame
        df = pd.DataFrame(audio_metadata)
        
        # Save the DataFrame to a CSV file, which will serve as our meow database
        df.to_csv(DATABASE_FILE, index=False)
        
        print(f"\n✅ Processing complete!")
        print(f"Meow database created at: {DATABASE_FILE}")
        print(f"Total processed files: {len(df)}")
    else:
        print("\n❌ Processing failed. No audio files were successfully processed.")

# This standard Python construct ensures that the main() function is called only when the script is executed directly.
if __name__ == "__main__":
    main()