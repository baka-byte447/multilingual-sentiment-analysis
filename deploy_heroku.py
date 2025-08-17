#!/usr/bin/env python3
"""
Heroku Deployment Helper Script
This script helps set up and deploy the Streamlit app to Heroku
"""

import os
import subprocess
import sys

def check_heroku_cli():
    """Check if Heroku CLI is available"""
    try:
        result = subprocess.run(['heroku', '--version'], 
                              capture_output=True, text=True, shell=True)
        if result.returncode == 0:
            print(f"✅ Heroku CLI found: {result.stdout.strip()}")
            return True
        else:
            print("❌ Heroku CLI not working properly")
            return False
    except FileNotFoundError:
        print("❌ Heroku CLI not found. Please restart your terminal after installation.")
        return False

def create_heroku_app(app_name):
    """Create a new Heroku app"""
    try:
        print(f"🚀 Creating Heroku app: {app_name}")
        result = subprocess.run(['heroku', 'create', app_name], 
                              capture_output=True, text=True, shell=True)
        if result.returncode == 0:
            print(f"✅ Heroku app created: {result.stdout.strip()}")
            return True
        else:
            print(f"❌ Failed to create app: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error creating app: {e}")
        return False

def set_environment_variables():
    """Set environment variables on Heroku"""
    try:
        # Get API key from .env file
        from dotenv import load_dotenv
        load_dotenv()
        
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            print("❌ GEMINI_API_KEY not found in .env file")
            return False
        
        print("🔧 Setting environment variables on Heroku...")
        
        # Set GEMINI_API_KEY
        result = subprocess.run(['heroku', 'config:set', f'GEMINI_API_KEY={api_key}'], 
                              capture_output=True, text=True, shell=True)
        if result.returncode == 0:
            print("✅ GEMINI_API_KEY set successfully")
        else:
            print(f"❌ Failed to set GEMINI_API_KEY: {result.stderr}")
            return False
        
        # Set other environment variables
        env_vars = {
            'SECRET_KEY': 'your-super-secret-key-change-this-in-production',
            'FLASK_DEBUG': 'false'
        }
        
        for key, value in env_vars.items():
            result = subprocess.run(['heroku', 'config:set', f'{key}={value}'], 
                                  capture_output=True, text=True, shell=True)
            if result.returncode == 0:
                print(f"✅ {key} set successfully")
            else:
                print(f"❌ Failed to set {key}: {result.stderr}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error setting environment variables: {e}")
        return False

def deploy_to_heroku():
    """Deploy the app to Heroku"""
    try:
        print("🚀 Deploying to Heroku...")
        
        # Add Heroku remote if not exists
        result = subprocess.run(['git', 'remote', 'get-url', 'heroku'], 
                              capture_output=True, text=True, shell=True)
        if result.returncode != 0:
            print("📡 Adding Heroku remote...")
            subprocess.run(['heroku', 'git:remote', '-a', 'your-app-name'], 
                         shell=True, check=True)
        
        # Push to Heroku
        print("📤 Pushing to Heroku...")
        result = subprocess.run(['git', 'push', 'heroku', 'main'], 
                              capture_output=True, text=True, shell=True)
        if result.returncode == 0:
            print("✅ Deployment successful!")
            return True
        else:
            print(f"❌ Deployment failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error during deployment: {e}")
        return False

def open_heroku_app():
    """Open the deployed app in browser"""
    try:
        print("🌐 Opening Heroku app...")
        subprocess.run(['heroku', 'open'], shell=True)
        return True
    except Exception as e:
        print(f"❌ Error opening app: {e}")
        return False

def main():
    """Main deployment process"""
    print("🚀 Heroku Deployment Helper")
    print("=" * 40)
    
    # Check if Heroku CLI is available
    if not check_heroku_cli():
        print("\n📋 To install Heroku CLI manually:")
        print("1. Download from: https://devcenter.heroku.com/articles/heroku-cli")
        print("2. Install and restart your terminal")
        print("3. Run this script again")
        return
    
    print("\n📋 Deployment Steps:")
    print("1. Create Heroku app")
    print("2. Set environment variables")
    print("3. Deploy the app")
    print("4. Open the app")
    
    # Get app name from user
    app_name = input("\nEnter your Heroku app name (or press Enter for auto-generated): ").strip()
    if not app_name:
        app_name = None
    
    # Step 1: Create app
    if app_name:
        if not create_heroku_app(app_name):
            print("❌ Failed to create app. Please try again.")
            return
    else:
        print("📝 Please create a Heroku app manually:")
        print("   heroku create your-app-name")
        print("   Then run this script again.")
        return
    
    # Step 2: Set environment variables
    if not set_environment_variables():
        print("❌ Failed to set environment variables.")
        return
    
    # Step 3: Deploy
    if not deploy_to_heroku():
        print("❌ Deployment failed.")
        return
    
    # Step 4: Open app
    open_heroku_app()
    
    print("\n🎉 Deployment completed successfully!")
    print(f"Your app is now live at: https://{app_name}.herokuapp.com")

if __name__ == "__main__":
    main()
