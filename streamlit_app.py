import streamlit as st
import pandas as pd
import json
import io
from config import Config
from pipeline.detect import detect_language
from pipeline.translate import translate_text
from pipeline.sentiment import analyze_sentiment
from pipeline.summarize import generate_summary
from utils.file_handler import process_csv_file, validate_file
from utils.exporter import export_to_csv, export_to_json

# Page configuration
st.set_page_config(
    page_title="Multilingual Sentiment Analysis",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .sentiment-positive {
        color: #28a745;
        font-weight: bold;
    }
    .sentiment-negative {
        color: #dc3545;
        font-weight: bold;
    }
    .sentiment-neutral {
        color: #6c757d;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Header
    st.markdown('<h1 class="main-header">🌍 Multilingual Sentiment Analysis</h1>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Sidebar for input options
    with st.sidebar:
        st.header("📥 Input Options")
        input_method = st.radio(
            "Choose input method:",
            ["Text Input", "File Upload"],
            index=0
        )
        
        st.markdown("---")
        st.header("⚙️ Settings")
        show_translations = st.checkbox("Show translations", value=True)
        show_confidence = st.checkbox("Show confidence scores", value=True)
        
        st.markdown("---")
        st.header("ℹ️ About")
        st.info("""
        This app analyzes sentiment in multiple languages:
        - Detects language automatically
        - Translates non-English text
        - Provides sentiment analysis
        - Generates AI-powered insights
        """)
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("📝 Input Data")
        
        if input_method == "Text Input":
            text_input = st.text_area(
                "Enter reviews (one per line):",
                height=200,
                placeholder="Enter your reviews here...\nOne review per line\n\nExample:\nThis product is amazing!\nI'm not satisfied with the service.\nThe quality is okay."
            )
            
            if st.button("🚀 Analyze Sentiment", type="primary", use_container_width=True):
                if text_input.strip():
                    process_text_input(text_input, show_translations, show_confidence)
                else:
                    st.error("Please enter some text to analyze.")
        
        else:  # File Upload
            uploaded_file = st.file_uploader(
                "Upload a CSV or TXT file:",
                type=['csv', 'txt'],
                help="Upload a file with reviews. CSV should have a 'text' or 'review' column."
            )
            
            if uploaded_file is not None:
                if st.button("🚀 Analyze Sentiment", type="primary", use_container_width=True):
                    process_file_upload(uploaded_file, show_translations, show_confidence)
    
    with col2:
        st.header("📊 Quick Stats")
        if 'results' in st.session_state and st.session_state.results:
            display_quick_stats(st.session_state.results)

def process_text_input(text_input, show_translations, show_confidence):
    """Process text input and analyze sentiment"""
    with st.spinner("🔍 Analyzing sentiment..."):
        reviews = [line.strip() for line in text_input.split('\n') if line.strip()]
        results = analyze_reviews(reviews, show_translations, show_confidence)
        st.session_state.results = results
        display_results(results, show_translations, show_confidence)

def process_file_upload(uploaded_file, show_translations, show_confidence):
    """Process uploaded file and analyze sentiment"""
    with st.spinner("🔍 Analyzing sentiment..."):
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
                # Try to find the text column
                text_columns = [col for col in df.columns if 'text' in col.lower() or 'review' in col.lower()]
                if text_columns:
                    reviews = df[text_columns[0]].dropna().tolist()
                else:
                    reviews = df.iloc[:, 0].dropna().tolist()  # Use first column
            else:  # txt file
                content = uploaded_file.read().decode('utf-8')
                reviews = [line.strip() for line in content.split('\n') if line.strip()]
            
            results = analyze_reviews(reviews, show_translations, show_confidence)
            st.session_state.results = results
            display_results(results, show_translations, show_confidence)
            
        except Exception as e:
            st.error(f"Error processing file: {str(e)}")

def analyze_reviews(reviews, show_translations, show_confidence):
    """Analyze sentiment for a list of reviews"""
    results = []
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for i, review in enumerate(reviews):
        if not review.strip():
            continue
        
        status_text.text(f"Processing review {i+1}/{len(reviews)}...")
        
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
        
        progress_bar.progress((i + 1) / len(reviews))
    
    status_text.text("✅ Analysis complete!")
    progress_bar.empty()
    status_text.empty()
    
    return results

def display_results(results, show_translations, show_confidence):
    """Display analysis results"""
    st.markdown("---")
    st.header("📈 Analysis Results")
    
    # Generate summary
    summary = generate_summary(results)
    
    # Display summary metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Reviews", summary['total_reviews'])
    
    with col2:
        sentiment_color = {
            'Positive': 'green',
            'Negative': 'red',
            'Mixed': 'orange',
            'Neutral': 'gray'
        }.get(summary['overall_sentiment'], 'blue')
        st.metric("Overall Sentiment", summary['overall_sentiment'])
    
    with col3:
        positive_pct = summary['distribution']['Positive']
        st.metric("Positive", f"{positive_pct:.1f}%")
    
    with col4:
        negative_pct = summary['distribution']['Negative']
        st.metric("Negative", f"{negative_pct:.1f}%")
    
    # Display AI insights
    st.subheader("🤖 AI Insights")
    st.info(summary['insights'])
    
    # Display detailed results
    st.subheader("📋 Detailed Results")
    
    # Create DataFrame for display
    display_data = []
    for result in results:
        row = {
            'ID': result['id'],
            'Original Text': result['original_text'][:100] + ('...' if len(result['original_text']) > 100 else ''),
            'Language': result['detected_language'].upper(),
            'Sentiment': result['sentiment_label']
        }
        
        if show_translations and result['translated_text']:
            row['Translation'] = result['translated_text'][:100] + ('...' if len(result['translated_text']) > 100 else '')
        
        if show_confidence:
            row['Confidence'] = f"{result['confidence']:.2f}"
        
        display_data.append(row)
    
    df_display = pd.DataFrame(display_data)
    st.dataframe(df_display, use_container_width=True)
    
    # Download options
    st.subheader("💾 Download Results")
    col1, col2 = st.columns(2)
    
    with col1:
        csv_data = export_to_csv(results)
        st.download_button(
            label="📥 Download as CSV",
            data=csv_data,
            file_name="sentiment_analysis_results.csv",
            mime="text/csv"
        )
    
    with col2:
        json_data = export_to_json(results)
        st.download_button(
            label="📥 Download as JSON",
            data=json_data,
            file_name="sentiment_analysis_results.json",
            mime="application/json"
        )

def display_quick_stats(results):
    """Display quick statistics in the sidebar"""
    if not results:
        st.info("No results to display")
        return
    
    total = len(results)
    positive = len([r for r in results if r['sentiment_label'] == 'Positive'])
    negative = len([r for r in results if r['sentiment_label'] == 'Negative'])
    neutral = len([r for r in results if r['sentiment_label'] == 'Neutral'])
    
    st.metric("Total", total)
    st.metric("Positive", positive)
    st.metric("Negative", negative)
    st.metric("Neutral", neutral)
    
    # Language distribution
    languages = {}
    for result in results:
        lang = result['detected_language']
        languages[lang] = languages.get(lang, 0) + 1
    
    st.subheader("🌍 Languages")
    for lang, count in languages.items():
        st.write(f"{lang.upper()}: {count}")

if __name__ == "__main__":
    main()
