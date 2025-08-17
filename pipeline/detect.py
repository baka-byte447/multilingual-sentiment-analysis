from langdetect import detect, DetectorFactory
import logging

# Set seed for consistent results
DetectorFactory.seed = 0

def detect_language(text):
    """
    Detect the language of the given text.
    
    Args:
        text (str): Input text to analyze
        
    Returns:
        str: Language code (e.g., 'en', 'es', 'fr')
    """
    try:
        if not text or len(text.strip()) < 3:
            return 'en'  # Default to English for very short texts
        
        detected = detect(text)
        return detected
    except Exception as e:
        logging.warning(f"Language detection failed for text: {text[:50]}... Error: {e}")
        return 'en'  # Default to English if detection fails

def get_language_name(lang_code):
    """
    Convert language code to full language name.
    
    Args:
        lang_code (str): Language code
        
    Returns:
        str: Full language name
    """
    lang_map = {
        'en': 'English',
        'es': 'Spanish',
        'fr': 'French',
        'de': 'German',
        'it': 'Italian',
        'pt': 'Portuguese',
        'ru': 'Russian',
        'zh': 'Chinese',
        'ja': 'Japanese',
        'ko': 'Korean',
        'ar': 'Arabic',
        'hi': 'Hindi',
        'nl': 'Dutch',
        'sv': 'Swedish',
        'no': 'Norwegian',
        'da': 'Danish',
        'fi': 'Finnish',
        'pl': 'Polish',
        'tr': 'Turkish',
        'th': 'Thai'
    }
    return lang_map.get(lang_code, lang_code.upper())