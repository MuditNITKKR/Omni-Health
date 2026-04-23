import streamlit as st
from src.ml_engine import predict_heart_risk

st.set_page_config(page_title="Omni Health | Heart Prediction", layout="wide")

st.title("📊 Cardiovascular Risk Assessment (UCI Model)")
st.write("Please provide clinical metrics to calculate cardiac risk.")

with st.form("heart_form"):
    col1, col2, col3 = st.columns(3)
    
    with col1:
        age = st.number_input("Age", min_value=1, max_value=120, value=50)
        sex = st.selectbox("Gender", ["Male", "Female"])
        cp = st.selectbox("Chest Pain Type", [0, 1, 2, 3], help="0: Typical, 1: Atypical, 2: Non-anginal, 3: Asymptomatic")
        trestbps = st.number_input("Resting Blood Pressure (mm Hg)", value=130)

    with col2:
        chol = st.number_input("Serum Cholesterol (mg/dl)", value=240)
        fbs = st.number_input("Fasting Blood Sugar (mg/dl)", value=100)
        restecg = st.selectbox("Resting ECG Results", [0, 1, 2])
        thalach = st.number_input("Max Heart Rate Achieved", value=150)

    with col3:
        exang = st.selectbox("Exercise Induced Angina", ["No", "Yes"])
        oldpeak = st.number_input("ST Depression (Oldpeak)", value=1.0, step=0.1)
        slope = st.selectbox("Slope of Peak Exercise ST Segment", [0, 1, 2])

    submitted = st.form_submit_button("Run Diagnostic Prediction")

if submitted:
    # Package data for the engine
    user_input = {
        "age": age, "sex": sex, "cp": cp, "trestbps": trestbps,
        "chol": chol, "fbs": fbs, "restecg": restecg, "thalach": thalach,
        "exang": exang, "oldpeak": oldpeak, "slope": slope
    }

    result, prob = predict_heart_risk(user_input)

    if result is not None:
        st.divider()
        risk_label = "HIGH RISK" if result == 1 else "LOW RISK"
        color = "red" if result == 1 else "green"
        
        st.markdown(f"### Result: <span style='color:{color}'>{risk_label}</span>", unsafe_allow_html=True)
        st.write(f"Confidence Level: **{prob*100:.1f}%**")