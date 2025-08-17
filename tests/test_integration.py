import pytest
import json
from app import app
from unittest.mock import patch

@pytest.fixture
def client():
    """Create test client."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index_page(client):
    """Test index page loads correctly."""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Multilingual Sentiment Analysis' in response.data

def test_analyze_with_text_input(client):
    """Test analysis with text input."""
    with patch('pipeline.detect.detect_language') as mock_detect, \
         patch('pipeline.translate.translate_text') as mock_translate, \
         patch('pipeline.sentiment.analyze_sentiment') as mock_sentiment, \
         patch('pipeline.summarize.generate_summary') as mock_summary:
        
        # Mock responses
        mock_detect.return_value = 'en'
        mock_translate.return_value = 'This is a great product!'
        mock_sentiment.return_value = {'label': 'Positive', 'confidence': 0.95}
        mock_summary.return_value = {
            'total_reviews': 1,
            'overall_sentiment': 'Positive',
            'distribution': {'Positive': 100, 'Negative': 0, 'Neutral': 0},
            'insights': 'Very positive feedback',
            'languages_detected': ['en']
        }
        
        response = client.post('/analyze', data={
            'text_reviews': 'This is a great product!'
        })
        
        assert response.status_code == 200
        assert b'Positive' in response.data
        assert b'Analysis Summary' in response.data

def test_analyze_empty_input(client):
    """Test analysis with empty input."""
    response = client.post('/analyze', data={})
    assert response.status_code == 200
    assert b'Please provide reviews' in response.data

@patch('utils.file_handler.process_csv_file')
@patch('utils.file_handler.validate_file')
def test_analyze_with_csv_upload(mock_validate, mock_process, client):
    """Test analysis with CSV file upload."""
    with patch('pipeline.detect.detect_language') as mock_detect, \
         patch('pipeline.translate.translate_text') as mock_translate, \
         patch('pipeline.sentiment.analyze_sentiment') as mock_sentiment, \
         patch('pipeline.summarize.generate_summary') as mock_summary:
        
        # Mock file processing
        mock_validate.return_value = True
        mock_process.return_value = ['Great product!', 'Terrible service.']
        
        # Mock pipeline responses
        mock_detect.return_value = 'en'
        mock_translate.return_value = 'Great product!'
        mock_sentiment.return_value = {'label': 'Positive', 'confidence': 0.9}
        mock_summary.return_value = {
            'total_reviews': 2,
            'overall_sentiment': 'Mixed',
            'distribution': {'Positive': 50, 'Negative': 50, 'Neutral': 0},
            'insights': 'Mixed feedback',
            'languages_detected': ['en']
        }
        
        # Create a mock file
        data = {'file': (open(__file__, 'rb'), 'test.csv')}
        response = client.post('/analyze', data=data, content_type='multipart/form-data')
        
        assert response.status_code == 200

def test_download_csv(client):
    """Test CSV download functionality."""
    test_data = json.dumps([
        {
            'id': 1,
            'original_text': 'Test review',
            'detected_language': 'en',
            'translated_text': None,
            'sentiment_label': 'Positive',
            'confidence': 0.9
        }
    ])
    
    response = client.get(f'/download/csv?data={test_data}')
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'text/csv; charset=utf-8'

def test_download_json(client):
    """Test JSON download functionality."""
    test_data = json.dumps([
        {
            'id': 1,
            'original_text': 'Test review',
            'detected_language': 'en',
            'translated_text': None,
            'sentiment_label': 'Positive',
            'confidence': 0.9
        }
    ])
    
    response = client.get(f'/download/json?data={test_data}')
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json; charset=utf-8'

def test_download_invalid_format(client):
    """Test download with invalid format."""
    response = client.get('/download/invalid')
    assert response.status_code == 400