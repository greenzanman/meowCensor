Of course. Here is a complete, step-by-step guide you can send to your friend. This covers everything they need to do on a fresh Windows machine.

-----

## Complete Setup Guide for Your Teammate (Windows)

Welcome to the team\! Follow these steps to get the project running on your laptop. We'll use a package manager called Chocolatey to make installing tools easy.

-----

### Step 1: Install Chocolatey Package Manager

This tool lets you install developer software from the command line, which is much faster than finding and running individual installers.

1.  Click the **Start Menu**, type `PowerShell`, right-click on "Windows PowerShell", and select **Run as Administrator**.

2.  Copy and paste the entire command below into the blue PowerShell window and press Enter.

    ```powershell
    Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
    ```

3.  Wait for it to finish. Once it's done, **close the admin PowerShell window**.

-----

### Step 2: Install All Your Tools

Now we'll use Chocolatey to install Python, Node.js, Git, and FFmpeg all at once.

1.  Open a **new, regular** PowerShell window (you don't need to be an administrator for this part).

2.  Copy and paste the following command to install everything and press Enter.

    ```powershell
    choco install python nodejs-lts git ffmpeg -y
    ```

3.  This will take a few minutes. Grab a coffee\! ☕

4.  Once it's finished, **close and reopen** your PowerShell window to make sure all the new tools are available in your system's PATH.

-----

### Step 3: Get the Project Code

Now you'll download the project code from GitHub.

1.  Your teammate needs to add you as a **collaborator** on the GitHub repository. You'll get an email invitation—make sure to accept it.

2.  In your PowerShell terminal, navigate to where you want to store the project (e.g., `cd C:\dev`).

3.  Run the `git clone` command with the repository URL (get this from the green "Code" button on the GitHub page).

    ```powershell
    git clone https://github.com/greenzanman/meowCensor.git
    ```

4.  Navigate into the newly created project folder:

    ```powershell
    cd meow-censor
    ```

-----

### Step 4: Set Up the Python Environment

This step creates an isolated environment for our project's Python packages.

1.  **Create the virtual environment:**
    ```powershell
    python -m venv venv
    ```
2.  **Activate it.** You'll need to do this every time you open a new terminal to work on the project.
    ```powershell
    .\venv\Scripts\activate
    ```
    Your prompt should now start with `(venv)`.
3.  **Install all the Python packages** from the `requirements.txt` file in the project:
    ```powershell
    pip install -r requirements.txt
    ```

-----

### Step 5: Configure Your API Key

The final step is to add your personal Google AI API key.

1.  Go to the **[Google AI Studio](https://aistudio.google.com/)** website and get your own API key.
2.  Open the `test_agent.py` file in a code editor.
3.  Find the line `os.environ["GEMINI_API_KEY"] = "YOUR_API_KEY"` and replace `"YOUR_API_KEY"` with the key you just generated. Save the file.

-----

### Testing Your Setup ✅

You're all done\! To make sure everything works, run the two test scripts from your terminal (make sure your `(venv)` is still active).

1.  **Test the AI agent:**

    ```powershell
    python test_agent.py
    ```

    This should connect to the API and print "True" and "False".

2.  **Test the audio processing:**

    ```powershell
    python test_audio.py
    ```

    This should transcribe the text from the sample audio file.

If both scripts run without errors, your setup is perfect. Welcome to the hackathon\!