from flask import Flask, render_template, request, jsonify, send_file
import io
import json
import pandas as pd
from werkzeug.utils import secure_filename
from config import Config
from pipeline.detect import detect_language
from pipeline.translate import translate_text
from pipeline.sentiment import analyze_sentiment
from pipeline.summarize import generate_summary
from utils.file_handler import process_csv_file, validate_file
from utils.exporter import export_to_csv, export_to_json



app = Flask(__name__)
app.config.from_object(Config)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        reviews = []
        
        # Handle file upload
        if 'file' in request.files and request.files['file'].filename:
            file = request.files['file']
            if file and allowed_file(file.filename):
                if validate_file(file):
                    reviews.extend(process_csv_file(file))
                else:
                    return render_template('index.html', error="Invalid file format")
            else:
                return render_template('index.html', error="Invalid file type. Please upload CSV or TXT files.")
        
        # Handle text input
        text_input = request.form.get('text_reviews', '').strip()
        if text_input:
            text_reviews = [line.strip() for line in text_input.split('\n') if line.strip()]
            reviews.extend(text_reviews)
        
        if not reviews:
            return render_template('index.html', error="Please provide reviews either through file upload or text input.")
        
        # Process reviews through pipeline
        results = []
        for i, review in enumerate(reviews):
            if not review.strip():
                continue
                
            # Detect language
            detected_lang = detect_language(review)
            
            # Translate if needed
            translated_text = review
            if detected_lang != 'en':
                translated_text = translate_text(review, detected_lang)
            
            # Analyze sentiment
            sentiment_result = analyze_sentiment(translated_text)
            
            results.append({
                'id': i + 1,
                'original_text': review,
                'detected_language': detected_lang,
                'translated_text': translated_text if detected_lang != 'en' else None,
                'sentiment_label': sentiment_result['label'],
                'confidence': sentiment_result['confidence']
            })
        
        # Generate overall summary
        summary = generate_summary(results)
        
        return render_template('results.html', results=results, summary=summary)
        
    except Exception as e:
        return render_template('index.html', error=f"An error occurred: {str(e)}")

@app.route('/download/<format>')
def download(format):
    try:
        results = request.args.get('data')
        if not results:
            return jsonify({'error': 'No data to download'}), 400
        
        data = json.loads(results)
        
        if format == 'csv':
            output = export_to_csv(data)
            return send_file(
                io.BytesIO(output),
                mimetype='text/csv',
                as_attachment=True,
                download_name='sentiment_analysis_results.csv'
            )
        elif format == 'json':
            output = export_to_json(data)
            return send_file(
                io.BytesIO(output),
                mimetype='application/json',
                as_attachment=True,
                download_name='sentiment_analysis_results.json'
            )
        else:
            return jsonify({'error': 'Invalid format'}), 400
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'])