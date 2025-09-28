# MeowCensor Project
# Phase 4: Integration and Final Touches

# --- 1. IMPORTS ---
import streamlit as st
import os
from tempfile import NamedTemporaryFile
from typing import List, Dict
import sys # NEW: To handle command-line arguments
import argparse # NEW: A better way to handle arguments

# Import agent functions from their new package location
from agents.transcriber_agent import transcribe_audio
from agents.censor_agent import find_swear_words
from agents.audio_surgeon_agent import splice_audio 

# Import the data models
from data_models import Transcript, Word

# --- 2. THE MAIN WORKFLOW ORCHESTRATOR (UPDATED) ---
def run_censor_workflow(input_audio_path: str, ui_mode: bool = True) -> str:
    """
    Executes the full MeowCensor pipeline.

    Args:
        input_audio_path (str): The path to the user-uploaded audio file.
        ui_mode (bool): If True, prints status to Streamlit. If False, prints to console.
    """
    # Helper function for printing status
    def log_status(message):
        if ui_mode:
            st.write(message)
        else:
            print(message)

    log_status("Step 1: Transcribing audio with Whisper... ✍️")
    transcript_data = transcribe_audio(input_audio_path)
    if not transcript_data:
        log_status("❌ Transcription failed. Could not process the audio.")
        return None

    word_objects = [Word(word=item['word'], start_time=item['start'], end_time=item['end']) for item in transcript_data]
    transcript_model = Transcript(words=word_objects)

    log_status("Step 2: Identifying words to censor with the ADK Agent... 🕵️")
    swear_words: List[Word] = find_swear_words(transcript_model)
    censor_times: List[Dict] = [word.model_dump() for word in swear_words]

    if not censor_times:
        log_status("✅ No profanity was found! Returning the original audio. 🎉")
        return input_audio_path

    log_status("Step 3: Performing audio surgery... 🐱‍⚕️")
    output_path = splice_audio(input_audio_path, censor_times)
    if not output_path:
        log_status("❌ Audio splicing failed. Could not generate the final file.")
        return None
        
    return output_path

# --- 3. STREAMLIT USER INTERFACE (UNCHANGED) ---
def run_streamlit_app():
    st.set_page_config(page_title="MeowCensor", page_icon="🐱")
    st.title("🐱 MeowCensor")
    st.markdown("Replace curse words in your audio files with cat sounds!")

    uploaded_file = st.file_uploader(
        "Upload your audio file (.mp3, .wav)",
        type=['mp3', 'wav']
    )

    if uploaded_file is not None:
        st.subheader("Your Original Audio")
        st.audio(uploaded_file, format='audio/wav')

        if st.button("Censor the Audio!", type="primary"):
            with st.spinner('Meowing in progress... Please wait.'):
                with NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_file:
                    tmp_file.write(uploaded_file.getvalue())
                    temp_input_path = tmp_file.name

                final_audio_path = run_censor_workflow(temp_input_path, ui_mode=True)

                if final_audio_path:
                    st.subheader("✅ Censored Audio")
                    st.success("Censoring complete!")
                    
                    with open(final_audio_path, "rb") as f:
                        audio_bytes = f.read()
                    st.audio(audio_bytes, format='audio/wav')

                    with open(final_audio_path, "rb") as f:
                        st.download_button(
                            label="Download Censored File",
                            data=f,
                            file_name=os.path.basename(final_audio_path),
                            mime="audio/wav"
                        )
                else:
                    st.error("The workflow failed. Please check the logs.")

# --- 4. NEW: COMMAND-LINE INTERFACE (CLI) ENTRY POINT ---
if __name__ == "__main__":
    # Check if any command-line arguments were passed.
    # sys.argv is a list of arguments. The first one is always the script name.
    # If the length is > 1, it means the user provided more arguments.
    if len(sys.argv) > 1:
        # --- This block runs for CLI mode ---
        print("--- MeowCensor CLI Mode ---")
        parser = argparse.ArgumentParser(description="Censor profanity in an audio file with meows.")
        parser.add_argument("input_file", help="The path to the audio file to censor.")
        args = parser.parse_args()

        if not os.path.exists(args.input_file):
            print(f"❌ Error: Input file not found at '{args.input_file}'")
        else:
            final_path = run_censor_workflow(args.input_file, ui_mode=False)
            if final_path:
                print(f"\n✅ Success! Censored audio saved to: {final_path}")
            else:
                print("\n❌ Workflow failed.")
    else:
        # --- This block runs for UI mode ---
        # If no arguments are provided, default to starting the Streamlit app.
        run_streamlit_app()