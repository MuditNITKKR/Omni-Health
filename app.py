import streamlit as st

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Omni Health | AI Diagnostic Suite",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CUSTOM CSS FOR THE HOME PAGE ---
st.markdown("""
    <style>
    .main {
        background-color: #0E1117;
    }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 3em;
        background-color: #00D1FF;
        color: #000000;
        font-weight: bold;
        border: none;
    }
    .stButton>button:hover {
        background-color: #008CBA;
        color: white;
    }
    .feature-card {
        background-color: #161B22;
        padding: 25px;
        border-radius: 15px;
        border: 1px solid #30363D;
        height: 350px;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2966/2966327.png", width=80)
    st.title("Omni Health")
    st.info("System Status: Online ✅")
    st.caption("Developed for NIT Kurukshetra Project")

# --- HERO SECTION ---
st.title("🏥 Omni Health: AI-Powered Medical Suite")
st.markdown("""
    Welcome to **Omni Health**, an integrated platform combining Deep Learning, Machine Learning, and 
    Natural Language Processing to assist in medical diagnostics and risk assessment.
""")
st.divider()

# --- NAVIGATION CARDS ---
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
        <div class="feature-card">
            <h3>📷 Deep Learning</h3>
            <p>Neural imaging for fracture detection and chest pathology analysis using YOLOv11.</p>
            <br>
        </div>
    """, unsafe_allow_html=True)
    if st.button("Open Detection Suite"):
        st.switch_page("pages/Detection.py")

with col2:
    st.markdown("""
        <div class="feature-card">
            <h3>📊 Machine Learning</h3>
            <p>Predictive risk modeling for chronic diseases like Diabetes and Heart Disease.</p>
            <br>
        </div>
    """, unsafe_allow_html=True)
    if st.button("Open Risk Predictor"):
        st.switch_page("pages/Prediction.py")

with col3:
    st.markdown("""
        <div class="feature-card">
            <h3>✍️ NLP Assistant</h3>
            <p>AI-driven medical report analysis and interactive Q&A for clinical insights.</p>
            <br>
        </div>
    """, unsafe_allow_html=True)
    if st.button("Open Report Analyzer"):
        st.switch_page("pages/Reporting.py")

st.divider()

# --- PROJECT FOOTER ---
foot_col1, foot_col2 = st.columns([2,1])
with foot_col1:
    st.subheader("About the Project")
    st.write("""
        Omni Health is designed to bridge the gap between complex AI models and clinical usability. 
        By utilizing state-of-the-art datasets like VinDr-CXR, we provide a unified interface for 
        radiologists and healthcare providers.
    """)
with foot_col2:
    st.subheader("Quick Stats")
    st.text("DL Models: 2 Active")
    st.text("ML Classifiers: 3 Active")
    st.text("NLP Engine: RAG-enabled")