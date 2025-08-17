import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # API Keys
    GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', '')
    
    # Model configurations
    SENTIMENT_MODEL = 'cardiffnlp/twitter-roberta-base-sentiment-latest'
    TRANSLATION_MODEL = 'Helsinki-NLP/opus-mt-{}-en'
    
    # File upload settings
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS = {'csv', 'txt'}
    
    # App settings
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
