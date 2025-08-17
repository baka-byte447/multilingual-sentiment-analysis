import pytest
from pipeline.detect import detect_language, get_language_name

def test_detect_english():
    """Test English language detection."""
    text = "This is a great product! I highly recommend it."
    result = detect_language(text)
    assert result == 'en'

def test_detect_spanish():
    """Test Spanish language detection."""
    text = "Este producto es increíble. Lo recomiendo mucho."
    result = detect_language(text)
    assert result == 'es'

def test_detect_french():
    """Test French language detection."""
    text = "Ce produit est fantastique. Je le recommande vivement."
    result = detect_language(text)
    assert result == 'fr'

def test_detect_short_text():
    """Test detection with very short text."""
    text = "OK"
    result = detect_language(text)
    assert result == 'en'  # Should default to English

def test_detect_empty_text():
    """Test detection with empty text."""
    text = ""
    result = detect_language(text)
    assert result == 'en'  # Should default to English

def test_get_language_name():
    """Test language name mapping."""
    assert get_language_name('en') == 'English'
    assert get_language_name('es') == 'Spanish'
    assert get_language_name('fr') == 'French'
    assert get_language_name('unknown') == 'UNKNOWN'