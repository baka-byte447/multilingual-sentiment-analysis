from transformers import pipeline
import logging
from config import Config

# Initialize sentiment analysis pipeline
sentiment_analyzer = None

def initialize_sentiment_analyzer():
    """Initialize the sentiment analysis pipeline."""
    global sentiment_analyzer
    try:
        sentiment_analyzer = pipeline(
            "sentiment-analysis",
            model=Config.SENTIMENT_MODEL,
            return_all_scores=True
        )
    except Exception as e:
        logging.warning(f"Failed to load primary model, using fallback: {e}")
        sentiment_analyzer = pipeline(
            "sentiment-analysis",
            model="nlptown/bert-base-multilingual-uncased-sentiment",
            return_all_scores=True
        )

def analyze_sentiment(text):
    """
    Analyze sentiment of the given text.
    
    Args:
        text (str): Text to analyze
        
    Returns:
        dict: Sentiment analysis result with label and confidence
    """
    global sentiment_analyzer
    
    if sentiment_analyzer is None:
        initialize_sentiment_analyzer()
    
    try:
        if not text or len(text.strip()) < 3:
            return {'label': 'Neutral', 'confidence': 0.5}
        
        results = sentiment_analyzer(text)
        
        # Handle different model outputs
        if isinstance(results[0], list):
            scores = results[0]
        else:
            scores = results
        
        # Find the highest scoring sentiment
        best_result = max(scores, key=lambda x: x['score'])
        
        # Map labels to standardized format
        label = map_sentiment_label(best_result['label'])
        confidence = round(best_result['score'], 3)
        
        return {
            'label': label,
            'confidence': confidence
        }
        
    except Exception as e:
        logging.error(f"Sentiment analysis failed: {e}")
        return {'label': 'Neutral', 'confidence': 0.5}

def map_sentiment_label(label):
    """
    Map model-specific labels to standardized sentiment labels.
    
    Args:
        label (str): Original model label
        
    Returns:
        str: Standardized label (Positive, Negative, Neutral)
    """
    label = label.upper()
    
    if label in ['POSITIVE', 'POS', 'LABEL_2', '5', '4']:
        return 'Positive'
    elif label in ['NEGATIVE', 'NEG', 'LABEL_0', '1', '2']:
        return 'Negative'
    else:
        return 'Neutral'

def get_sentiment_distribution(results):
    """
    Calculate sentiment distribution from results.
    
    Args:
        results (list): List of sentiment analysis results
        
    Returns:
        dict: Sentiment distribution
    """
    distribution = {'Positive': 0, 'Negative': 0, 'Neutral': 0}
    
    for result in results:
        sentiment = result.get('sentiment_label', 'Neutral')
        distribution[sentiment] += 1
    
    total = len(results)
    if total > 0:
        for key in distribution:
            distribution[key] = round(distribution[key] / total * 100, 1)
    
    return distribution