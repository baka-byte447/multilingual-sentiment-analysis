import streamlit as st
import pandas as pd
import json
import io
import time
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
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state for theme
if 'current_theme' not in st.session_state:
    st.session_state.current_theme = 'default'
if 'theme_transition' not in st.session_state:
    st.session_state.theme_transition = False

# Dynamic theme definitions based on sentiment
THEMES = {
    'default': {
        'primary': '#1a1a2e',
        'secondary': '#16213e',
        'accent': '#0f3460',
        'text': '#e94560',
        'background': '#0f0f23',
        'card_bg': '#1a1a2e',
        'border': '#e94560',
        'gradient': 'linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%)'
    },
    'positive': {
        'primary': '#1a2e1a',
        'secondary': '#162e16',
        'accent': '#0f5a0f',
        'text': '#45e945',
        'background': '#0f230f',
        'card_bg': '#1a2e1a',
        'border': '#45e945',
        'gradient': 'linear-gradient(135deg, #0f230f 0%, #1a2e1a 50%, #162e16 100%)'
    },
    'negative': {
        'primary': '#2e1a1a',
        'secondary': '#2e1616',
        'accent': '#5a0f0f',
        'text': '#e94545',
        'background': '#230f0f',
        'card_bg': '#2e1a1a',
        'border': '#e94545',
        'gradient': 'linear-gradient(135deg, #230f0f 0%, #2e1a1a 50%, #2e1616 100%)'
    },
    'neutral': {
        'primary': '#2e2e1a',
        'secondary': '#2e2e16',
        'accent': '#5a5a0f',
        'text': '#e9e945',
        'background': '#23230f',
        'card_bg': '#2e2e1a',
        'border': '#e9e945',
        'gradient': 'linear-gradient(135deg, #23230f 0%, #2e2e1a 50%, #2e2e16 100%)'
    },
    'mixed': {
        'primary': '#2e1a2e',
        'secondary': '#2e162e',
        'accent': '#5a0f5a',
        'text': '#e945e9',
        'background': '#230f23',
        'card_bg': '#2e1a2e',
        'border': '#e945e9',
        'gradient': 'linear-gradient(135deg, #230f23 0%, #2e1a2e 50%, #2e162e 100%)'
    }
}

def get_current_theme():
    """Get the current theme based on sentiment"""
    return THEMES.get(st.session_state.current_theme, THEMES['default'])

def apply_theme_transition(new_theme):
    """Apply smooth theme transition"""
    st.session_state.theme_transition = True
    st.session_state.current_theme = new_theme
    time.sleep(0.1)  # Small delay for transition effect

