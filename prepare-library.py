import os
import sys
import shutil
import numpy as np # NumPy is needed for pitch calculation
import freesound
import librosa
import pandas as pd
from dotenv import load_dotenv
from tqdm import tqdm
import soundfile as sf

# --- Configuration ---
load_dotenv()
FREESOUND_API_KEY = os.getenv("FREESOUND_API_KEY")
DOWNLOAD_COUNT = 50  # Number of meow sounds to download
MAX_DURATION = 3  # Maximum duration of sounds in seconds
LIBRARY_DIR = "meow_library"
RAW_AUDIO_DIR = os.path.join(LIBRARY_DIR, "raw")
PROCESSED_AUDIO_DIR = os.path.join(LIBRARY_DIR, "processed")
DATABASE_FILE = "meow_database.csv"

# --- Helper Function to Clean Directories ---
def clean_directories():
    """Deletes and recreates the library directory to ensure a fresh start."""
    if os.path.exists(LIBRARY_DIR):
        print(f"Clearing old files in '{LIBRARY_DIR}'...")
        shutil.rmtree(LIBRARY_DIR)
    os.makedirs(RAW_AUDIO_DIR, exist_ok=True)
    os.makedirs(PROCESSED_AUDIO_DIR, exist_ok=True)
    print("Directories are clean and ready.")

# --- Initialize Freesound Client ---
client = freesound.FreesoundClient()
client.set_token(FREESOUND_API_KEY, "token")

# --- Main Script Execution ---
clean_directories()

# --- Download Meow Sound Previews ---
print("\nSearching for meow sounds on Freesound...")
results = client.text_search(
    query="cat meow",
    filter=f"duration:[0 TO {MAX_DURATION}]",
    fields="id,name,previews,duration",
    page_size=DOWNLOAD_COUNT + 20 # Fetch more than needed to ensure we get enough
)

print(f"Found {results.count} sounds. Downloading the first {DOWNLOAD_COUNT} previews...")

downloaded_sound_paths = []
for sound in tqdm(results, total=DOWNLOAD_COUNT, desc="Downloading sounds"):
    if len(downloaded_sound_paths) >= DOWNLOAD_COUNT:
        break
    try:
        safe_name = "".join(c for c in sound.name if c.isalnum() or c in (' ', '_')).rstrip()
        filename = f"{sound.id}_{safe_name.replace(' ', '_')}.mp3"
        output_path = os.path.join(RAW_AUDIO_DIR, filename)

        if not os.path.exists(output_path):
            sound.retrieve_preview(RAW_AUDIO_DIR, filename)
            
        downloaded_sound_paths.append(output_path)
    except Exception as e:
        print(f"Could not download preview for sound {sound.id}: {e}")

# --- Process Audio Files ---
print("\nProcessing downloaded audio files...")
audio_metadata = []
for raw_path in tqdm(downloaded_sound_paths, desc="Processing audio"):
    try:
        # Load the downloaded .mp3 file
        y, sr = librosa.load(raw_path, sr=None)

        # Trim leading and trailing silence
        y_trimmed, _ = librosa.effects.trim(y, top_db=20)

        # Skip if audio is empty after trimming
        if len(y_trimmed) == 0:
            continue

        # Estimate pitch using the pYIN algorithm
        f0, voiced_flag, voiced_probs = librosa.pyin(y_trimmed, fmin=librosa.note_to_hz('C2'), fmax=librosa.note_to_hz('C7'))
        
        # Calculate the average pitch, ignoring unvoiced frames (where f0 is NaN)
        average_pitch_hz = np.nanmean(f0) if np.any(voiced_flag) else 0

        # Save the processed audio as a consistent .wav file
        processed_filename = os.path.splitext(os.path.basename(raw_path))[0] + ".wav"
        processed_path = os.path.join(PROCESSED_AUDIO_DIR, processed_filename)
        sf.write(processed_path, y_trimmed, sr)

        # Get duration of the trimmed audio
        duration = librosa.get_duration(y=y_trimmed, sr=sr)

        # Add metadata to our list
        audio_metadata.append({
            "filename": processed_filename,
            "path": processed_path,
            "duration_seconds": duration,
            "average_pitch_hz": average_pitch_hz
        })
    except Exception as e:
        print(f"Could not process file {raw_path}: {e}")
        print("This might be caused by a missing 'ffmpeg' installation. Please see https://ffmpeg.org/download.html for installation instructions.")

# --- Save Metadata to CSV ---
# Create a pandas DataFrame and save to CSV
if audio_metadata:
    df = pd.DataFrame(audio_metadata)
    df.to_csv(DATABASE_FILE, index=False)
    print(f"\n✅ Processing complete!")
    print(f"Meow database created at: {DATABASE_FILE}")
    print(f"Total processed files: {len(df)}")
else:
    print("\n❌ Processing failed. No audio files were successfully processed.")