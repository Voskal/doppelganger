from flask import Flask, render_template, request, send_file
import os
from core.tts_engine import generate_audio, initialize_tts
from core.translator import translate_text
from werkzeug.utils import secure_filename
import torch
import asyncio

# Initialize the Flask application
app = Flask(__name__)

# Configure folders for uploads and outputs
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUTPUT_FOLDER'] = os.path.join("static", "output")

# Ensure the directories exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

# Supported languages stored in a dictionary for easy referencing
SUPPORTED_LANGUAGE = {
    "English": "en",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Italian": "it",
    "Portuguese": "pt",
    "Polish": "pl",
    "Turkish": "tr",
    "Russian": "ru",
    "Dutch": "nl",
    "Czech": "cs",
    "Arabic": "ar",
    "Chinese": "zh-cn",
    "Japanese": "ja",
    "Hungarian": "hu",
    "Korean": "ko",
    "Hindi": "hi"
}

# Determine whether to use GPU or CPU for TTS model
device = "cuda" if torch.cuda.is_available() else "cpu"

# Initialize the text-to-speech engine
tts = initialize_tts(device)

# Multiple routes point to the same homepage
@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    # Render the main template and pass in the supported languages
    return render_template('index.html', supported_languages=SUPPORTED_LANGUAGE)

@app.route('/process', methods=['POST'])
def process():
    # Retrieve the voice sample files from the form
    sample_files = request.files.getlist('samples')
    sample_paths = []

    # Save each uploaded sample in the uploads folder
    for file in sample_files:
        if file:
            # Secure the filename and build the full file path
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename))
            file.save(file_path)  # Save file to disk
            sample_paths.append(file_path)

    # Determine whether user chose "upload .txt file" or "manual text"
    text_choice = request.form.get('text_choice')
    text = ""

    # If user uploaded a file, save it and read its contents
    if text_choice == 'upload':
        text_file = request.files.get('text_file')
        if text_file and text_file.filename:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(text_file.filename))
            text_file.save(filepath)
            with open(filepath, 'r', encoding='utf-8') as f:
                text = f.read()
    else:
        # Otherwise, pull the text directly from the textarea
        text = request.form.get('manual_text', '')

    # If no text was provided, return the form with an error message
    if not text.strip():
        return render_template(
            "index.html",
            supported_languages=SUPPORTED_LANGUAGE,
            error="You must provide text to synthesize."
        )

    # Get the desired output filename (or default to 'output')
    output_name = request.form.get('output_name', 'output').strip()

    # Auto-detect the language of the provided text
    _, src_lang, _ = asyncio.run(translate_text(text))

    # Check if the user wants translation
    translate_option = request.form.get('translate_option')
    translated_text = None  # This will store the final translated text if needed

    if translate_option == 'no':
        # If user does NOT want translation but the detected language isn't supported,
        # force-translate the text to English so TTS can handle it
        if src_lang not in SUPPORTED_LANGUAGE.values():
            text, _, _ = asyncio.run(translate_text(text, translate_language="en"))
            tts_lang = "en"
        else:
            tts_lang = src_lang
    else:
        # If user DOES want translation, translate to the selected language
        selected_lang = request.form.get('target_language')
        text, _, _ = asyncio.run(translate_text(text, translate_language=selected_lang))
        tts_lang = selected_lang
        # Store the translated text so we can show a "Translated Text" download button
        translated_text = text

    # Generate the final audio file using the TTS engine
    output_filename = generate_audio(text, sample_paths, tts_lang, output_name, tts)

    # Render the template, passing the audio file and any translated text
    return render_template(
        'index.html',
        output_file=f"output/{output_filename}",
        supported_languages=SUPPORTED_LANGUAGE,
        translated_text=translated_text
    )

@app.route('/download')
def download_file():
    # Provide a way to download the generated .wav file
    output_path = os.path.join(app.config['OUTPUT_FOLDER'], 'output.wav')
    return send_file(output_path, as_attachment=True)

# Run the Flask app in debug mode on port 9999
if __name__ == '__main__':
    app.run(debug=True, port=9999)