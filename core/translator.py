from googletrans import Translator

async def translate_text(text, translate_language=None):
    # Use 'async with' to handle the Translator context manager asynchronously
    async with Translator() as translator:
        # If no 'translate_language' is provided, attempt to auto-detect the source
        if translate_language is None:
            result = await translator.translate(text)
        else:
            # Otherwise, translate to the specific target language
            result = await translator.translate(text, translate_language)
        
        # Return the translated text, the detected source language, and the target language
        return result.text, result.src.lower(), result.dest.lower()