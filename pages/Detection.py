# File: D:\coding\OMNI HEALTH\pages\Detection.py
import streamlit as st
from PIL import Image
import cv2
import numpy as np
from src.dl_engine import FractureDetector # <--- Crucial Import

st.set_page_config(page_title="Omni Health | Detection", layout="wide")

# Caching the detector so it doesn't reload on every click
@st.cache_resource
def load_detector():
    # Make sure this path exactly matches your folder structure
    return FractureDetector("models/fr1.pt")

st.title("📷 Fracture Detection System")

# Initialize the detector
try:
    detector = load_detector()
except Exception as e:
    st.error(f"Failed to load model: {e}")
    st.stop()

uploaded_file = st.file_uploader("Upload Bone X-ray", type=["jpg", "jpeg", "png"])

if uploaded_file:
    img = Image.open(uploaded_file)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Original X-ray")
        st.image(img, use_container_width=True)
        
    with col2:
        st.subheader("AI Analysis")
        with st.spinner("Scanning for fractures..."):
            # Run the prediction
            annotated_img, findings = detector.predict(img)
            
            # Convert BGR (OpenCV) to RGB (Streamlit)
            result_rgb = cv2.cvtColor(annotated_img, cv2.COLOR_BGR2RGB)
            st.image(result_rgb, use_container_width=True)

    if findings:
        st.success(f"Detected {len(findings)} potential fracture(s).")
        st.table(findings)
    else:
        st.info("No fractures detected with current confidence settings.")