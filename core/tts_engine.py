from TTS.api import TTS
from werkzeug.utils import secure_filename
import os

def initialize_tts(device):
    # Initialize and return the TTS model, loading it onto the requested device (CPU or GPU)
    return TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2").to(device)

def generate_audio(text, samples, language, output, tts):
    # Secure the 'output' filename to avoid invalid characters, then add '.wav' extension
    output_filename = secure_filename(output) + ".wav"
    # Determine the path to save the generated audio file inside 'static/output'
    output_path = os.path.join("static", "output", output_filename)

    # Use the TTS engine to generate the audio:
    # - 'text': the string to be spoken
    # - 'speaker_wav': paths to the speaker's sample(s) for voice cloning
    # - 'language': language code to use for TTS
    # - 'split_sentences': whether TTS should handle the text in segments
    tts.tts_to_file(
        text,
        speaker_wav=samples,
        language=language,
        file_path=output_path,
        split_sentences=True
    )

    # Return just the filename (e.g., "myoutput.wav") so the Flask app can reference it
    return output_filename