# **Design Doc: MeowCensor Project 🐱 (v1.1)**

### **1. Overview**

**MeowCensor** is a web application that automatically replaces profanity in user-uploaded audio files with cat "meow" sounds. The system is designed as a modular, multi-agent pipeline that handles transcription, profanity detection, and audio manipulation. The core innovation is its use of a pre-processed library of meow sounds, allowing the system to select a meow of the appropriate length and pitch to naturally fit into the conversation, providing a more elegant and humorous alternative to a standard bleep.

### **2. Goals & Features**

* **Primary Goal:** To provide a simple, user-friendly tool for censoring audio files.
* **User Interface (UI):** A clean web interface built with **Streamlit** that allows users to:
    * Upload an audio file (`.mp3`, `.wav`).
    * See a visual indicator while the file is being processed.
    * Play the final, censored audio directly in the browser.
    * Download the censored audio file.
* **Accurate Censorship:** The system must accurately identify the start and end times of spoken curse words.
* **Natural Sound Replacement:** The replacement "meow" sounds should match the duration of the censored word to avoid awkward pauses or cut-offs.
* **Modular Architecture:** The backend will be built as a sequence of independent agents, making the system easy to develop, debug, and extend.

### **3. System Architecture**

The project follows a sequential, multi-agent workflow. An input audio file is passed through a series of specialized agents, each performing one task before handing its output to the next.



1.  **UI (Streamlit):** User uploads the `audio_file.mp3`.
2.  **Transcriber Agent:** Receives the audio file and generates a `transcript.json` with word-level timestamps.
3.  **Censor Agent:** Receives the `transcript.json`, identifies swear words, and outputs a `timestamps_to_censor.json`.
4.  **Audio Surgeon Agent:** Receives the original `audio_file.mp3`, the `timestamps_to_censor.json`, and our pre-built **Meow Library**. It performs the audio replacement and outputs the final `censored_audio.mp3`.
5.  **UI (Streamlit):** The final audio file is presented to the user for playback and download.

### **4. Component Specifications**

#### **4.1. Meow Library (Prerequisite)**
This is the offline-prepared database of sounds that the Audio Surgeon Agent will use.
* **Source:** Audio files sourced from Freesound.org via its API.
* **Processing:** All files are to be automatically processed to:
    * **Trim Silence:** Remove silence from the beginning and end.
    * **Analyze:** Extract key metadata.
* **Database (`meow_database.csv`):** A catalog file containing metadata for each audio file, including its `filename`, `duration_sec`, and `average_pitch_hz`.

#### **4.2. Frontend: Streamlit UI (`app.py`)**
* **Framework:** Streamlit
* **User Flow:**
    1.  A title "Meow Censor" is displayed.
    2.  An `st.file_uploader` widget allows the user to select an audio file.
    3.  Upon upload, the original audio is playable via `st.audio`.
    4.  A button `st.button("Censor the Audio!")` triggers the backend process.
    5.  While processing, an `st.spinner('Meowing in progress...')` is shown.
    6.  Upon completion, the spinner is replaced with a success message and a new `st.audio` player for the censored result.
    7.  An `st.download_button` allows the user to save the final file.

#### **4.3. Backend: Agent Workflow (`main.py`)**
* **Framework:** Agent Development Kit (ADK)
* **Transcriber Agent:**
    * **Input:** Path to an audio file.
    * **Tool:** **OpenAI Whisper**. This provides high-quality transcription and can be run locally, making it a free and powerful option.
    * **Output:** A structured JSON format containing each word and its start/end time.
* **Censor Agent:**
    * **Input:** The structured transcript data from the Transcriber Agent.
    * **Tool:** An LLM (e.g., Gemini 1.5 Flash).
    * **Logic:** The agent will rely on the LLM's **general knowledge** to identify profanity. The prompt will instruct it to find common English curse words, insults, and slurs based on its broad understanding, rather than a fixed list.
    * **Output:** A JSON list containing the start and end times for each identified curse word. Example: `[{"word": "darn", "start_time": 1.3, "end_time": 1.8}]`.
* **Audio Surgeon Agent:**
    * **Input:** Path to the original audio file and the JSON list from the Censor Agent.
    * **Tool:** An audio manipulation library (e.g., `pydub`).
    * **Logic:**
        1.  For each timestamp pair, calculate the required duration (`end_time - start_time`).
        2.  Query the `meow_database.csv` to find the meow file with the **closest duration and a comparable pitch** to the speaker's voice.
        3.  If the duration of the selected meow is not a perfect match, **slightly time-stretch** the meow audio to fit the required duration seamlessly.
        4.  Use `pydub` to slice the original audio and insert the prepared meow sound.
    * **Output:** The path to the newly created censored audio file (e.g., `"censored_output.mp3"`).

### **5. Reach Features (Future Work)**
* **Live Audio Recording:** Add a feature to the UI to allow users to record audio directly in the browser instead of uploading a file.