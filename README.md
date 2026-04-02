# HeartCare AI - Heart Disease Prediction System

## 🚀 Overview

A full-stack, enterprise-grade clinical application that utilizes Machine Learning (XGBoost) to assess the risk of heart disease based on patient health data. The project features a beautifully designed frontend and a robust FastAPI backend, enhanced with **SHAP (SHapley Additive exPlanations)** for transparent model explainability and automated PDF report generation.

## 📁 Project Structure

- `backend/`: FastAPI server handling ML inference, SHAP explanations, PDF generation, and MongoDB integration.
- `web_frontend/`: A modern, responsive clinical UI with advanced CSS animations to interact with the API.
- `model/`: Machine Learning training pipeline (data preprocessing & XGBoost training).
- `dataset/`: Directory to hold the datasets (like `heart.csv`) used to train the machine learning model.

## ✨ Key Features

- **Accurate Predictions**: Uses a tuned XGBoost classifier to provide a high-accuracy risk assessment.
- **Explainable AI (XAI)**: Integrates SHAP values to explain which clinical factors contributed most to the prediction.
- **Clinical Frontend Interface**: Fully redesigned with a modern, professional clinical UI, featuring a pure CSS-based medical heart visualization, responsive layouts, and glassmorphism styling.
- **Automated PDF Reports**: Generates professional clinical reports with patient data, risk assessment, and key risk factors.
- **Secure API**: Backend protected via API key authentication.
- **Data Persistence**: Optional MongoDB integration to seamlessly record predictions.

## 🛠️ Tech Stack

- **Frontend**: HTML5, Vanilla JavaScript, CSS3 (Custom animations, Grid, Flexbox)
- **Backend Framework**: Python, FastAPI, Uvicorn, Pydantic
- **Machine Learning**: Scikit-Learn, XGBoost, SHAP, Pandas, NumPy, Joblib
- **Database**: MongoDB (via PyMongo)
- **PDF Generation**: ReportLab

## ⚙️ Getting Started

### Prerequisites

- Python 3.8+
- (Optional) MongoDB instance for database persistence.

### 1. Backend Setup

1. Navigate to the `backend` directory:
   ```bash
   cd backend
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Configure environment variables:
   Create a `.env` file in the `backend` directory. Example:
   ```env
   MONGO_URI=your_mongodb_connection_string
   API_KEY=Heart_disease_api
   ```
4. Start the backend server:
   ```bash
   uvicorn main:app --reload --host 127.0.0.1 --port 8000
   ```
   *(Windows Alternative: Simply double-click on `start_backend.bat`)*

### 2. Frontend Setup

1. Ensure the FastAPI backend server is running and accessible on port `8000`.
2. The frontend requires no build steps. You can either:
   - Double-click `index.html` inside the `web_frontend` directory.
   - Start a simple local server:
     ```bash
     cd web_frontend
     python -m http.server 3000
     ```
     Then navigate his browser to `http://localhost:3000/`.

### 3. Training the Model (Optional)

If you wish to retrain the machine learning model with updated data:
1. Switch to the `model` directory:
   ```bash
   cd model
   ```
2. Run the training script:
   ```bash
   python preprocessing_training.py
   ```
   *Note: This script will load data from `../dataset/heart.csv`, evaluate the XGBoost model, and overwrite the `heart_model.pkl` in the `backend` directory.*

## 📡 API Endpoints

The API includes endpoints meant to streamline predictions and usability:
- **`POST /api/predict`**: Accepts patient clinical parameters and securely returns risk probability, risk level, and full SHAP explanations. (Requires the `api-key` header).
- **`POST /api/report`**: Generates and returns a downloadable PDF clinical report containing predicted risks and visualizations.
- **`GET /health`**: Health check endpoints to monitor background service health.

## 🎨 UI / UX Enhancements

The frontend highlights state-of-the-art modern clinical aesthetics representing the **HeartCare AI** brand:
- **Professional Medical Palette**: Clean, trustworthy medical styling throughout.
- **CSS-Based Visualizations**: Continuous pulsing ECG and heart icons strictly using modern CSS.
- **Highly Responsive Design**: Easily usable across mobile phones, tablets, and desktop displays.
