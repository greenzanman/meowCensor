Here is a practical, step-by-step implementation plan to build the MeowCensor project based on the design document. This plan breaks the project into four manageable phases, allowing you to build and test each part incrementally.

***

### ## Phase 1: Build and Prepare the Meow Library 📚

**Goal:** Create the foundational dataset of clean, analyzed meow sounds. This entire phase is a one-time, offline process.

**Step 1.1: Setup and API Access**
* **Action:** Create a Freesound.org account and get an API key.
* **Tools:** `Python`, `requests` library.
* **Outcome:** You can programmatically access Freesound's data.

**Step 1.2: Script for Downloading and Processing**
* **Action:** Write a Python script (`prepare_library.py`) that loops through search results for "meow," "cat," etc.
* **Inside the loop, for each sound:**
    1.  **Download** the audio file into a `./meow_library/` folder.
    2.  **Load** the audio with `librosa.load()`.
    3.  **Trim Silence** using `librosa.effects.trim()`.
    4.  **Analyze** the trimmed audio to get its `duration` and average `pitch`.
    5.  **Save** the trimmed audio back to the file, overwriting the original.
    6.  **Store Metadata** (filename, duration, pitch) in a list.
* **Tools:** `freesound-python`, `librosa`, `pandas`, `soundfile`.
* **Outcome:** A folder of trimmed audio files and a `meow_database.csv` catalog.

***

### ## Phase 2: Develop the Backend Agents ⚙️

**Goal:** Implement and test each agent's core logic independently.

**Step 2.1: Transcriber Agent**
* **Action:** Create a Python function `transcribe_audio(file_path)` that takes an audio file and uses OpenAI Whisper to return a list of words with their timestamps.
* **Tools:** `openai-whisper` library. You can start with the tiny base model for speed.
* **Testing:** Test this function with a sample audio file to ensure you get accurate, word-level timestamps.

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