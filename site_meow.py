import streamlit as st
from pydub import AudioSegment
import subprocess
import sys
import os
import base64

def get_base64_of_bin_file(bin_file):
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
        
def set_background_image(image_path):
        bin_str = get_base64_of_bin_file(image_path)
        page_bg_img = f'''
        <style>
        .stApp {{
        background-image: url("data:image/png;base64,{bin_str}");
        background-size: content;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed; /* Optional: pins the background image */
        }}
        </style>
        '''
        st.markdown(page_bg_img, unsafe_allow_html = True)

st.html(''' 
    <html>
    <head>
    <style>        
        h1 {text-align: center;
            font-family: cursive;
            font-size: 40px;
            }
        p {text-align: center;
           font-family: cursive;
           font-size: 20px;}
    </style>
    </head>
    <body>
        <h1>Meow Censorfier</h1>
        <p>A cuter way to deal with unsavory language.</p>
    </body>
    </html> 
''')

set_background_image('cat_bg.png')


def save_bytes_to_file(byte_data, filename):
    """
    Writes raw bytes directly to a file.

    Args:
        byte_data (bytes): The bytes to write.
        filename (str): The name of the output file.
    """
    with open(filename, 'wb') as f:
        f.write(byte_data)

# Create a file uploader widget
audio = st.audio_input("Record high quality audio", sample_rate=16000)
if audio:
    with open("recorded_audio.wav", "wb") as f:
        f.write(audio.getbuffer())
        st.write("Audio recorded and saved successfully!")

uploaded_file = st.file_uploader("Choose a file", type=["wav", "mp3"])

if os.path.exists("temp_audio/audio.wav"):
    os.remove("temp_audio/audio.wav")

if uploaded_file is not None:
    # Read the uploaded file
    bytes_data = uploaded_file.getvalue()

    # Display information about the uploaded file
    st.write("Filename:", uploaded_file.name)
    st.write("File type:", uploaded_file.type)
    st.write("File size (bytes):", len(bytes_data))
    st.audio(uploaded_file.name, format="audio/mpeg", loop=False)
    
    #Convert file to WAV if necessary
    AUDIO_FILE = uploaded_file.name
    if AUDIO_FILE.endswith('.mp3'):
        convert = AudioSegment.from_mp3(AUDIO_FILE)
        convert.export('temp_audio/audio.wav', format='wav')
        st.write("yippee")
    else:
        save_bytes_to_file(bytes_data, 'temp_audio/audio.wav')

    
if st.button('MEOWIFY'):
    if uploaded_file is not None:
         audioTest = subprocess.run([sys.executable, "test_audio.py", 'temp_audio/audio.wav'], capture_output = True, text = True)
         st.write(audioTest.stdout)
         st.write(audioTest.stderr)
    else:
        st.write("Please select a file")
        
if os.path.exists('temp_audio/audio.wav'):
    st.audio('temp_audio/audio.wav', format="audio/mpeg", loop=False)