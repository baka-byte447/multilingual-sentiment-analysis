@echo off
echo Fixing installation...
if exist venv rmdir /s /q venv
python -m venv venv
call venv\Scripts\activate
python -m pip install --upgrade pip setuptools wheel
python -m pip install flask pandas requests python-dotenv langdetect
python -m pip install torch --index-url https://download.pytorch.org/whl/cpu
python -m pip install transformers google-generativeai
python -m pip install pytest pytest-flask
echo ✅ Installation complete!
python -c "import flask, torch; print('Success! All packages working.')"
pause