import pandas as pd
import json
import io

def export_to_csv(results):
    """
    Export results to CSV format.
    
    Args:
        results (list): List of sentiment analysis results
        
    Returns:
        bytes: CSV data as bytes
    """
    # Prepare data for CSV
    csv_data = []
    for result in results:
        csv_data.append({
            'ID': result['id'],
            'Original_Text': result['original_text'],
            'Detected_Language': result['detected_language'],
            'Translated_Text': result.get('translated_text', ''),
            'Sentiment_Label': result['sentiment_label'],
            'Confidence': result['confidence']
        })
    
    # Create DataFrame and convert to CSV
    df = pd.DataFrame(csv_data)
    output = io.StringIO()
    df.to_csv(output, index=False)
    return output.getvalue().encode('utf-8')

def export_to_json(results):
    """
    Export results to JSON format.
    
    Args:
        results (list): List of sentiment analysis results
        
    Returns:
        bytes: JSON data as bytes
    """
    # Create structured JSON output
    export_data = {
        'metadata': {
            'total_reviews': len(results),
            'export_format': 'json'
        },
        'results': results
    }
    
    return json.dumps(export_data, indent=2, ensure_ascii=False).encode('utf-8')