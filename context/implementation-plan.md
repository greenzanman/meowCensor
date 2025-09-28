A practical, step-by-step implementation plan to build the MeowCensor project based on the design document. This plan breaks the project into four manageable phases, allowing you to build and test each part incrementally.

***

### ## Phase 1: Build and Prepare the Meow Library 📚

**Goal:** Create the foundational dataset of clean, analyzed meow sounds. This entire phase is a one-time, offline process.

**Step 1.1: Setup and API Access (Completed)**
* **Action:** Create a Freesound.org account and get an API key.
* **Tools:** `Python`, `requests` library.
* **Outcome:** You can programmatically access Freesound's data.

* **Phase 1: Build and Prepare the Meow Library 📚**
    * **Step 1.2: Script for Downloading and Processing**
        * **Action:** Write a Python script (`prepare_library.py`) that searches Freesound for suitable audio.
        * **Inside the script, for each sound:**
            1.  **Download** the audio **preview** file (e.g., `.mp3`) into a `./meow_library/raw/` folder.
            2.  **Load** the raw audio file with `librosa.load()`.
            3.  **Trim Silence** from the start and end using `librosa.effects.trim()`.
            4.  **Analyze** the trimmed audio to get its `duration` and average `pitch` (`librosa.pyin`).
            5.  **Save** the processed audio as a new `.wav` file in the `./meow_library/processed/` directory.
            6.  **Store Metadata** (new filename, path, duration, pitch) in a list.
        * **Tools:** `freesound`, `librosa`, `pandas`, `soundfile`, `numpy`.
        * **Outcome:** Two folders (`/raw` and `/processed` audio) and a `meow_database.csv` catalog ready for use.

***

### ## Phase 2: Develop the Backend Agents ⚙️

**Goal:** Implement and test each agent's core logic independently.

**Goal:** Implement and test each agent's core logic independently.

**Step 2.1: Transcriber Agent (Completed)**
* **Goal:** Create a self-contained Python module that accurately transcribes an audio file, providing word-level timestamps for every word spoken.
* **Environment Setup:**
    1.  **Install FFmpeg:** This is a system dependency for Whisper. It can be installed with `brew install ffmpeg` (macOS), `choco install ffmpeg` (Windows), or `sudo apt install ffmpeg` (Debian/Ubuntu).
    2.  **Install Python Library:** Run `pip install openai-whisper`.
* **Final Code (`transcriber_agent.py`):**
    ```python
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

        Args:
            file_path (str): The full path to the audio file (e.g., .mp3, .wav).

        Returns:
            list[dict]: A list of dictionaries, where each dictionary represents a word
                        and contains {'word': str, 'start': float, 'end': float}.
                        Returns an empty list if the model isn't loaded or an error occurs.
        """
        if not model:
            print("Whisper model is not available. Cannot transcribe.")
            return []
        
        if not os.path.exists(file_path):
            print(f"Error: Audio file not found at '{file_path}'")
            return []

        print(f"Starting transcription for: {os.path.basename(file_path)}...")
        
        try:
            result = model.transcribe(file_path, word_timestamps=True)
            
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
    if __name__ == '__main__':
        sample_file_to_test = "test.mp3" 
        
        print("\n--- [Running Standalone Test] ---")
        if os.path.exists(sample_file_to_test):
            transcript = transcribe_audio(sample_file_to_test)
            
            if transcript:
                print("\n✅ Test Passed. Transcription Result (first 15 words):")
                for item in transcript[:15]:
                    print(f"  - Word: \"{item['word']:<15}\" Start: {item['start']:.2f}s, End: {item['end']:.2f}s")
            else:
                print("\n❌ Test Failed. Transcription returned an empty list.")
        else:
            print(f"\n🟡 Test Skipped. Please create a file named '{sample_file_to_test}' to run the test.")

    ```
* **Testing:** Test the agent by running `python transcriber_agent.py` with a sample audio file named `test.mp3` in the same directory. Verify that it prints accurate, word-level timestamps.


**Step 2.2: Censor Agent**
* **Action:** Create a function `find_swear_words(transcript)` that takes the timestamped list from the previous step. It should format this data into a string, send it to an LLM (like Gemini via its API), and parse the response to get the start and end times of words to be censored.
* **Tools:** `google-generativeai` or `openai` library.
* **Prompting:** Your prompt is key here. It should be something like: *"You are a content moderator. From the following text with timestamps, identify any curse words, profanity, or slurs. Respond ONLY with a JSON list of the start and end times for each word you identify. If none are found, return an empty list []."*
* **Testing:** Test with sample transcripts containing obvious and subtle curse words to see if the LLM correctly identifies them and returns a valid JSON.

**Step 2.3: Audio Surgeon Agent**
* **Action:** Create a function `splice_audio(audio_path, censor_times)`. This function will be the most complex.
    1.  Load your `meow_database.csv` into a pandas DataFrame.
    2.  Load the original audio file with `pydub`.
    3.  Loop through each `censor_time` entry.
    4.  For each entry, calculate the needed duration.
    5.  **Search your DataFrame** to find the meow with the closest duration and pitch.
    6.  Load the chosen meow file with `pydub`.
    7.  If necessary, **time-stretch** the meow using `pydub.effects.speedup` to match the duration perfectly.
    8.  Splice the meow into the audio segment.
* **Tools:** `pydub`, `pandas`.
* **Testing:** Create a mock list of timestamps and test the splicing logic on a sample audio file. Check if the output audio has meows at the correct times and if they sound natural.

***

### ## Phase 3: Build the User Interface 🖥️

**Goal:** Create the web interface that allows a user to interact with your backend.

**Step 3.1: Basic File I/O**
* **Action:** Create an `app.py` file. Use `streamlit` to build the UI as specified in the design doc.
* **Functionality:**
    * `st.title("Meow Censor")`
    * `st.file_uploader()` to accept `.mp3` and `.wav` files.
    * `st.button("Censor the Audio!")` to trigger the process.
* **Outcome:** A user can upload a file and click a button.

**Step 3.2: Add Processing Feedback**
* **Action:** Implement the `st.spinner()` to provide feedback to the user after they click the button.
* **Functionality:** The spinner should be active while the backend agents are running.
* **Outcome:** The user knows the application is working and not frozen.

**Step 3.3: Display and Download Results**
* **Action:** Once the audio processing is complete, display the final result.
* **Functionality:**
    * Use `st.audio()` to let the user play the censored file.
    * Use `st.download_button()` to allow the user to save the file.
* **Outcome:** A user can hear and save the final product.

***

### ## Phase 4: Integration and Final Touches 🔗

**Goal:** Connect the UI to the backend agents to create a fully functional application.

**Step 4.1: Create the Main Workflow**
* **Action:** In your `app.py` or a `main.py` file, create a main function `run_censor_workflow(file_path)` that calls your three agent functions in sequence.
    1.  `transcript = transcribe_audio(file_path)`
    2.  `censor_times = find_swear_words(transcript)`
    3.  `output_path = splice_audio(file_path, censor_times)`
    4.  Return `output_path`.
* **Outcome:** A single function that orchestrates the entire backend process.

**Step 4.2: Connect UI to Workflow**
* **Action:** Inside the `if st.button(...)` block in your Streamlit app, call your `run_censor_workflow()` function.
* **Outcome:** The "Censor the Audio!" button now triggers the full, end-to-end process, and the final audio path is returned to the UI for display and download.

**Step 4.3: Refinement**
* **Action:** Test the full application with various audio files. Add error handling (e.g., for failed transcriptions or unsupported file types) and clean up the code.
* **Outcome:** A robust and polished final application.

yay