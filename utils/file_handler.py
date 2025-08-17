import pandas as pd
import csv
import io
import logging
from werkzeug.datastructures import FileStorage

def validate_file(file):
    """
    Validate uploaded file.
    
    Args:
        file (FileStorage): Uploaded file
        
    Returns:
        bool: True if valid, False otherwise
    """
    try:
        if not file or not file.filename:
            return False
        
        # Check file extension
        allowed_extensions = ['csv', 'txt']
        extension = file.filename.rsplit('.', 1)[1].lower()
        
        return extension in allowed_extensions
    except Exception:
        return False

def process_csv_file(file):
    """
    Process uploaded CSV file and extract reviews.
    
    Args:
        file (FileStorage): Uploaded CSV file
        
    Returns:
        list: List of review texts
    """
    reviews = []
    
    try:
        # Read file content
        content = file.read().decode('utf-8')
        file.seek(0)  # Reset file pointer
        
        # Try to parse as CSV
        df = pd.read_csv(io.StringIO(content))
        
        # Look for review column (case-insensitive)
        review_column = None
        for col in df.columns:
            if col.lower() in ['review', 'reviews', 'text', 'comment', 'feedback', 'content']:
                review_column = col
                break
        
        if review_column:
            reviews = df[review_column].dropna().tolist()
        else:
            # If no standard column found, use first column
            if not df.empty:
                reviews = df.iloc[:, 0].dropna().tolist()
        
        # Convert to strings and filter empty reviews
        reviews = [str(review).strip() for review in reviews if str(review).strip()]
        
    except Exception as e:
        logging.error(f"CSV processing failed: {e}")
        # Try to read as plain text
        try:
            file.seek(0)
            content = file.read().decode('utf-8')
            reviews = [line.strip() for line in content.split('\n') if line.strip()]
        except Exception as e2:
            logging.error(f"Text processing failed: {e2}")
            reviews = []
    
    return reviews

def process_text_file(file):
    """
    Process uploaded text file.
    
    Args:
        file (FileStorage): Uploaded text file
        
    Returns:
        list: List of review texts (one per line)
    """
    reviews = []
    
    try:
        content = file.read().decode('utf-8')
        reviews = [line.strip() for line in content.split('\n') if line.strip()]
    except Exception as e:
        logging.error(f"Text file processing failed: {e}")
    
    return reviews