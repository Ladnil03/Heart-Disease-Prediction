# Heart Disease Prediction

A complete machine learning application for predicting heart disease risk using XGBoost classifier with FastAPI backend and Streamlit frontend.

## Features

- **Machine Learning Model**: XGBoost classifier for heart disease prediction
- **REST API**: FastAPI backend with comprehensive error handling
- **Web Interface**: Streamlit frontend for user-friendly interaction
- **Database**: MongoDB Atlas for storing predictions and API keys
- **Security**: Environment-based configuration and API key authentication
- **Validation**: Input validation with proper medical data ranges

## Project Structure

```
Heart_Disease_prediction/
├── backend/
│   ├── main.py          # FastAPI backend
│   └── .env             # Backend environment variables
├── frontend/
│   ├── app.py           # Streamlit frontend
│   └── .env             # Frontend environment variables
├── model/
│   ├── preprocessing_training.py  # Model training script
│   └── heart_model.pkl  # Trained model (generated)
├── dataset/
│   └── cleaned_heart.csv  # Dataset for training
├── requirements.txt     # Python dependencies
├── .gitignore          # Git ignore file
└── README.md           # This file
```

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Environment Configuration

The `.env` files are already configured with necessary variables:

**Backend (.env)**:
- `MONGO_URI`: MongoDB connection string
- `API_KEY`: API authentication key

**Frontend (.env)**:
- `API_KEY`: API authentication key
- `API_URL`: Backend API endpoint

### 3. Train the Model

```bash
cd model
python preprocessing_training.py
```

This will create `heart_model.pkl` in the model directory.

### 4. Run the Backend

```bash
cd backend
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

### 5. Run the Frontend

```bash
cd frontend
streamlit run app.py
```

## Usage

1. Open the Streamlit app in your browser (usually http://localhost:8501)
2. Fill in the medical parameters in the form
3. Click "🔍 Predict" to get the heart disease risk assessment
4. View the prediction results with risk level and probability

## API Endpoints

### POST /predict

Predicts heart disease risk based on input parameters.

**Headers:**
- `api-key`: Authentication key

**Request Body:**
```json
{
  "age": 63,
  "sex": 1,
  "cp": 3,
  "trestbps": 145,
  "chol": 233,
  "fbs": 1,
  "restecg": 0,
  "thalach": 150,
  "exang": 0,
  "oldpeak": 2.3,
  "slope": 0,
  "ca": 0,
  "thal": 1
}
```

**Response:**
```json
{
  "risk_probability": 0.85,
  "risk_level": "High"
}
```

## Input Parameters

- **age**: Age (1-150)
- **sex**: Sex (0=Female, 1=Male)
- **cp**: Chest pain type (0-3)
- **trestbps**: Resting blood pressure (50-300)
- **chol**: Serum cholesterol (100-600)
- **fbs**: Fasting blood sugar > 120 mg/dl (0 or 1)
- **restecg**: Resting ECG results (0-2)
- **thalach**: Maximum heart rate (60-250)
- **exang**: Exercise induced angina (0 or 1)
- **oldpeak**: ST depression (0.0-10.0)
- **slope**: Slope of peak exercise ST segment (0-2)
- **ca**: Number of major vessels (0-3)
- **thal**: Thalassemia (1-3)

## Security Features

- Environment-based configuration
- API key authentication
- Input validation with medical ranges
- Comprehensive error handling
- Resource leak prevention
- Secure database connections

## Error Handling

The application includes comprehensive error handling for:
- Network connection failures
- Database connectivity issues
- Model loading errors
- Invalid input validation
- API authentication failures

## Technologies Used

- **Backend**: FastAPI, Pydantic, PyMongo
- **Frontend**: Streamlit, Requests
- **Machine Learning**: XGBoost, Scikit-learn, Pandas, NumPy
- **Database**: MongoDB Atlas
- **Configuration**: python-dotenv