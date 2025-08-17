# Multilingual Sentiment Analysis Pipeline Web App

A Flask-based web application that performs sentiment analysis on multilingual text reviews. The app automatically detects languages, translates non-English text to English, analyzes sentiment using AI models, and provides comprehensive insights.

## Features

- **Multilingual Support**: Auto-detects 20+ languages and translates to English
- **Multiple Input Options**: Text input or CSV file upload
- **AI-Powered Analysis**: Uses Hugging Face Transformers for sentiment analysis
- **Smart Translation**: Gemini API with Hugging Face fallback
- **Comprehensive Results**: Individual review analysis + overall summary
- **Export Functionality**: Download results as CSV or JSON
- **Clean UI**: Bootstrap-based responsive interface

## Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd multilingual-sentiment-app
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
Create a `.env` file in the root directory:
```env
GEMINI_API_KEY=your_gemini_api_key_here
SECRET_KEY=your_secret_key_here
FLASK_DEBUG=false
```

To get a Gemini API key:
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Add it to your `.env` file

## Usage

1. **Start the application**
```bash
python app.py
```

2. **Access the web interface**
Open your browser and go to `http://localhost:5000`

3. **Analyze reviews**
   - **Option 1**: Upload a CSV file with reviews (column should be named 'review', 'text', 'comment', or 'feedback')
   - **Option 2**: Paste reviews in the text area (one per line)

4. **View results**
   - See individual sentiment analysis for each review
   - Get an overall summary with AI-generated insights
   - Download results as CSV or JSON

## API Endpoints

- `GET /` - Main input page
- `POST /analyze` - Process reviews and show results
- `GET /download/<format>` - Download results (format: csv or json)

## Testing

Run the test suite:
```bash
# Install test dependencies (already in requirements.txt)
pip install pytest pytest-flask

# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test file
pytest tests/test_integration.py -v
```

## Configuration

Edit `config.py` to modify:
- Model configurations
- File upload settings
- API endpoints
- Debug settings

## Project Structure

```
multilingual-sentiment-app/
│
├── app.py                # Flask entry point
├── config.py             # Configuration settings
├── requirements.txt      # Python dependencies
├── README.md             # This file
├── .env                  # Environment variables (create this)
│
├── pipeline/             # Core processing modules
│   ├── __init__.py
│   ├── detect.py         # Language detection
│   ├── translate.py      # Translation (Gemini + HF)
│   ├── sentiment.py      # Sentiment analysis
│   └── summarize.py      # AI summarization
│
├── templates/            # HTML templates
│   ├── base.html         # Base template
│   ├── index.html        # Input page
│   └── results.html      # Results page
│
├── static/              # Static files
│   └── style.css        # Custom CSS
│
├── utils/               # Utility functions
│   ├── __init__.py
│   ├── file_handler.py  # File processing
│   └── exporter.py      # Data export
│
└── tests/               # Test files
    ├── test_detect.py
    ├── test_translate.py
    ├── test_sentiment.py
    ├── test_summarize.py
    └── test_integration.py
```

## Dependencies

- **Flask**: Web framework
- **Transformers**: Hugging Face models for sentiment analysis
- **langdetect**: Language detection
- **google-generativeai**: Gemini API client
- **pandas**: Data processing
- **Bootstrap**: Frontend styling

## Supported Languages

The app can detect and process text in 20+ languages including:
- English, Spanish, French, German, Italian, Portuguese
- Russian, Chinese, Japanese, Korean, Arabic, Hindi
- Dutch, Swedish, Norwegian, Danish, Finnish
- Polish, Turkish, Thai, and more

## Troubleshooting

**Common Issues:**

1. **Import Errors**: Make sure all dependencies are installed: `pip install -r requirements.txt`

2. **Gemini API Errors**: 
   - Check your API key is valid
   - Ensure you have API quota available
   - App will fallback to Hugging Face translation if Gemini fails

3. **Model Download Issues**: 
   - First run may be slow as models download
   - Ensure stable internet connection
   - Models are cached locally after first download

4. **CSV Upload Issues**:
   - Ensure CSV has a column named 'review', 'text', 'comment', or 'feedback'
   - Check file encoding (UTF-8 recommended)
   - Maximum file size is 16MB

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## License

This project is licensed under the MIT License.
```

This completes the full multilingual sentiment analysis web application! The project includes:

✅ **Complete Flask Application** with all requested features
✅ **Clean Bootstrap UI** with responsive design
✅ **Multilingual Pipeline** (detection, translation, sentiment analysis)
✅ **AI-Powered Insights** using Gemini API with fallbacks
✅ **File Upload & Export** functionality
✅ **Comprehensive Test Suite** with unit and integration tests
✅ **Professional Documentation** with setup instructions

The app supports multiple input methods, processes reviews through a sophisticated AI pipeline, provides detailed results with export options, and includes a complete test suite. The code is production-ready with proper error handling, logging, and configuration management.