import streamlit as st
from PIL import Image
import cv2
from src.dl_engine import DL_Suite

st.set_page_config(page_title="Omni Health | Detection", layout="wide")

@st.cache_resource
def get_suite():
    return DL_Suite()

suite = get_suite()

st.title("📷 Neural Imaging Suite")

# --- SELECTOR ---
with st.sidebar:
    st.header("Diagnostic Settings")
    mode = st.radio("Select Target:", ["Fracture Detection", "Chest Disease (NIH)"])
    st.divider()
    threshold = st.slider("Detection Threshold", 0.1, 1.0, 0.25)

uploaded_file = st.file_uploader("Upload X-ray Image", type=["jpg", "png", "jpeg"])

if uploaded_file:
    input_img = Image.open(uploaded_file)
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Input Scan")
        st.image(input_img, use_container_width=True)

    with col2:
        st.subheader("AI Interpretation")
        with st.spinner("Processing..."):
            if mode == "Fracture Detection":
                processed_img, findings = suite.detect_fracture(input_img, threshold)
            else:
                processed_img, findings = suite.analyze_chest(input_img, threshold)

            # Display Result (Ensure RGB)
            if mode == "Fracture Detection":
                st.image(cv2.cvtColor(processed_img, cv2.COLOR_BGR2RGB), use_container_width=True)
            else:
                st.image(input_img, use_container_width=True)

    # --- SHARED RESULTS TABLE ---
    if findings:
        st.divider()
        st.success(f"Detected {len(findings)} condition(s)")
        st.table(findings)
    else:
        st.info("No pathologies detected at this threshold.")