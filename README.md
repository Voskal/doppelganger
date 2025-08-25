# Project Overview

Doppelganger is a web application that clones a voice using uploaded sample(s), then converts text to speech in the cloned voice. It can optionally translate the text before speaking it. The app provides:
- A Flask-based server (server.py)
- A Text-to-Speech engine using the TTS library (tts_engine.py)
- A Translation module using (an async variant of) googletrans (translator.py)
- A Front-end (index.html + style.css) that lets you upload files and receive output
> End result: a .wav file containing spoken audio in the cloned voice, and a .txt file with the translation to your text input (optional).

*Key Features*:

Voice Samples:
> Upload one or more samples to capture a speaker’s vocal characteristics.

Automatic or Manual Text: 
> Provide text via a .txt file or by typing into a text area.

Auto-Detection & Translation: 
> Auto-detect the input text’s language, optionally translate it into a target language.

Speech Synthesis: 
> Generate a .wav audio file.

Download: 
> Easily download both the final audio and, if desired, the translated text.

# Setup & Installation
Python Environment
> Python Version: Recommended Python 3.9 or higher.

Required Libraries
Inside your environment, install project dependencies. You need:
- Flask (for the web server)
- googletrans (for autodetecting language and translation)
- torch (PyTorch, needed for the TTS model)
- TTS (Coqui TTS library)
- Werkzeug (for secure file handling)

# Running the Project
Ensure you have the correct dependencies installed as mentioned above.
Run the Flask app: **server.py**
> By default, it starts on port 9999 in debug mode.
Open a Browser and navigate to:
http://127.0.0.1:9999/
> You should see the Doppelganger web interface.

# How It Works (High-Level)
- Upload Voice Samples (one or more .mp3/.wav files).
- Provide Text (via .txt upload or manual input).
- (Optional) Translation:
  - Auto-detect the text language.
- If user chooses translation, convert text to the chosen language.
- If user does not choose translation but the text isn’t in a supported TTS language, it defaults to English.
> Voice Cloning & Synthesis:
- The TTS model (Coqui TTS) clones the speaker’s voice from the samples.
- Synthesizes the final text into audio (.wav).
> Download:
- The .wav file and, if translation was used, a .txt file with translated text.

# Step-by-Step Guide
Access the Web App:

In your browser, go to http://127.0.0.1:9999.

![Image](https://kappa.lol/DiCmvr.png)
Step 1: Upload Voice Samples

> Select one or more .mp3 or .wav files.

Step 2: Enter Text

> Option A: Click “Upload .txt File” and choose your text file.

> Option B: Click “Enter Text” to type directly into the text box.

Step 3: Translation Choice

> “Translate Text”: Pick a target language (e.g., English, Spanish, etc.).

> “Do Not Translate”: Use your text’s source language (auto-detected if needed).

Step 4: Name Your Output

> Provide a filename (the app will add .wav automatically).

Click “**CLONE**”

> The app processes the voice samples, text, and translation settings.

> A loading spinner appears. Wait until it completes.

Results:

- A built-in audio player to listen to the .wav.
- Download link for the audio file.
- If translated, a downloadable .txt containing the new text.

# Troubleshooting & Tips
googletrans Errors:

- If you see async usage issues, confirm you’re using a version that supports asynchronous calls (googletrans==4.0.0-rc1 or an alternative).
- Alternatively, adapt the code to synchronous usage or a different library.

TTS Model:
- Ensure PyTorch is installed (pip install torch).
- Large models may require GPU or may be slow on CPU.
- If your GPU is not recognized, check your CUDA installation (on NVIDIA hardware).

File Upload:

- If you get a FileNotFoundError or PermissionError, ensure your uploads and static/output folders exist and have the correct permissions.
- You might need to manually create these folders if your system blocks auto-creation.

Missing Audio or No Sound:
- Double-check your browser’s audio settings.
- Ensure the .wav file is actually generated in static/output.

Translation Not Accurate:

- The googletrans service is approximate. If precise translations are required, consider a more robust translator service.

# **Conclusion**
Doppelganger provides a straightforward, interactive way to clone a voice from sample(s), translate text (optionally), and produce spoken audio in the cloned voice. By combining Flask, Coqui TTS, and googletrans, it demonstrates:

- Basic web development with Python & Flask

- File handling and secure uploads

- Language detection and translation workflow

- Neural text-to-speech on CPU/GPU

Once you install the correct dependencies and run server.py, you’re set to explore or extend Doppelganger for your own use cases. Enjoy experimenting with voice cloning, translations, and the mesmerizing potential of AI-based TTS!