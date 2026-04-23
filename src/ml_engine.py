import joblib
import pandas as pd
import os

def predict_heart_risk(user_data):
    model_path = "models/heart-disease_model.pkl"
    
    if not os.path.exists(model_path):
        return None, "Model file not found."

    model = joblib.load(model_path)

    # 1. Create the DataFrame with the EXACT features the model expects
    # The 'Unnamed: 0' column was present during training, so we include a dummy value
    input_df = pd.DataFrame([{
        'Unnamed: 0': 0,
        'age': user_data['age'],
        'sex': 1 if user_data['sex'] == "Male" else 0,
        'chest pain type': user_data['cp'],
        'resting bps': user_data['trestbps'],
        'cholesterol': user_data['chol'],
        'fasting blood sugar': 1 if user_data['fbs'] > 120 else 0,
        'resting ecg': user_data['restecg'],
        'max heart rate': user_data['thalach'],
        'exercise angina': 1 if user_data['exang'] == "Yes" else 0,
        'oldpeak': user_data['oldpeak'],
        'ST slope': user_data['slope']
    }])

    # 2. Predict
    prediction = model.predict(input_df)[0]
    prob = model.predict_proba(input_df)[0][1]

    return prediction, prob