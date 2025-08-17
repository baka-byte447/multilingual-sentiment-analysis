# 🚀 Streamlit Deployment Guide

This guide will help you deploy the Multilingual Sentiment Analysis app to various platforms.

## 📋 Prerequisites

1. **GitHub Repository**: Your code should be in a GitHub repository
2. **Environment Variables**: Set up your `GEMINI_API_KEY` in the deployment platform
3. **Python 3.11+**: The app requires Python 3.11 or higher

## 🌐 Deployment Options

### 1. Streamlit Cloud (Recommended)

**Steps:**
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with your GitHub account
3. Click "New app"
4. Select your repository: `baka-byte447/multilingual-sentiment-analysis`
5. Set the main file path: `streamlit_app.py`
6. Add your secrets in the "Secrets" section:
   ```
   GEMINI_API_KEY = "your-api-key-here"
   SECRET_KEY = "your-secret-key-here"
   ```
7. Click "Deploy"

**Advantages:**
- Free tier available
- Automatic deployments from GitHub
- Built-in secrets management
- Easy to use

### 2. Heroku

**Steps:**
1. Install Heroku CLI
2. Create a new Heroku app:
   ```bash
   heroku create your-app-name
   ```
3. Set environment variables:
   ```bash
   heroku config:set GEMINI_API_KEY="your-api-key-here"
   heroku config:set SECRET_KEY="your-secret-key-here"
   ```
4. Deploy:
   ```bash
   git push heroku main
   ```

### 3. Railway

**Steps:**
1. Go to [railway.app](https://railway.app)
2. Connect your GitHub repository
3. Add environment variables in the dashboard
4. Deploy automatically

### 4. Render

**Steps:**
1. Go to [render.com](https://render.com)
2. Create a new Web Service
3. Connect your GitHub repository
4. Set build command: `pip install -r requirements.txt`
5. Set start command: `streamlit run streamlit_app.py --server.port=$PORT --server.address=0.0.0.0`
6. Add environment variables
7. Deploy

## 🔧 Environment Variables

Make sure to set these environment variables in your deployment platform:

```bash
GEMINI_API_KEY=your-gemini-api-key-here
SECRET_KEY=your-secret-key-here
FLASK_DEBUG=false
```

## 📁 File Structure

Your deployment should include these files:

```
├── streamlit_app.py          # Main Streamlit application
├── requirements.txt          # Python dependencies
├── packages.txt             # System dependencies
├── Procfile                 # For Heroku/Railway
├── runtime.txt              # Python version
├── .streamlit/
│   └── config.toml         # Streamlit configuration
├── pipeline/                # Analysis pipeline
├── utils/                   # Utility functions
└── config.py               # Configuration settings
```

## 🐛 Troubleshooting

### Common Issues:

1. **Import Errors**: Make sure all dependencies are in `requirements.txt`
2. **API Key Issues**: Verify your `GEMINI_API_KEY` is set correctly
3. **Memory Issues**: The app uses transformers, so ensure adequate memory allocation
4. **Port Issues**: Make sure the port is set to `$PORT` for cloud deployments

### Debug Mode:

To run locally for testing:
```bash
streamlit run streamlit_app.py
```

## 📊 Performance Tips

1. **Model Caching**: The app caches translation models for better performance
2. **Batch Processing**: Large files are processed in batches
3. **Progress Indicators**: Users see progress bars during analysis
4. **Error Handling**: Graceful fallbacks for API failures

## 🔒 Security Notes

1. Never commit API keys to your repository
2. Use environment variables for sensitive data
3. The app includes input validation and sanitization
4. File uploads are restricted to safe formats

## 📞 Support

If you encounter issues:
1. Check the deployment platform logs
2. Verify all environment variables are set
3. Ensure your API key has sufficient quota
4. Test locally before deploying

---

**Happy Deploying! 🎉**
