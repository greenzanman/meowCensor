import os
import sys

print("--- DEBUG INFO ---")
print(f"Python Executable: {sys.executable}")
print(f"Working Directory: {os.getcwd()}")
print("Python Search Paths (sys.path):")
for path in sys.path:
    print(f"  - {path}")
print("--- END DEBUG INFO ---\n")

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
MAX_DURATION = 3     # Max duration of sounds in seconds
RAW_AUDIO_DIR = "meow_library/raw"
PROCESSED_AUDIO_DIR = "meow_library/processed"
DATABASE_FILE = "meow_database.csv"

# --- Initialize Freesound Client ---
client = freesound.FreesoundClient()
client.set_token(FREESOUND_API_KEY, "token")

# --- Create Directories ---
os.makedirs(RAW_AUDIO_DIR, exist_ok=True)
os.makedirs(PROCESSED_AUDIO_DIR, exist_ok=True)


# --- Download Meow Sounds ---
print("Searching for meow sounds on Freesound...")
results = client.text_search(
    query="cat meow",
    filter=f"duration:[0 TO {MAX_DURATION}]",
    fields="id,name,previews,download,duration"
)

print(f"Found {results.count} sounds. Downloading the first {DOWNLOAD_COUNT}...")

downloaded_sounds = []
for sound in tqdm(results, total=DOWNLOAD_COUNT, desc="Downloading sounds"):
    if len(downloaded_sounds) >= DOWNLOAD_COUNT:
        break
    try:
        filename = f"{sound.id}_{sound.name.replace(' ', '_')}.wav"
        output_path = os.path.join(RAW_AUDIO_DIR, filename)
        if not os.path.exists(output_path): # Avoid re-downloading
            # Using retrieve_preview instead of retrieve to avoid OAuth2 requirement
            sound.retrieve_preview(RAW_AUDIO_DIR, filename)
        downloaded_sounds.append(output_path)
    except Exception as e:
        print(f"Could not download sound {sound.id}: {e}")



# --- Process Audio Files ---
audio_metadata = []

for raw_path in tqdm(downloaded_sounds, desc="Processing audio"):
    try:
        # Load audio file
        y, sr = librosa.load(raw_path, sr=None)

        # Trim leading and trailing silence
        y_trimmed, _ = librosa.effects.trim(y, top_db=20)

        # Skip if audio is empty after trimming
        if len(y_trimmed) == 0:
            continue

        # Save the processed audio
        processed_filename = os.path.basename(raw_path)
        processed_path = os.path.join(PROCESSED_AUDIO_DIR, processed_filename)
        sf.write(processed_path, y_trimmed, sr)

        # Get duration of the trimmed audio
        duration = librosa.get_duration(y=y_trimmed, sr=sr)

        # Add metadata to our list
        audio_metadata.append({
            "filename": processed_filename,
            "path": processed_path,
            "duration_seconds": duration,
        })
    except Exception as e:
        print(f"Could not process file {raw_path}: {e}")



# --- Save Metadata to CSV ---
# Create a pandas DataFrame and save to CSV
df = pd.DataFrame(audio_metadata)
df.to_csv(DATABASE_FILE, index=False)

print("\nProcessing complete!")
print(f"Meow database created at: {DATABASE_FILE}")
print(f"Total processed files: {len(df)}")