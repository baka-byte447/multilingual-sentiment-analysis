import pytest
from unittest.mock import patch, MagicMock
from pipeline.sentiment import analyze_sentiment, map_sentiment_label, get_sentiment_distribution

def test_map_sentiment_labels():
    """Test sentiment label mapping."""
    assert map_sentiment_label('POSITIVE') == 'Positive'
    assert map_sentiment_label('NEGATIVE') == 'Negative'
    assert map_sentiment_label('NEUTRAL') == 'Neutral'
    assert map_sentiment_label('LABEL_2') == 'Positive'
    assert map_sentiment_label('LABEL_0') == 'Negative'

def test_analyze_empty_text():
    """Test sentiment analysis with empty text."""
    result = analyze_sentiment("")
    assert result['label'] == 'Neutral'
    assert result['confidence'] == 0.5

@patch('pipeline.sentiment.sentiment_analyzer')
def test_analyze_sentiment_success(mock_analyzer):
    """Test successful sentiment analysis."""
    mock_analyzer.return_value = [
        [
            {'label': 'POSITIVE', 'score': 0.9},
            {'label': 'NEGATIVE', 'score': 0.1}
        ]
    ]
    
    result = analyze_sentiment("This is great!")
    assert result['label'] == 'Positive'
    assert result['confidence'] == 0.9

def test_get_sentiment_distribution():
    """Test sentiment distribution calculation."""
    results = [
        {'sentiment_label': 'Positive'},
        {'sentiment_label': 'Positive'},
        {'sentiment_label': 'Negative'},
        {'sentiment_label': 'Neutral'}
    ]
    
    distribution = get_sentiment_distribution(results)
    assert distribution['Positive'] == 50.0
    assert distribution['Negative'] == 25.0
    assert distribution['Neutral'] == 25.0

def test_get_sentiment_distribution_empty():
    """Test sentiment distribution with empty results."""
    distribution = get_sentiment_distribution([])
    assert distribution['Positive'] == 0
    assert distribution['Negative'] == 0
    assert distribution['Neutral'] == 0