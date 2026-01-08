"""
Streamlit frontend for XLNet Indonesian Sarcasm Detection
Provides a clean and modern UI for the sarcasm detection API
Calls FastAPI backend instead of loading model directly
"""

import streamlit as st
import requests
from typing import Optional

# Page configuration
st.set_page_config(
    page_title="Sarcasm Detector 🎭",
    page_icon="🎭",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for modern styling
st.markdown("""
    <style>
        * {
            margin: 0;
            padding: 0;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        
        .main {
            max-width: 900px;
            margin: 0 auto;
            padding: 2rem;
        }
        
        .header-container {
            text-align: center;
            margin-bottom: 3rem;
        }
        
        .header-title {
            font-size: 3rem;
            font-weight: 800;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 0.5rem;
        }
        
        .header-subtitle {
            font-size: 1.1rem;
            color: #666;
            font-weight: 400;
        }
        
        .input-section {
            background: white;
            padding: 2rem;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
            margin-bottom: 2rem;
        }
        
        .input-label {
            font-size: 1.1rem;
            font-weight: 600;
            color: #333;
            margin-bottom: 0.8rem;
            display: block;
        }
        
        .stTextArea textarea {
            font-size: 15px !important;
            border-radius: 8px !important;
            border: 2px solid #e0e0e0 !important;
            padding: 12px !important;
            font-family: 'Segoe UI', sans-serif !important;
        }
        
        .stTextArea textarea:focus {
            border-color: #667eea !important;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
        }
        
        .button-container {
            display: flex;
            gap: 1rem;
            margin-top: 1.5rem;
        }
        
        .result-box-sarcasm {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 2rem;
            border-radius: 12px;
            margin-bottom: 2rem;
            box-shadow: 0 8px 24px rgba(102, 126, 234, 0.3);
        }
        
        .result-box-non-sarcasm {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
            padding: 2rem;
            border-radius: 12px;
            margin-bottom: 2rem;
            box-shadow: 0 8px 24px rgba(245, 87, 108, 0.3);
        }
        
        .result-label {
            font-size: 1.5rem;
            font-weight: 700;
            margin-bottom: 1rem;
        }
        
        .confidence-text {
            font-size: 1.3rem;
            font-weight: 600;
            margin: 1rem 0;
        }
        
        .confidence-bar {
            width: 100%;
            height: 8px;
            background: rgba(255, 255, 255, 0.3);
            border-radius: 4px;
            overflow: hidden;
            margin: 1rem 0;
        }
        
        .confidence-fill {
            height: 100%;
            background: rgba(255, 255, 255, 0.8);
            border-radius: 4px;
        }
        
        .analyzed-text-box {
            background: #f8f9fa;
            padding: 1.5rem;
            border-left: 4px solid #667eea;
            border-radius: 8px;
            margin: 2rem 0;
            font-style: italic;
            color: #555;
        }
        
        .divider {
            margin: 2rem 0;
            border: none;
            height: 1px;
            background: linear-gradient(to right, transparent, #ddd, transparent);
        }
        
        .footer-text {
            text-align: center;
            color: #999;
            font-size: 0.9rem;
            margin-top: 3rem;
        }
        
        .stButton button {
            font-weight: 600;
            padding: 0.75rem 1.5rem !important;
            border-radius: 8px !important;
            font-size: 1rem !important;
        }
        
        .primary-btn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
            color: white !important;
            border: none !important;
            padding: 0.8rem 2rem !important;
            font-size: 1.05rem !important;
            font-weight: 700 !important;
            border-radius: 8px !important;
            cursor: pointer;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3) !important;
            transition: all 0.3s ease !important;
        }
        
        .primary-btn:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4) !important;
        }
        
        .secondary-btn {
            background: #f0f0f0 !important;
            color: #333 !important;
            border: 2px solid #e0e0e0 !important;
            padding: 0.7rem 1.2rem !important;
            font-size: 0.95rem !important;
            font-weight: 600 !important;
            border-radius: 8px !important;
            cursor: pointer;
            transition: all 0.3s ease !important;
        }
        
        .secondary-btn:hover {
            background: #e8e8e8 !important;
            border-color: #d0d0d0 !important;
        }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
    <div class="header-container">
        <div class="header-title">🎭 Sarcasm Detector</div>
        <div class="header-subtitle">Detect sarcasm in Indonesian text using AI</div>
    </div>
""", unsafe_allow_html=True)

# Configuration
API_URL = "http://localhost:7860"

# Try to connect to API at startup
@st.cache_resource
def check_api_connection():
    """Check if API is available"""
    try:
        response = requests.get(f"{API_URL}/health", timeout=2)
        return response.status_code == 200
    except:
        return False

# Sidebar
with st.sidebar:
    st.markdown("### ℹ️ About")
    st.markdown(
        """
        This application uses a fine-tuned **XLNet** model trained on Indonesian text to detect sarcasm.
        
        **How it works:**
        1. Enter Indonesian text
        2. Click "Predict"
        3. Get sarcasm detection result
        
        **Model:** XLNet (Fine-tuned)
        **Framework:** Hugging Face
        """
    )
    st.markdown("---")
    st.markdown("**API Status:** " + ("✅ Connected" if check_api_connection() else "❌ Not Connected"))

# Main input section
st.markdown("""
    <div class="input-section">
        <label class="input-label">✍️ Enter Your Text</label>
        <p style="font-size: 13px; color: #999; margin-bottom: 1rem;">Type Indonesian text to analyze for sarcasm (max 1000 characters)</p>
    </div>
""", unsafe_allow_html=True)

# Text input area
user_text = st.text_area(
    label="Input text",
    placeholder="Contoh: Ya, tentu saja, saya sangat senang dengan cuaca hujan hari ini!",
    height=120,
    label_visibility="collapsed"
)

# Button section
st.markdown("<br>", unsafe_allow_html=True)
col1, col2, col3 = st.columns([1, 1, 2])

with col1:
    predict_button = st.button(
        "🚀 Predict",
        key="predict_btn",
        use_container_width=True,
        type="primary"
    )

with col2:
    clear_button = st.button(
        "🗑️ Clear",
        key="clear_btn",
        use_container_width=True
    )

# Prediction logic
if predict_button:
    # Check input
    if not user_text.strip():
        st.error("❌ Please enter some text to analyze!")
    
    elif len(user_text) > 1000:
        st.error("❌ Text is too long! Maximum 1000 characters allowed.")
    
    else:
        # Check API connection first
        if not check_api_connection():
            st.error(
                "❌ Cannot connect to API server. "
                "Please make sure the FastAPI backend is running on http://localhost:7860"
            )
        else:
            # Show loading indicator
            with st.spinner("🔍 Analyzing text..."):
                try:
                    # Call the API
                    response = requests.post(
                        f"{API_URL}/predict",
                        json={"text": user_text},
                        timeout=30
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        
                        # Store result in session state for display
                        st.session_state.prediction = result["prediction"]
                        st.session_state.confidence = result["confidence"]
                        st.session_state.input_text = user_text
                        
                    else:
                        st.error(f"❌ API Error: {response.status_code}")
                        
                except requests.exceptions.ConnectionError:
                    st.error(
                        "❌ Cannot reach the API server. "
                        "Please ensure the FastAPI backend is running on http://localhost:7860"
                    )
                except requests.exceptions.Timeout:
                    st.error("❌ Request timeout. Please try again.")
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")

if clear_button:
    st.session_state.clear()
    st.rerun()

# Display results if available
if hasattr(st.session_state, 'prediction'):
    st.markdown("<hr class='divider'>", unsafe_allow_html=True)
    st.markdown("### 📊 Result")
    
    prediction = st.session_state.prediction
    confidence = st.session_state.confidence
    confidence_percent = confidence * 100
    
    # Result box styling based on prediction
    if prediction == "Sarcasm":
        result_html = f"""
        <div class='result-box-sarcasm'>
            <div class='result-label'>🎭 Sarcasm Detected</div>
            <div class='confidence-text'>Confidence: {confidence_percent:.1f}%</div>
            <div class='confidence-bar'>
                <div class='confidence-fill' style='width: {confidence_percent}%;'></div>
            </div>
            <div style='font-size: 14px; margin-top: 1rem; opacity: 0.95;'>The text is likely sarcastic.</div>
        </div>
        """
    else:
        result_html = f"""
        <div class='result-box-non-sarcasm'>
            <div class='result-label'>✅ Non-Sarcasm</div>
            <div class='confidence-text'>Confidence: {confidence_percent:.1f}%</div>
            <div class='confidence-bar'>
                <div class='confidence-fill' style='width: {confidence_percent}%;'></div>
            </div>
            <div style='font-size: 14px; margin-top: 1rem; opacity: 0.95;'>The text is likely not sarcastic.</div>
        </div>
        """
    
    st.markdown(result_html, unsafe_allow_html=True)
    
    # Show analyzed text
    st.markdown("### 📝 Analyzed Text")
    st.markdown(f'<div class="analyzed-text-box">{st.session_state.input_text}</div>', unsafe_allow_html=True)
    
    # Try again button
    if st.button("🔄 Analyze Another Text", use_container_width=True):
        st.session_state.clear()
        st.rerun()

# Footer
st.markdown("<hr class='divider'>", unsafe_allow_html=True)
st.markdown(
    "<div class='footer-text'>Built with Streamlit & FastAPI | XLNet Indonesian Sarcasm Detection</div>",
    unsafe_allow_html=True
)