def get_css(theme):
    """Generate dynamic CSS based on current theme"""
    return f"""
    <style>
        /* Global Theme Variables */
        :root {{
            --primary-color: {theme['primary']};
            --secondary-color: {theme['secondary']};
            --accent-color: {theme['accent']};
            --text-color: {theme['text']};
            --background-color: {theme['background']};
            --card-bg: {theme['card_bg']};
            --border-color: {theme['border']};
            --gradient: {theme['gradient']};
        }}
        
        /* Smooth Theme Transitions */
        * {{
            transition: all 0.6s cubic-bezier(0.4, 0, 0.2, 1) !important;
        }}
        
        /* Main Background */
        .main {{
            background: var(--gradient) !important;
            min-height: 100vh;
        }}
        
        /* Custom Scrollbar */
        ::-webkit-scrollbar {{
            width: 12px;
        }}
        
        ::-webkit-scrollbar-track {{
            background: var(--secondary-color);
            border-radius: 10px;
        }}
        
        ::-webkit-scrollbar-thumb {{
            background: var(--accent-color);
            border-radius: 10px;
            border: 2px solid var(--secondary-color);
        }}
        
        ::-webkit-scrollbar-thumb:hover {{
            background: var(--text-color);
        }}
        
        /* Header Styling */
        .main-header {{
            font-size: 4rem;
            font-weight: 900;
            text-align: center;
            color: var(--text-color);
            margin-bottom: 2rem;
            text-shadow: 0 0 30px var(--text-color);
            animation: glow 2s ease-in-out infinite alternate;
            background: linear-gradient(45deg, var(--text-color), var(--accent-color));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}
        
        @keyframes glow {{
            from {{ filter: drop-shadow(0 0 20px var(--text-color)); }}
            to {{ filter: drop-shadow(0 0 30px var(--accent-color)); }}
        }}
        
        /* Sidebar Styling */
        .css-1d391kg {{
            background: var(--card-bg) !important;
            border-right: 3px solid var(--border-color) !important;
        }}
        
        /* Card Styling */
        .metric-card {{
            background: var(--card-bg) !important;
            padding: 1.5rem;
            border-radius: 15px;
            border: 2px solid var(--border-color);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
            backdrop-filter: blur(10px);
            transition: all 0.3s ease;
        }}
        
        .metric-card:hover {{
            transform: translateY(-5px) scale(1.02);
            box-shadow: 0 15px 45px rgba(0, 0, 0, 0.4);
            border-color: var(--text-color);
        }}
        
        /* Button Styling */
        .stButton > button {{
            background: linear-gradient(45deg, var(--accent-color), var(--text-color)) !important;
            border: none !important;
            border-radius: 25px !important;
            padding: 12px 30px !important;
            font-weight: bold !important;
            text-transform: uppercase !important;
            letter-spacing: 1px !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3) !important;
        }}
        
        .stButton > button:hover {{
            transform: translateY(-2px) scale(1.05) !important;
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.4) !important;
            filter: brightness(1.2) !important;
        }}
        
        /* Input Styling */
        .stTextArea textarea {{
            background: var(--card-bg) !important;
            border: 2px solid var(--border-color) !important;
            border-radius: 15px !important;
            color: var(--text-color) !important;
            font-size: 16px !important;
            padding: 15px !important;
            transition: all 0.3s ease !important;
        }}
        
        .stTextArea textarea:focus {{
            border-color: var(--text-color) !important;
            box-shadow: 0 0 20px var(--text-color) !important;
            transform: scale(1.02) !important;
        }}
        
        /* File Uploader */
        .stFileUploader {{
            background: var(--card-bg) !important;
            border: 2px dashed var(--border-color) !important;
            border-radius: 15px !important;
            padding: 20px !important;
            transition: all 0.3s ease !important;
        }}
        
        .stFileUploader:hover {{
            border-color: var(--text-color) !important;
            background: var(--secondary-color) !important;
        }}
        
        /* Metrics */
        .stMetric {{
            background: var(--card-bg) !important;
            padding: 20px !important;
            border-radius: 15px !important;
            border: 2px solid var(--border-color) !important;
            transition: all 0.3s ease !important;
        }}
        
        .stMetric:hover {{
            transform: translateY(-3px) scale(1.03) !important;
            border-color: var(--text-color) !important;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4) !important;
        }}
        
        /* Dataframe */
        .stDataFrame {{
            background: var(--card-bg) !important;
            border-radius: 15px !important;
            border: 2px solid var(--border-color) !important;
            overflow: hidden !important;
        }}
        
        /* Progress Bar */
        .stProgress > div > div {{
            background: linear-gradient(90deg, var(--accent-color), var(--text-color)) !important;
            border-radius: 10px !important;
        }}
        
        /* Spinner */
        .stSpinner > div {{
            border-color: var(--text-color) !important;
            border-top-color: var(--accent-color) !important;
        }}
        
        /* Info Boxes */
        .stAlert {{
            background: var(--card-bg) !important;
            border: 2px solid var(--border-color) !important;
            border-radius: 15px !important;
            color: var(--text-color) !important;
        }}
        
        /* Hover Effects for Whole Page */
        .main:hover {{
            filter: brightness(1.05) contrast(1.1);
        }}
        
        /* Floating Particles Effect */
        .particles {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: -1;
        }}
        
        .particle {{
            position: absolute;
            width: 4px;
            height: 4px;
            background: var(--text-color);
            border-radius: 50%;
            animation: float 6s infinite linear;
            opacity: 0.6;
        }}
        
        @keyframes float {{
            0% {{ transform: translateY(100vh) rotate(0deg); opacity: 0; }}
            10% {{ opacity: 0.6; }}
            90% {{ opacity: 0.6; }}
            100% {{ transform: translateY(-100px) rotate(360deg); opacity: 0; }}
        }}
        
        /* Sentiment-specific animations */
        .sentiment-positive {{
            animation: positivePulse 2s ease-in-out infinite;
        }}
        
        .sentiment-negative {{
            animation: negativePulse 2s ease-in-out infinite;
        }}
        
        .sentiment-neutral {{
            animation: neutralPulse 2s ease-in-out infinite;
        }}
        
        @keyframes positivePulse {{
            0%, 100% {{ transform: scale(1); }}
            50% {{ transform: scale(1.05); }}
        }}
        
        @keyframes negativePulse {{
            0%, 100% {{ transform: scale(1); }}
            50% {{ transform: scale(0.95); }}
        }}
        
        @keyframes neutralPulse {{
            0%, 100% {{ transform: scale(1); }}
            50% {{ transform: scale(1.02); }}
        }}
        
        /* Responsive Design */
        @media (max-width: 768px) {{
            .main-header {{
                font-size: 2.5rem;
            }}
        }}
    </style>
    
    <!-- Floating Particles -->
    <div class="particles">
        <div class="particle" style="left: 10%; animation-delay: 0s;"></div>
        <div class="particle" style="left: 20%; animation-delay: 1s;"></div>
        <div class="particle" style="left: 30%; animation-delay: 2s;"></div>
        <div class="particle" style="left: 40%; animation-delay: 3s;"></div>
        <div class="particle" style="left: 50%; animation-delay: 4s;"></div>
        <div class="particle" style="left: 60%; animation-delay: 5s;"></div>
        <div class="particle" style="left: 70%; animation-delay: 6s;"></div>
        <div class="particle" style="left: 80%; animation-delay: 7s;"></div>
        <div class="particle" style="left: 90%; animation-delay: 8s;"></div>
    </div>
    """

