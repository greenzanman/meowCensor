# /agents/audio_surgeon_agent.py

import os
from typing import List, Dict

import pandas as pd
from pydub import AudioSegment
from pydub.effects import speedup


# --- 1. ROBUST PATH CONFIGURATION ---
# This section creates reliable, absolute paths to necessary files.
# By starting from the location of this script (__file__), it ensures that the
# paths work correctly regardless of where the main application is run from.

# Get the absolute path to the project's root directory (one level up from 'agents').
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Construct the full path to the meow database CSV file in the root directory.
DEFAULT_MEOW_DB_PATH = os.path.join(PROJECT_ROOT, "meow_database.csv")

# Construct the full path to the folder containing the processed WAV meow files.
MEOW_LIBRARY_PATH = os.path.join(PROJECT_ROOT, "meow_library", "processed")


# --- 2. CORE SPLICING FUNCTION ---
def splice_audio(audio_path: str, censor_times: List[Dict], meow_db_path: str = DEFAULT_MEOW_DB_PATH) -> str:
    """
    Replaces specified segments of an audio file with the best-matching meow sound.

    This function iterates through a list of timestamps, cuts out the corresponding
    audio segments, and intelligently replaces them with meow sounds from the library
    that have been stretched to fit the required duration perfectly.
    """
    print("--- Initializing the Audio Surgeon Agent ---")
    
    # --- Input Validation ---
    # Failsafe checks to ensure the required audio file and database exist.
    if not os.path.exists(audio_path):
        print(f"❌ Fatal Error: Source audio file not found at '{audio_path}'")
        return ""
        
    if not os.path.exists(meow_db_path):
        print(f"❌ Fatal Error: Meow database not found at '{meow_db_path}'")
        return ""

    # --- File Loading ---
    # Load the meow database and the original audio file into memory.
    try:
        meow_db = pd.read_csv(meow_db_path)
        original_audio = AudioSegment.from_file(audio_path)
        print("✅ Successfully loaded meow database and source audio.")
    except Exception as e:
        print(f"❌ Fatal Error: Could not process source files. Details: {e}")
        return ""

    # --- Audio Reconstruction Loop ---
    # Sort timestamps to process the audio in chronological order.
    censor_times.sort(key=lambda x: x['start_time'])
    
    # `last_end_time_ms` tracks the end of the last processed segment.
    last_end_time_ms = 0
    # `final_audio` starts as an empty clip and is built up piece by piece.
    final_audio = AudioSegment.silent(duration=0)

    # Process each identified swear word segment.
    for i, segment in enumerate(censor_times):
        # Convert timestamps from seconds (float) to milliseconds (integer).
        start_ms = int(segment['start_time'] * 1000)
        end_ms = int(segment['end_time'] * 1000)
        
        # 1. Append the clean audio *before* the current swear word.
        final_audio += original_audio[last_end_time_ms:start_ms]
        
        # Calculate the exact duration needed for the replacement meow.
        duration_needed_s = (end_ms - start_ms) / 1000.0
        duration_needed_ms = end_ms - start_ms

        # Skip if the segment has no duration (shouldn't happen, but a good failsafe).
        if duration_needed_s <= 0:
            continue

        # 2. Find and prepare the best meow for replacement.
        # Find the meow in the database with the closest duration to the word being replaced.
        meow_db['duration_diff'] = abs(meow_db['duration_seconds'] - duration_needed_s)
        best_meow_info = meow_db.loc[meow_db['duration_diff'].idxmin()]
        
        # Construct the full path to the selected meow WAV file.
        meow_file_name = os.path.basename(best_meow_info['path'])
        meow_audio_path = os.path.join(MEOW_LIBRARY_PATH, meow_file_name)
        
        if not os.path.exists(meow_audio_path):
            print(f"  > ❌ Warning: Meow file not found: {meow_audio_path}. Skipping segment.")
            continue

        # Load the chosen meow sound.
        meow_audio = AudioSegment.from_file(meow_audio_path)
        
        # --- DYNAMIC VOLUME NORMALIZATION ---
        # Get the audio segment of the original word that is being replaced.
        original_word_segment = original_audio[start_ms:end_ms]

        # Check if the segment has sound before trying to measure it.
        if original_word_segment.dBFS > -float('inf'):
            # Calculate the difference between the PEAK loudness of the word and the meow.
            # .max_dBFS measures the loudest single point in the audio clip.
            dBFS_difference = original_word_segment.max_dBFS - meow_audio.max_dBFS

            # Apply the calculated gain to the meow audio to match the word's peak volume.
            normalized_meow = meow_audio.apply_gain(dBFS_difference)
        else:
            # If the original segment is pure silence, don't change the meow's volume.
            normalized_meow = meow_audio
        
        # Create a silent audio clip of the exact length needed.
        replacement_segment = AudioSegment.silent(duration=duration_needed_ms)

        # Time-stretch the meow to fit the duration of the swear word perfectly.
        original_meow_duration_s = len(normalized_meow) / 1000.0
        if original_meow_duration_s > 0:
            playback_speed = original_meow_duration_s / duration_needed_s
            playback_speed = max(0.5, min(2.0, playback_speed))
            
            # Use the new 'normalized_meow' for stretching.
            stretched_meow = speedup(normalized_meow, playback_speed=playback_speed, chunk_size=150, crossfade=25)
            replacement_segment = replacement_segment.overlay(stretched_meow)

        final_audio += replacement_segment
        print(f"  > Replaced segment #{i+1} ({duration_needed_s:.2f}s) with meow '{meow_file_name}'.")
        
        last_end_time_ms = end_ms

    # 4. Append any remaining clean audio from after the last swear word.
    final_audio += original_audio[last_end_time_ms:]
    
    # --- File Export ---
    # Create a new filename for the censored output (e.g., 'my_audio_censored.wav').
    base, ext = os.path.splitext(os.path.basename(audio_path))
    output_filename = f"{base}_censored.wav"
    output_path = os.path.join(PROJECT_ROOT, output_filename)
    
    # Save the final, reconstructed audio to a new file.
    try:
        final_audio.export(output_path, format="wav")
        print(f"\n✅ Audio surgery complete. File saved to: {output_path}")
        return output_path
    except Exception as e:
        print(f"❌ Fatal Error: Could not export the final audio file. Details: {e}")
        return ""