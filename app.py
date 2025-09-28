# MeowCensor Project
# Final Merged Application

# --- 1. IMPORTS ---
import streamlit as st
import os
import sys
import argparse
import base64
from tempfile import NamedTemporaryFile
from typing import List, Dict
from audio_recorder_streamlit import audio_recorder

# Import agent functions and data models
from agents.transcriber_agent import transcribe_audio
from agents.censor_agent import find_swear_words
from agents.audio_surgeon_agent import splice_audio 
from data_models import Transcript, Word

# --- 2. MERGED: UI STYLING HELPERS (from site_meow.py) ---
# These functions handle the custom background and fonts.
def get_base64_of_bin_file(bin_file):
    # Check if the file exists before trying to open it
    if not os.path.exists(bin_file):
        st.warning(f"Asset file not found: {bin_file}. Styling may be incomplete.")
        return None
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_page_styling():
    """Applies custom CSS for background, fonts, and styles the app."""
    # Paths to asset files
    font_path = os.path.join("assets", "Mouly.woff2")
    background_image_path = os.path.join("assets", "cat_bg.png")

    # Read font data and encode it
    font_binary = get_base64_of_bin_file(font_path)
    bg_image_binary = get_base64_of_bin_file(background_image_path)
    
    # Return early if assets are missing
    if not font_binary or not bg_image_binary:
        return

    # Custom CSS block
    page_styling = f'''
    <style>
        @font-face {{
            font-family: 'Mouly';
            src: url("data:application/font-woff2;base64,{font_binary}") format('woff2');
        }}
        .stApp {{
            background-image: url("data:image/png;base64,{bg_image_binary}");
            background-size: contain;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        h1, h2, h3 {{
            text-align: center;
            font-family: 'Mouly', cursive, sans-serif;
        }}
        .stButton>button {{
            border-radius: 20px;
            border: 2px solid #FFDDC1;
            background-color: #FF6B6B;
            color: white;
            padding: 10px 24px;
            font-family: 'Mouly', cursive, sans-serif;
            font-size: 1.2em;
        }}
    </style>
    '''
    st.markdown(page_styling, unsafe_allow_html=True)


# --- 3. BACKEND: WORKFLOW ORCHESTRATOR (from app.py) ---
def run_censor_workflow(input_audio_path: str, progress_bar) -> str:
    """Executes the full MeowCensor pipeline, updating a progress bar."""
    
    # Helper for logging status
    def log_status(message, progress):
        print(message) # Log to console
        if progress_bar:
            progress_bar.progress(progress, text=message)

    log_status("Step 1/3: Transcribing audio with Whisper... ✍️", 0.1)
    transcript_data = transcribe_audio(input_audio_path)
    if not transcript_data:
        st.error("Transcription failed. Could not process the audio.")
        return None

    word_objects = [Word(word=item['word'], start_time=item['start'], end_time=item['end']) for item in transcript_data]
    transcript_model = Transcript(words=word_objects)

    log_status("Step 2/3: Identifying words to censor with the AI Agent... 🕵️", 0.5)
    swear_words: List[Word] = find_swear_words(transcript_model)
    censor_times: List[Dict] = [word.model_dump() for word in swear_words]

    if not censor_times:
        log_status("No profanity was found! Returning original audio. 🎉", 1.0)
        return input_audio_path

    log_status("Step 3/3: Performing audio surgery... 🐱‍⚕️", 0.8)
    output_path = splice_audio(input_audio_path, censor_times)
    if not output_path:
        st.error("Audio splicing failed. Could not generate the final file.")
        return None
        
    log_status("Censoring complete! ✅", 1.0)
    return output_path


# --- 4. MERGED: STREAMLIT UI FUNCTION ---
def run_streamlit_app():
    """Runs the main Streamlit application UI."""
    # Apply the custom styling first
    set_page_styling()

    st.title("Meow-Censor")
    st.header("A cuter way to deal with unsavory language.")
    st.write("") # Spacer

    # --- Two columns for input options ---
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Upload Audio")
        uploaded_file = st.file_uploader(
            "Upload your audio file (.mp3, .wav)",
            type=['mp3', 'wav'],
            label_visibility="collapsed"
        )

    with col2:
        st.subheader("Record Audio")
        recorded_audio = audio_recorder(
            text="Click to Record",
            recording_color="#FF6B6B",
            neutral_color="#FFDDC1",
            icon_name="microphone",
            pause_threshold=3.0,
        )

    # --- Processing Logic ---
    audio_bytes_to_process = None
    if uploaded_file:
        audio_bytes_to_process = uploaded_file.getvalue()
        st.subheader("Your Uploaded Audio")
        st.audio(audio_bytes_to_process)
    elif recorded_audio:
        audio_bytes_to_process = recorded_audio
        st.subheader("Your Recorded Audio")
        st.audio(audio_bytes_to_process)

    if st.button("MEOWIFY", use_container_width=True):
        if audio_bytes_to_process:
            # Use a progress bar for better UX
            progress_bar = st.progress(0, text="Starting the meowification process...")
            
            # Use NamedTemporaryFile for robust, safe file handling
            with NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
                tmp_file.write(audio_bytes_to_process)
                temp_input_path = tmp_file.name

            # Run the main workflow
            final_audio_path = run_censor_workflow(temp_input_path, progress_bar)

            # --- Display Results ---
            if final_audio_path:
                st.subheader("Censored Audio")
                with open(final_audio_path, "rb") as f:
                    final_audio_bytes = f.read()
                st.audio(final_audio_bytes, format='audio/wav')
                
                # Provide a download button
                st.download_button(
                    label="Download Censored File",
                    data=final_audio_bytes,
                    file_name=os.path.basename(final_audio_path),
                    mime="audio/wav",
                    use_container_width=True
                )
            else:
                st.error("The workflow failed. Please check the logs in your terminal.")

            # Clean up the temp file
            os.remove(temp_input_path)
        else:
            st.warning("Please upload or record some audio first!")


# --- 5. CLI ENTRY POINT (from app.py) ---
# This logic allows the script to be run from the command line as well.
if __name__ == "__main__":
    if len(sys.argv) > 1:
        print("--- MeowCensor CLI Mode ---")
        parser = argparse.ArgumentParser(description="Censor profanity in an audio file with meows.")
        parser.add_argument("input_file", help="The path to the audio file to censor.")
        args = parser.parse_args()

        if not os.path.exists(args.input_file):
            print(f"❌ Error: Input file not found at '{args.input_file}'")
        else:
            final_path = run_censor_workflow(args.input_file, progress_bar=None) # No progress bar in CLI
            if final_path:
                print(f"\n✅ Success! Censored audio saved to: {final_path}")
            else:
                print("\n❌ Workflow failed.")
    else:
        # If no arguments, default to starting the Streamlit app.
        run_streamlit_app()