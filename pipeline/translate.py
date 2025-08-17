import google.generativeai as genai
from transformers import pipeline
import logging
from config import Config

# Configure Gemini
if Config.GEMINI_API_KEY:
    genai.configure(api_key=Config.GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash-latest')

# Fallback translation models
translation_cache = {}

def translate_with_gemini(text, source_lang):
    """
    Translate text using Gemini API.
    
    Args:
        text (str): Text to translate
        source_lang (str): Source language code
        
    Returns:
        str: Translated text or original if translation fails
    """
    try:
        if not Config.GEMINI_API_KEY:
            raise Exception("Gemini API key not configured")
        
        prompt = f"Translate the following text from {source_lang} to English. Return only the translation without any additional text:\n\n{text}"
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        logging.warning(f"Gemini translation failed: {e}")
        return None

def translate_with_huggingface(text, source_lang):
    """
    Translate text using Hugging Face transformers.
    
    Args:
        text (str): Text to translate
        source_lang (str): Source language code
        
    Returns:
        str: Translated text or original if translation fails
    """
    try:
        # Create model name based on source language
        model_name = f"Helsinki-NLP/opus-mt-{source_lang}-en"
        
        # Use cached translator if available
        if model_name not in translation_cache:
            translation_cache[model_name] = pipeline("translation", model=model_name)
        
        translator = translation_cache[model_name]
        result = translator(text, max_length=512)
        return result[0]['translation_text']
    except Exception as e:
        logging.warning(f"HuggingFace translation failed for {source_lang}: {e}")
        return None

def translate_text(text, source_lang):
    """
    Translate text to English using Gemini API with HuggingFace fallback.
    
    Args:
        text (str): Text to translate
        source_lang (str): Source language code
        
    Returns:
        str: Translated text or original text if translation fails
    """
    if source_lang == 'en' or not text.strip():
        return text
    
    # Try Gemini first
    translated = translate_with_gemini(text, source_lang)
    if translated:
        return translated
    
    # Fallback to HuggingFace
    translated = translate_with_huggingface(text, source_lang)
    if translated:
        return translated
    
    # If all fails, return original text
    logging.warning(f"All translation methods failed for language {source_lang}")
    return text