def main():
    # Get current theme
    theme = get_current_theme()
    
    # Apply CSS
    st.markdown(get_css(theme), unsafe_allow_html=True)
    
    # Header with dynamic theme
    st.markdown('<h1 class="main-header">🌌 Multilingual Sentiment Analysis</h1>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Sidebar with enhanced styling
    with st.sidebar:
        st.markdown(f"""
        <div style="
            background: {theme['card_bg']};
            padding: 20px;
            border-radius: 15px;
            border: 2px solid {theme['border']};
            margin-bottom: 20px;
        ">
            <h2 style="color: {theme['text']}; text-align: center;">🎛️ Control Panel</h2>
        </div>
        """, unsafe_allow_html=True)
        
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
        st.header("🎨 Theme Preview")
        theme_preview = st.selectbox(
            "Preview themes:",
            ["default", "positive", "negative", "neutral", "mixed"],
            index=0
        )
        
        if st.button("Apply Theme Preview"):
            apply_theme_transition(theme_preview)
            st.rerun()
        
        st.markdown("---")
        st.header("ℹ️ About")
        st.info("""
        **AI-Powered Sentiment Analysis**
        
        ✨ **Features:**
        - 🌍 Multi-language support
        - 🔍 Automatic language detection
        - 📊 Real-time sentiment analysis
        - 🤖 AI-powered insights
        - 🎨 Dynamic theme system
        """)
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(f"""
        <div style="
            background: {theme['card_bg']};
            padding: 25px;
            border-radius: 20px;
            border: 3px solid {theme['border']};
            margin-bottom: 20px;
        ">
            <h2 style="color: {theme['text']}; text-align: center;">📝 Input Data</h2>
        </div>
        """, unsafe_allow_html=True)
        
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
        st.markdown(f"""
        <div style="
            background: {theme['card_bg']};
            padding: 20px;
            border-radius: 15px;
            border: 2px solid {theme['border']};
        ">
            <h3 style="color: {theme['text']}; text-align: center;">📊 Quick Stats</h3>
        </div>
        """, unsafe_allow_html=True)
        
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
    """Display analysis results with dynamic theming"""
    theme = get_current_theme()
    
    st.markdown("---")
    
    # Generate summary
    summary = generate_summary(results)
    
    # Determine overall theme based on sentiment
    overall_sentiment = summary['overall_sentiment'].lower()
    if overall_sentiment in ['positive', 'negative', 'neutral', 'mixed']:
        apply_theme_transition(overall_sentiment)
        theme = get_current_theme()
        st.rerun()
    
    st.markdown(f"""
    <div style="
        background: {theme['card_bg']};
        padding: 30px;
        border-radius: 20px;
        border: 3px solid {theme['border']};
        margin: 20px 0;
    ">
        <h2 style="color: {theme['text']}; text-align: center;">📈 Analysis Results</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Display summary metrics with enhanced styling
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Reviews", summary['total_reviews'])
    
    with col2:
        st.metric("Overall Sentiment", summary['overall_sentiment'])
    
    with col3:
        positive_pct = summary['distribution']['Positive']
        st.metric("Positive", f"{positive_pct:.1f}%")
    
    with col4:
        negative_pct = summary['distribution']['Negative']
        st.metric("Negative", f"{negative_pct:.1f}%")
    
    # Display AI insights with enhanced styling
    st.markdown(f"""
    <div style="
        background: {theme['card_bg']};
        padding: 25px;
        border-radius: 15px;
        border: 2px solid {theme['border']};
        margin: 20px 0;
    ">
        <h3 style="color: {theme['text']}; margin-bottom: 15px;">🤖 AI Insights</h3>
        <p style="color: {theme['text']}; font-size: 16px; line-height: 1.6;">{summary['insights']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Display detailed results
    st.markdown(f"""
    <div style="
        background: {theme['card_bg']};
        padding: 25px;
        border-radius: 15px;
        border: 2px solid {theme['border']};
        margin: 20px 0;
    ">
        <h3 style="color: {theme['text']}; margin-bottom: 15px;">📋 Detailed Results</h3>
    </div>
    """, unsafe_allow_html=True)
    
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
    
    # Download options with enhanced styling
    st.markdown(f"""
    <div style="
        background: {theme['card_bg']};
        padding: 25px;
        border-radius: 15px;
        border: 2px solid {theme['border']};
        margin: 20px 0;
    ">
        <h3 style="color: {theme['text']}; margin-bottom: 15px;">💾 Download Results</h3>
    </div>
    """, unsafe_allow_html=True)
    
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
    """Display quick statistics in the sidebar with enhanced styling"""
    theme = get_current_theme()
    
    if not results:
        st.info("No results to display")
        return
    
    total = len(results)
    positive = len([r for r in results if r['sentiment_label'] == 'Positive'])
    negative = len([r for r in results if r['sentiment_label'] == 'Negative'])
    neutral = len([r for r in results if r['sentiment_label'] == 'Neutral'])
    
    # Enhanced metrics display
    st.markdown(f"""
    <div style="
        background: {theme['card_bg']};
        padding: 15px;
        border-radius: 10px;
        border: 2px solid {theme['border']};
        margin: 10px 0;
        text-align: center;
    ">
        <h4 style="color: {theme['text']}; margin: 0;">📊 Statistics</h4>
    </div>
    """, unsafe_allow_html=True)
    
    st.metric("Total", total)
    st.metric("Positive", positive)
    st.metric("Negative", negative)
    st.metric("Neutral", neutral)
    
    # Language distribution with enhanced styling
    languages = {}
    for result in results:
        lang = result['detected_language']
        languages[lang] = languages.get(lang, 0) + 1
    
    st.markdown(f"""
    <div style="
        background: {theme['card_bg']};
        padding: 15px;
        border-radius: 10px;
        border: 2px solid {theme['border']};
        margin: 10px 0;
    ">
        <h4 style="color: {theme['text']}; margin-bottom: 10px;">🌍 Languages</h4>
    </div>
    """, unsafe_allow_html=True)
    
    for lang, count in languages.items():
        st.markdown(f"""
        <div style="
            background: {theme['secondary']};
            padding: 8px 12px;
            border-radius: 8px;
            margin: 5px 0;
            border-left: 4px solid {theme['text']};
        ">
            <span style="color: {theme['text']}; font-weight: bold;">{lang.upper()}:</span>
            <span style="color: {theme['text']}; float: right;">{count}</span>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
