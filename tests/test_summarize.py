import pytest
from unittest.mock import patch, MagicMock
from pipeline.summarize import generate_summary, generate_basic_insights

def test_generate_summary_empty_results():
    """Test summary generation with empty results."""
    summary = generate_summary([])
    assert summary['total_reviews'] == 0
    assert summary['overall_sentiment'] == 'Neutral'
    assert summary['insights'] == 'No reviews to analyze.'

def test_generate_summary_with_results():
    """Test summary generation with sample results."""
    results = [
        {
            'sentiment_label': 'Positive',
            'detected_language': 'en',
            'original_text': 'Great product!'
        },
        {
            'sentiment_label': 'Positive',
            'detected_language': 'es',
            'original_text': 'Excelente producto!'
        },
        {
            'sentiment_label': 'Negative',
            'detected_language': 'fr',
            'original_text': 'Produit terrible'
        }
    ]
    
    summary = generate_summary(results)
    assert summary['total_reviews'] == 3
    assert summary['overall_sentiment'] in ['Positive', 'Mixed']
    assert 'en' in summary['languages_detected']
    assert 'es' in summary['languages_detected']
    assert 'fr' in summary['languages_detected']

def test_generate_basic_insights():
    """Test basic insights generation."""
    distribution = {'Positive': 70, 'Negative': 20, 'Neutral': 10}
    insights = generate_basic_insights(distribution)
    assert 'predominantly positive' in insights.lower()
    
    distribution = {'Positive': 20, 'Negative': 70, 'Neutral': 10}
    insights = generate_basic_insights(distribution)
    assert 'mainly negative' in insights.lower()
    
    distribution = {'Positive': 40, 'Negative': 30, 'Neutral': 30}
    insights = generate_basic_insights(distribution)
    assert 'mixed' in insights.lower()

@patch('pipeline.summarize.model')
@patch('pipeline.summarize.Config.GEMINI_API_KEY', 'test-key')
def test_generate_ai_insights_success(mock_model):
    """Test AI insights generation with Gemini."""
    mock_response = MagicMock()
    mock_response.text = "The sentiment is predominantly positive with high customer satisfaction."
    mock_model.generate_content.return_value = mock_response
    
    results = [{'sentiment_label': 'Positive', 'original_text': 'Great!', 'detected_language': 'en'}]
    distribution = {'Positive': 100, 'Negative': 0, 'Neutral': 0}
    
    from pipeline.summarize import generate_ai_insights
    insights = generate_ai_insights(results, distribution)
    
    assert "positive" in insights.lower()
    mock_model.generate_content.assert_called_once()