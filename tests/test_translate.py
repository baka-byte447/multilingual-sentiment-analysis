import pytest
from unittest.mock import patch, MagicMock
from pipeline.translate import translate_text, translate_with_huggingface

def test_translate_english_text():
    """Test that English text is returned unchanged."""
    text = "This is English text"
    result = translate_text(text, 'en')
    assert result == text

def test_translate_empty_text():
    """Test translation of empty text."""
    result = translate_text("", 'es')
    assert result == ""

@patch('pipeline.translate.translate_with_gemini')
@patch('pipeline.translate.translate_with_huggingface')
def test_translate_fallback_to_huggingface(mock_hf, mock_gemini):
    """Test fallback from Gemini to HuggingFace."""
    mock_gemini.return_value = None
    mock_hf.return_value = "This is translated text"
    
    result = translate_text("Esto es texto en español", 'es')
    assert result == "This is translated text"
    mock_gemini.assert_called_once()
    mock_hf.assert_called_once()

@patch('pipeline.translate.pipeline')
def test_huggingface_translation_success(mock_pipeline):
    """Test successful HuggingFace translation."""
    mock_translator = MagicMock()
    mock_translator.return_value = [{'translation_text': 'Translated text'}]
    mock_pipeline.return_value = mock_translator
    
    result = translate_with_huggingface("Texto original", 'es')
    assert result == 'Translated text'

@patch('pipeline.translate.pipeline')
def test_huggingface_translation_failure(mock_pipeline):
    """Test HuggingFace translation failure."""
    mock_pipeline.side_effect = Exception("Translation failed")
    
    result = translate_with_huggingface("Texto original", 'es')
    assert result is None