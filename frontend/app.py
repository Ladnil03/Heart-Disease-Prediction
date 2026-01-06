import streamlit as st
import requests

# ----------------------------------
# Backend Configuration
# ----------------------------------
API_URL = "http://127.0.0.1:8000/predict"   # MUST be HTTP
API_KEY = "Heart_disease_api"

# ----------------------------------
# Page Config
# ----------------------------------
st.set_page_config(
    page_title="Heart Disease Prediction",
    page_icon="❤️",
    layout="centered"
)

st.title("❤️ Heart Disease Prediction")
st.write("Fill the form below and predict heart disease risk.")
st.divider()

# ----------------------------------
# Form UI
# ----------------------------------
with st.form("heart_form"):
    age = st.number_input("Age", min_value=1, max_value=100, value=30)

    sex = st.selectbox(
        "Sex",
        [0, 1],
        format_func=lambda x: "Female" if x == 0 else "Male"
    )

    cp = st.selectbox("Chest Pain Type (cp)", [0, 1, 2, 3])
    trestbps = st.number_input("Resting Blood Pressure (trestbps)", min_value=1, max_value=250, value=120)
    chol = st.number_input("Serum Cholesterol (chol)", min_value=1, max_value=600, value=200)
    fbs = st.selectbox("Fasting Blood Sugar > 120 mg/dl (fbs)", [0, 1])
    restecg = st.selectbox("Resting ECG (restecg)", [0, 1, 2])
    thalach = st.number_input("Max Heart Rate (thalach)", min_value=1, max_value=250, value=150)
    exang = st.selectbox("Exercise Induced Angina (exang)", [0, 1])
    oldpeak = st.number_input("Oldpeak", min_value=0.0, max_value=10.0, value=1.0)
    slope = st.selectbox("Slope", [0, 1, 2])
    ca = st.selectbox("Major Vessels (ca)", [0, 1, 2, 3])
    thal = st.selectbox("Thal", [1, 2, 3])

    submit = st.form_submit_button("🔍 Predict")

# ----------------------------------
# Form Validation + Backend Call
# ----------------------------------
if submit:
    errors = []

    if age <= 0:
        errors.append("Age must be greater than 0")
    if trestbps <= 0:
        errors.append("Blood pressure must be greater than 0")
    if chol <= 0:
        errors.append("Cholesterol must be greater than 0")
    if thalach <= 0:
        errors.append("Heart rate must be greater than 0")

    if errors:
        st.error("Please fix the following errors:")
        for e in errors:
            st.write(f"❌ {e}")
    else:
        payload = {
            "age": age,
            "sex": sex,
            "cp": cp,
            "trestbps": trestbps,
            "chol": chol,
            "fbs": fbs,
            "restecg": restecg,
            "thalach": thalach,
            "exang": exang,
            "oldpeak": oldpeak,
            "slope": slope,
            "ca": ca,
            "thal": thal
        }

        # ✅ CORRECT HEADER (THIS WAS YOUR BUG)
        headers = {
            "api-key": API_KEY,
            "Content-Type": "application/json"
        }

        with st.spinner("Sending data to backend..."):
            response = requests.post(
                API_URL,
                json=payload,
                headers=headers
            )

        if response.status_code == 200:
            result = response.json()

            st.success("✅ Prediction Successful")

            st.subheader("📋 Submitted Data")
            st.json(payload)

            st.subheader("🧠 Prediction Result")
            risk = result["risk_level"]
            prob = result["risk_probability"]

            if risk == "High":
                st.error(f"🚨 High Risk ({prob})")
            elif risk == "Moderate":
                st.warning(f"⚠️ Moderate Risk ({prob})")
            else:
                st.success(f"💚 Low Risk ({prob})")

        else:
            st.error("❌ Backend Error")
            st.code(response.text)
