import streamlit as st
import requests
import os
from dotenv import load_dotenv
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

# Load environment variables
load_dotenv()

# ----------------------------------
# Configuration
# ----------------------------------
API_URL = os.getenv("API_URL", "http://127.0.0.1:8000/predict")
API_KEY = os.getenv("API_KEY")

if not API_KEY:
    st.error("API_KEY not found in environment variables")
    st.stop()

# ----------------------------------
# Custom CSS Styling
# ----------------------------------
def load_css():
    st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
    
    /* Main App Styling - Dark Theme */
    .main {
        padding: 0rem 1rem;
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        color: #e0e0e0;
    }
    
    .stApp {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    }
    
    /* Custom Header */
    .header-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    }
    
    .header-title {
        color: #ffffff;
        font-family: 'Poppins', sans-serif;
        font-size: 3rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .header-subtitle {
        color: rgba(255,255,255,0.9);
        font-family: 'Poppins', sans-serif;
        font-size: 1.2rem;
        font-weight: 300;
        margin: 0.5rem 0 0 0;
    }
    
    /* Form Container */
    .form-container {
        background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 5px 20px rgba(0,0,0,0.3);
        margin-bottom: 2rem;
        color: #ecf0f1;
    }
    
    /* Input Groups */
    .input-group {
        background: linear-gradient(135deg, #34495e 0%, #2c3e50 100%);
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        border-left: 4px solid #667eea;
        color: #ecf0f1;
    }
    
    .input-group-title {
        color: #ecf0f1;
        font-family: 'Poppins', sans-serif;
        font-size: 1.1rem;
        font-weight: 600;
        margin-bottom: 1rem;
    }
    
    /* Results Container */
    .result-container {
        padding: 2rem;
        border-radius: 15px;
        margin: 1rem 0;
        text-align: center;
        box-shadow: 0 5px 20px rgba(0,0,0,0.3);
    }
    
    .result-high {
        background: linear-gradient(135deg, #e74c3c, #c0392b);
        color: #ffffff;
    }
    
    .result-moderate {
        background: linear-gradient(135deg, #f39c12, #e67e22);
        color: #ffffff;
    }
    
    .result-low {
        background: linear-gradient(135deg, #27ae60, #2ecc71);
        color: #ffffff;
    }
    
    .result-title {
        font-family: 'Poppins', sans-serif;
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    .result-subtitle {
        font-family: 'Poppins', sans-serif;
        font-size: 1.2rem;
        font-weight: 400;
        opacity: 0.9;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: #ffffff;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 25px;
        font-family: 'Poppins', sans-serif;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
    }
    
    /* Sidebar */
    .css-1d391kg {
        background: linear-gradient(180deg, #2c3e50 0%, #34495e 100%);
    }
    
    /* Info boxes */
    .info-box {
        background: linear-gradient(135deg, #34495e 0%, #2c3e50 100%);
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #3498db;
        margin: 1rem 0;
        color: #ecf0f1;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Custom metric cards */
    .metric-card {
        background: linear-gradient(135deg, #34495e 0%, #2c3e50 100%);
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.3);
        text-align: center;
        margin: 0.5rem;
        color: #ecf0f1;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #667eea;
        font-family: 'Poppins', sans-serif;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #bdc3c7;
        font-family: 'Poppins', sans-serif;
    }
    
    /* Streamlit specific dark theme overrides */
    .stSelectbox > div > div {
        background-color: #34495e;
        color: #ecf0f1;
    }
    
    .stNumberInput > div > div > input {
        background-color: #34495e;
        color: #ecf0f1;
        border: 1px solid #667eea;
    }
    
    .stTextInput > div > div > input {
        background-color: #34495e;
        color: #ecf0f1;
        border: 1px solid #667eea;
    }
    
    /* Form styling */
    .stForm {
        background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
        border-radius: 15px;
        padding: 2rem;
        border: none;
    }
    
    /* Dataframe styling */
    .stDataFrame {
        background-color: #34495e;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background-color: #34495e;
        color: #ecf0f1;
    }
    
    .streamlit-expanderContent {
        background-color: #2c3e50;
        color: #ecf0f1;
    }
    </style>
    """, unsafe_allow_html=True)

# ----------------------------------
# Helper Functions
# ----------------------------------
def create_gauge_chart(probability, risk_level):
    """Create a beautiful gauge chart for risk probability"""
    
    # Determine color based on risk level
    if risk_level == "High":
        color = "#ff6b6b"
    elif risk_level == "Moderate":
        color = "#feca57"
    else:
        color = "#48dbfb"
    
    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = probability * 100,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Risk Probability (%)", 'font': {'size': 20, 'family': 'Poppins'}},
        delta = {'reference': 50},
        gauge = {
            'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': color},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 30], 'color': '#e8f5e8'},
                {'range': [30, 60], 'color': '#fff3cd'},
                {'range': [60, 100], 'color': '#f8d7da'}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 90
            }
        }
    ))
    
    fig.update_layout(
        paper_bgcolor="rgba(26,26,46,0.8)",
        plot_bgcolor="rgba(26,26,46,0.8)",
        font={'color': "#ecf0f1", 'family': "Poppins"},
        height=300
    )
    
    return fig

def create_risk_bar_chart(probability):
    """Create a risk level bar chart"""
    categories = ['Low Risk', 'Moderate Risk', 'High Risk']
    values = [max(0, 30-probability*100), max(0, min(30, probability*100-30)), max(0, probability*100-60)]
    colors = ['#48dbfb', '#feca57', '#ff6b6b']
    
    fig = px.bar(
        x=categories, 
        y=values, 
        color=categories,
        color_discrete_map={
            'Low Risk': '#48dbfb',
            'Moderate Risk': '#feca57', 
            'High Risk': '#ff6b6b'
        },
        title="Risk Level Distribution"
    )
    
    fig.update_layout(
        paper_bgcolor="rgba(26,26,46,0.8)",
        plot_bgcolor="rgba(26,26,46,0.8)",
        font={'family': "Poppins", 'color': "#ecf0f1"},
        showlegend=False,
        height=300
    )
    
    return fig

def display_sample_data():
    """Display sample data for quick testing"""
    st.markdown("### 📋 Quick Test Samples")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("👨 High Risk Sample", key="high_risk"):
            return {
                'age': 65, 'sex': 1, 'cp': 3, 'trestbps': 160, 'chol': 280,
                'fbs': 1, 'restecg': 2, 'thalach': 120, 'exang': 1,
                'oldpeak': 3.5, 'slope': 2, 'ca': 2, 'thal': 3
            }
    
    with col2:
        if st.button("👩 Moderate Risk Sample", key="mod_risk"):
            return {
                'age': 45, 'sex': 0, 'cp': 2, 'trestbps': 140, 'chol': 220,
                'fbs': 0, 'restecg': 1, 'thalach': 150, 'exang': 0,
                'oldpeak': 1.5, 'slope': 1, 'ca': 1, 'thal': 2
            }
    
    with col3:
        if st.button("👶 Low Risk Sample", key="low_risk"):
            return {
                'age': 25, 'sex': 0, 'cp': 0, 'trestbps': 110, 'chol': 180,
                'fbs': 0, 'restecg': 0, 'thalach': 180, 'exang': 0,
                'oldpeak': 0.0, 'slope': 0, 'ca': 0, 'thal': 1
            }
    
    return None

# ----------------------------------
# Main App
# ----------------------------------
def main():
    # Load custom CSS
    load_css()
    
    # Page configuration
    st.set_page_config(
        page_title="Heart Disease Prediction",
        page_icon="❤️",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Header
    st.markdown("""
    <div class="header-container">
        <h1 class="header-title">❤️ Heart Disease Prediction</h1>
        <p class="header-subtitle">Advanced AI-powered cardiovascular risk assessment</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown("### 🏥 About This App")
        st.markdown("""
        <div class="info-box">
        This application uses advanced machine learning to predict heart disease risk based on medical parameters.
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 📊 How It Works")
        st.markdown("""
        1. **Input** your medical data
        2. **AI Analysis** using XGBoost model
        3. **Get Results** with risk assessment
        4. **Consult** with healthcare professionals
        """)
        
        st.markdown("### ⚠️ Medical Disclaimer")
        st.warning("This tool is for educational purposes only. Always consult healthcare professionals for medical decisions.")
    
    # Main content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Sample data section
        sample_data = display_sample_data()
        
        st.markdown("### 📝 Patient Information")
        
        # Form
        with st.form("heart_form", clear_on_submit=False):
            # Personal Information
            st.markdown('<div class="input-group">', unsafe_allow_html=True)
            st.markdown('<div class="input-group-title">👤 Personal Information</div>', unsafe_allow_html=True)
            
            pcol1, pcol2 = st.columns(2)
            with pcol1:
                age = st.number_input("Age (years)", min_value=1, max_value=150, value=sample_data['age'] if sample_data else 45, help="Patient's age in years")
            with pcol2:
                sex = st.selectbox("Sex", [0, 1], format_func=lambda x: "👩 Female" if x == 0 else "👨 Male", index=sample_data['sex'] if sample_data else 0)
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Symptoms
            st.markdown('<div class="input-group">', unsafe_allow_html=True)
            st.markdown('<div class="input-group-title">🩺 Symptoms & Conditions</div>', unsafe_allow_html=True)
            
            scol1, scol2 = st.columns(2)
            with scol1:
                cp = st.selectbox("Chest Pain Type", [0, 1, 2, 3], 
                                format_func=lambda x: ["No Pain", "Typical Angina", "Atypical Angina", "Non-Anginal"][x],
                                index=sample_data['cp'] if sample_data else 0,
                                help="Type of chest pain experienced")
                fbs = st.selectbox("Fasting Blood Sugar > 120 mg/dl", [0, 1], 
                                 format_func=lambda x: "❌ No" if x == 0 else "✅ Yes",
                                 index=sample_data['fbs'] if sample_data else 0)
            with scol2:
                exang = st.selectbox("Exercise Induced Angina", [0, 1], 
                                   format_func=lambda x: "❌ No" if x == 0 else "✅ Yes",
                                   index=sample_data['exang'] if sample_data else 0,
                                   help="Chest pain induced by exercise")
                restecg = st.selectbox("Resting ECG", [0, 1, 2], 
                                     format_func=lambda x: ["Normal", "ST-T Abnormality", "LV Hypertrophy"][x],
                                     index=sample_data['restecg'] if sample_data else 0)
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Vital Signs
            st.markdown('<div class="input-group">', unsafe_allow_html=True)
            st.markdown('<div class="input-group-title">💓 Vital Signs</div>', unsafe_allow_html=True)
            
            vcol1, vcol2 = st.columns(2)
            with vcol1:
                trestbps = st.number_input("Resting Blood Pressure (mmHg)", min_value=50, max_value=300, 
                                         value=sample_data['trestbps'] if sample_data else 120,
                                         help="Blood pressure at rest")
                thalach = st.number_input("Max Heart Rate", min_value=60, max_value=250, 
                                        value=sample_data['thalach'] if sample_data else 150,
                                        help="Maximum heart rate achieved")
            with vcol2:
                chol = st.number_input("Serum Cholesterol (mg/dl)", min_value=100, max_value=600, 
                                     value=sample_data['chol'] if sample_data else 200,
                                     help="Cholesterol level in blood")
                oldpeak = st.number_input("ST Depression", min_value=0.0, max_value=10.0, 
                                        value=sample_data['oldpeak'] if sample_data else 1.0, step=0.1,
                                        help="ST depression induced by exercise")
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Advanced Parameters
            st.markdown('<div class="input-group">', unsafe_allow_html=True)
            st.markdown('<div class="input-group-title">🔬 Advanced Parameters</div>', unsafe_allow_html=True)
            
            acol1, acol2, acol3 = st.columns(3)
            with acol1:
                slope = st.selectbox("ST Slope", [0, 1, 2], 
                                   format_func=lambda x: ["Upsloping", "Flat", "Downsloping"][x],
                                   index=sample_data['slope'] if sample_data else 0,
                                   help="Slope of peak exercise ST segment")
            with acol2:
                ca = st.selectbox("Major Vessels", [0, 1, 2, 3], 
                                format_func=lambda x: f"{x} vessels",
                                index=sample_data['ca'] if sample_data else 0,
                                help="Number of major vessels colored by fluoroscopy")
            with acol3:
                thal = st.selectbox("Thalassemia", [1, 2, 3], 
                                  format_func=lambda x: ["Normal", "Fixed Defect", "Reversible Defect"][x-1],
                                  index=sample_data['thal']-1 if sample_data else 0,
                                  help="Thalassemia blood disorder")
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Submit button
            st.markdown("<br>", unsafe_allow_html=True)
            submit = st.form_submit_button("🔍 Analyze Heart Disease Risk", use_container_width=True)
    
    with col2:
        st.markdown("### 📈 Risk Factors")
        
        # Display risk factor information
        risk_factors = [
            ("Age", "Higher risk after 45 (women) or 55 (men)"),
            ("Cholesterol", "High levels increase risk"),
            ("Blood Pressure", "Hypertension is a major risk factor"),
            ("Exercise", "Regular activity reduces risk"),
            ("Chest Pain", "May indicate heart problems")
        ]
        
        for factor, description in risk_factors:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">{factor}</div>
                <div style="font-size: 0.8rem; color: #666; margin-top: 0.5rem;">{description}</div>
            </div>
            """, unsafe_allow_html=True)
    
    # Process form submission
    if submit:
        payload = {
            "age": age, "sex": sex, "cp": cp, "trestbps": trestbps, "chol": chol,
            "fbs": fbs, "restecg": restecg, "thalach": thalach, "exang": exang,
            "oldpeak": oldpeak, "slope": slope, "ca": ca, "thal": thal
        }
        
        headers = {
            "api-key": API_KEY,
            "Content-Type": "application/json"
        }
        
        try:
            with st.spinner("🔄 Analyzing your data with AI..."):
                response = requests.post(API_URL, json=payload, headers=headers, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                risk_level = result["risk_level"]
                probability = result["risk_probability"]
                
                # Results section
                st.markdown("---")
                st.markdown("## 📊 Analysis Results")
                
                # Main result display
                result_class = f"result-{risk_level.lower()}"
                st.markdown(f"""
                <div class="result-container {result_class}">
                    <div class="result-title">{risk_level} Risk</div>
                    <div class="result-subtitle">Probability: {probability * 100:.1f}%</div>
                </div>
                """, unsafe_allow_html=True)
                
                # Charts
                col1, col2 = st.columns(2)
                
                with col1:
                    st.plotly_chart(create_gauge_chart(probability, risk_level), use_container_width=True)
                
                with col2:
                    st.plotly_chart(create_risk_bar_chart(probability), use_container_width=True)
                
                # Recommendations
                st.markdown("### 💡 Recommendations")
                
                if risk_level == "High":
                    st.error("""
                    **Immediate Action Required:**
                    - Consult a cardiologist immediately
                    - Consider lifestyle changes
                    - Regular monitoring required
                    - Follow prescribed medications
                    """)
                elif risk_level == "Moderate":
                    st.warning("""
                    **Preventive Measures Recommended:**
                    - Regular check-ups with your doctor
                    - Maintain healthy diet and exercise
                    - Monitor blood pressure and cholesterol
                    - Reduce stress and avoid smoking
                    """)
                else:
                    st.success("""
                    **Maintain Healthy Lifestyle:**
                    - Continue current healthy habits
                    - Regular exercise and balanced diet
                    - Annual health check-ups
                    - Stay informed about heart health
                    """)
                
                # Data summary
                with st.expander("📋 View Submitted Data"):
                    df = pd.DataFrame([payload])
                    st.dataframe(df, use_container_width=True)
            
            else:
                st.error(f"❌ Backend Error: {response.text}")
                
        except requests.exceptions.ConnectionError:
            st.error("❌ Connection Error: Unable to connect to the backend server. Please ensure the backend is running.")
        except requests.exceptions.Timeout:
            st.error("❌ Timeout Error: The request took too long. Please try again.")
        except requests.exceptions.RequestException as e:
            st.error(f"❌ Request Error: {str(e)}")
        except Exception as e:
            st.error(f"❌ Unexpected Error: {str(e)}")

if __name__ == "__main__":
    main()