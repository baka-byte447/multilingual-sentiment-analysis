import google.generativeai as genai
import json
import logging
from config import Config
from pipeline.sentiment import get_sentiment_distribution

# Configure Gemini
if Config.GEMINI_API_KEY:
    genai.configure(api_key=Config.GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash-latest')

def generate_summary(results):
    """
    Generate an overall summary of sentiment analysis results using Gemini API.
    
    Args:
        results (list): List of sentiment analysis results
        
    Returns:
        dict: Summary with insights and statistics
    """
    try:
        if not results:
            return {
                'overall_sentiment': 'Neutral',
                'total_reviews': 0,
                'distribution': {'Positive': 0, 'Negative': 0, 'Neutral': 0},
                'insights': 'No reviews to analyze.',
                'languages_detected': []
            }
        
        # Calculate basic statistics
        total_reviews = len(results)
        distribution = get_sentiment_distribution(results)
        
        # Get unique languages
        languages = list(set([result['detected_language'] for result in results]))
        
        # Determine overall sentiment
        if distribution['Positive'] > 50:
            overall_sentiment = 'Positive'
        elif distribution['Negative'] > 50:
            overall_sentiment = 'Negative'
        else:
            overall_sentiment = 'Mixed'
        
        # Generate AI insights if Gemini is available
        insights = generate_ai_insights(results, distribution)
        
        return {
            'overall_sentiment': overall_sentiment,
            'total_reviews': total_reviews,
            'distribution': distribution,
            'insights': insights,
            'languages_detected': languages
        }
        
    except Exception as e:
        logging.error(f"Summary generation failed: {e}")
        return {
            'overall_sentiment': 'Unknown',
            'total_reviews': len(results) if results else 0,
            'distribution': {'Positive': 0, 'Negative': 0, 'Neutral': 0},
            'insights': 'Unable to generate insights.',
            'languages_detected': []
        }

def generate_ai_insights(results, distribution):
    """
    Generate AI-powered insights using Gemini API.
    
    Args:
        results (list): Sentiment analysis results
        distribution (dict): Sentiment distribution
        
    Returns:
        str: Generated insights
    """
    try:
        if not Config.GEMINI_API_KEY:
            return generate_basic_insights(distribution)
        
        # Prepare sample reviews for analysis
        sample_reviews = []
        for sentiment in ['Positive', 'Negative', 'Neutral']:
            sentiment_reviews = [r for r in results if r['sentiment_label'] == sentiment]
            if sentiment_reviews:
                sample_reviews.extend(sentiment_reviews[:2])  # Take up to 2 samples per sentiment
        
        # Create prompt for Gemini
        prompt = f"""
        Analyze the following sentiment analysis results and provide insights:
        
        Total Reviews: {len(results)}
        Sentiment Distribution: {distribution}
        
        Sample Reviews:
        {json.dumps([{
            'text': r['original_text'][:200] + ('...' if len(r['original_text']) > 200 else ''),
            'sentiment': r['sentiment_label'],
            'language': r['detected_language']
        } for r in sample_reviews], indent=2)}
        
        Please provide a concise analysis (2-3 sentences) focusing on:
        1. Overall sentiment trend
        2. Key themes or patterns you notice
        3. Any notable insights about the feedback
        
        Keep the response under 150 words and professional.
        """
        
        response = model.generate_content(prompt)
        return response.text.strip()
        
    except Exception as e:
        logging.warning(f"AI insights generation failed: {e}")
        return generate_basic_insights(distribution)

def generate_basic_insights(distribution):
    """
    Generate basic insights based on sentiment distribution.
    
    Args:
        distribution (dict): Sentiment distribution
        
    Returns:
        str: Basic insights
    """
    insights = []
    
    if distribution['Positive'] > 60:
        insights.append("The overall sentiment is predominantly positive, indicating high satisfaction.")
    elif distribution['Negative'] > 60:
        insights.append("The sentiment is mainly negative, suggesting areas for improvement.")
    else:
        insights.append("The sentiment is mixed, with varying opinions across reviews.")
    
    if distribution['Neutral'] > 30:
        insights.append("A significant portion of reviews are neutral, indicating moderate engagement.")
    
    return " ".join(insights)