# 🚀 Heroku Deployment Guide

This guide will walk you through deploying your Multilingual Sentiment Analysis app to Heroku step by step.

## 📋 Prerequisites

1. **GitHub Repository**: Your code should be in a GitHub repository
2. **Heroku Account**: Sign up at [heroku.com](https://heroku.com)
3. **Heroku CLI**: Install the command line interface
4. **Python 3.11+**: Ensure compatibility

## 🔧 Step-by-Step Deployment

### Step 1: Install Heroku CLI

**Windows (PowerShell):**
```powershell
winget install --id=Heroku.HerokuCLI -e
```

**macOS:**
```bash
brew tap heroku/brew && brew install heroku
```

**Linux:**
```bash
curl https://cli-assets.heroku.com/install.sh | sh
```

**After installation, restart your terminal/command prompt.**

### Step 2: Login to Heroku

```bash
heroku login
```

This will open your browser to authenticate with Heroku.

### Step 3: Create Heroku App

```bash
heroku create your-app-name
```

Replace `your-app-name` with your desired app name (must be unique across all of Heroku).

**Example:**
```bash
heroku create multilingual-sentiment-app-2024
```

### Step 4: Set Environment Variables

Set your Gemini API key and other configuration:

```bash
heroku config:set GEMINI_API_KEY="your-actual-api-key-here"
heroku config:set SECRET_KEY="your-super-secret-key-change-this-in-production"
heroku config:set FLASK_DEBUG="false"
```

**Important:** Replace `your-actual-api-key-here` with your real Gemini API key from the `.env` file.

### Step 5: Add Heroku Remote (if needed)

```bash
heroku git:remote -a your-app-name
```

### Step 6: Deploy to Heroku

```bash
git push heroku main
```

### Step 7: Open Your App

```bash
heroku open
```

## 🐛 Troubleshooting

### Common Issues:

1. **"heroku: command not found"**
   - Restart your terminal after installation
   - Ensure Heroku CLI is in your PATH

2. **Build fails during deployment**
   - Check that all dependencies are in `requirements.txt`
   - Ensure Python version compatibility (3.11+)

3. **App crashes on startup**
   - Check Heroku logs: `heroku logs --tail`
   - Verify environment variables are set correctly

4. **Memory issues**
   - The app uses transformers which require significant memory
   - Consider upgrading to a paid Heroku dyno if needed

### Check Logs:

```bash
heroku logs --tail
```

This shows real-time logs to help debug issues.

## 📊 App Configuration

Your app includes these deployment-ready files:

- `streamlit_app.py` - Main Streamlit application
- `requirements.txt` - Python dependencies
- `Procfile` - Tells Heroku how to run the app
- `runtime.txt` - Specifies Python version
- `.streamlit/config.toml` - Streamlit configuration

## 🔒 Security Notes

1. **Never commit API keys** to your repository
2. **Use environment variables** for sensitive data
3. **The app includes input validation** and sanitization
4. **File uploads are restricted** to safe formats

## 📱 Testing Your Deployment

After deployment:

1. **Test text input** with sample reviews
2. **Test file upload** with a small CSV file
3. **Verify language detection** works
4. **Check sentiment analysis** functionality
5. **Test download features**

## 🚀 Performance Tips

1. **Model Caching**: The app caches translation models
2. **Batch Processing**: Large files are processed efficiently
3. **Progress Indicators**: Users see real-time feedback
4. **Error Handling**: Graceful fallbacks for failures

## 📞 Support

If you encounter issues:

1. **Check Heroku logs**: `heroku logs --tail`
2. **Verify environment variables**: `heroku config`
3. **Ensure API key has sufficient quota**
4. **Test locally before deploying**

## 🎯 Quick Commands Reference

```bash
# Create app
heroku create your-app-name

# Set config
heroku config:set GEMINI_API_KEY="your-key"

# Deploy
git push heroku main

# Open app
heroku open

# Check logs
heroku logs --tail

# Check config
heroku config

# Restart app
heroku restart
```

---

**Happy Deploying! 🎉**

Your app will be available at: `https://your-app-name.herokuapp.com`
