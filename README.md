# 🏥 Heart Disease Prediction System

A complete **production-ready** machine learning application for predicting heart disease risk using XGBoost classifier. Features a modern web frontend deployed on Vercel, FastAPI backend deployed on Railway, and MongoDB Atlas for data storage.

## 🎯 What This Project Does

This application predicts the risk of heart disease based on 13 medical parameters using a trained XGBoost machine learning model. Users can input their health data through a beautiful web interface and receive instant risk assessments (Low/Moderate/High) with probability scores.

## 🚀 Live Demo

- **Frontend**: [Deployed on Vercel](https://heart-disease-prediction-three.vercel.app/)
- **Backend API**: [Deployed on Railway](https://heart-disease-prediction-production-7bb8.up.railway.app)
- **Database**: MongoDB Atlas (Cloud)

## 🏗️ Architecture Overview

```
┌─────────────────┐    HTTP Requests    ┌─────────────────┐    Database Queries    ┌─────────────────┐
│   Web Frontend  │ ──────────────────► │   FastAPI Backend│ ────────────────────► │  MongoDB Atlas   │
│   (Vercel)      │                     │   (Railway)      │                        │  (Cloud)         │
│                 │ ◄────────────────── │                  │ ◄──────────────────── │                 │
│ HTML/CSS/JS     │    JSON Response     │ XGBoost Model    │   Prediction Results   │ Predictions &    │
│                 │                     │                  │                        │ API Keys         │
└─────────────────┘                     └─────────────────┘                        └─────────────────┘
```

### Components:

1. **Frontend (Vercel)**: Modern responsive web interface
2. **Backend (Railway)**: FastAPI server with ML model
3. **Database (MongoDB Atlas)**: Cloud database for predictions
4. **Model**: XGBoost classifier trained on heart disease dataset

## 📊 Features

### 🤖 Machine Learning
- **XGBoost Classifier**: High-performance gradient boosting algorithm
- **13 Medical Features**: Age, sex, chest pain type, blood pressure, cholesterol, etc.
- **Risk Assessment**: Low/Moderate/High risk levels with probability scores
- **Real-time Prediction**: Instant results with beautiful visualization

### 🔒 Security & Validation
- **API Key Authentication**: Secure backend access
- **Input Validation**: Medical data range validation
- **CORS Enabled**: Cross-origin requests allowed
- **Environment Variables**: Secure configuration management

### 🎨 User Experience
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Loading Animations**: Smooth user feedback
- **Error Handling**: User-friendly error messages
- **Form Validation**: Real-time input validation
- **Result Visualization**: Color-coded risk levels with progress bars

### ☁️ Cloud Deployment
- **Vercel Frontend**: Global CDN, automatic HTTPS, instant deployments
- **Railway Backend**: Serverless deployment, auto-scaling, built-in monitoring
- **MongoDB Atlas**: Cloud database with automatic backups

## 📁 Project Structure

```
Heart_Disease_prediction/
├── backend/                    # Railway deployment (FastAPI)
│   ├── main.py                # FastAPI application
│   ├── heart_model.pkl        # Trained XGBoost model
│   ├── requirements.txt       # Python dependencies
│   ├── Procfile              # Railway deployment config
│   └── .env                  # Environment variables
├── web_frontend/              # Vercel deployment (Static)
│   ├── index.html            # Main HTML page
│   ├── css/
│   │   └── style.css         # Styling
│   ├── js/
│   │   └── script.js         # Frontend logic & API calls
│   └── assets/               # Images and icons
├── model/                     # ML model development
│   ├── preprocessing_training.py  # Model training script
│   └── README.md             # Model documentation
├── dataset/                   # Training data
│   └── cleaned_heart.csv     # Heart disease dataset
├── .env                       # Root environment variables
├── .gitignore                # Git ignore rules
└── README.md                 # This file
```

## 🛠️ Technologies Used

### Backend
- **FastAPI**: Modern Python web framework
- **XGBoost**: Machine learning algorithm
- **MongoDB**: NoSQL database
- **Pydantic**: Data validation
- **Uvicorn**: ASGI server

### Frontend
- **HTML5**: Semantic markup
- **CSS3**: Modern styling with animations
- **JavaScript (ES6+)**: Interactive functionality
- **Fetch API**: HTTP requests

### Deployment & Cloud
- **Railway**: Backend deployment platform
- **Vercel**: Frontend deployment platform
- **MongoDB Atlas**: Cloud database
- **GitHub**: Version control

### Development
- **Python 3.9+**: Programming language
- **scikit-learn**: ML utilities
- **pandas**: Data manipulation
- **numpy**: Numerical computing

## 🚀 Deployment Guide

### Backend (Railway)
1. **Connect Repository**: Link GitHub repo to Railway
2. **Set Root Directory**: `backend`
3. **Environment Variables**:
   - `MONGO_URI`: Your MongoDB Atlas connection string
   - `API_KEY`: `Heart_disease_api`
4. **Deploy**: Railway auto-deploys on git push

### Frontend (Vercel)
1. **Connect Repository**: Link GitHub repo to Vercel
2. **Set Root Directory**: `web_frontend`
3. **Framework Preset**: Other (static files)
4. **Deploy**: Vercel auto-deploys on git push

### Database (MongoDB Atlas)
1. **Create Cluster**: Free tier available
2. **Create Database**: `heart_disease_db`
3. **Create Collections**:
   - `api_keys`: Store API authentication
   - `predictions`: Store prediction results

## 📡 API Documentation

### Base URL
```
https://heart-disease-prediction-production-7bb8.up.railway.app
```

### Endpoints

#### GET `/`
Health check endpoint.
```bash
curl https://heart-disease-prediction-production-7bb8.up.railway.app/
```
**Response:**
```json
{
  "message": "Heart Disease Prediction API",
  "status": "running"
}
```

#### POST `/api/predict`
Predict heart disease risk.
```bash
curl -X POST https://heart-disease-prediction-production-7bb8.up.railway.app/api/predict \
  -H "Content-Type: application/json" \
  -H "api-key: Heart_disease_api" \
  -d '{
    "age": 55,
    "sex": 1,
    "cp": 2,
    "trestbps": 130,
    "chol": 250,
    "fbs": 0,
    "restecg": 1,
    "thalach": 150,
    "exang": 0,
    "oldpeak": 1.5,
    "slope": 1,
    "ca": 0,
    "thal": 2
  }'
```
**Response:**
```json
{
  "risk_probability": 0.87,
  "risk_level": "High"
}
```

### Request Parameters
| Parameter | Type | Range | Description |
|-----------|------|-------|-------------|
| `age` | int | 1-150 | Age in years |
| `sex` | int | 0-1 | Sex (0=Female, 1=Male) |
| `cp` | int | 0-3 | Chest pain type |
| `trestbps` | int | 50-300 | Resting blood pressure |
| `chol` | int | 100-600 | Serum cholesterol |
| `fbs` | int | 0-1 | Fasting blood sugar >120mg/dl |
| `restecg` | int | 0-2 | Resting ECG results |
| `thalach` | int | 60-250 | Maximum heart rate |
| `exang` | int | 0-1 | Exercise induced angina |
| `oldpeak` | float | 0.0-10.0 | ST depression |
| `slope` | int | 0-2 | Peak exercise ST slope |
| `ca` | int | 0-3 | Major vessels colored |
| `thal` | int | 1-3 | Thalassemia |

## 🏠 Local Development

### Prerequisites
- Python 3.9+
- MongoDB Atlas account
- Git

### Setup Steps

1. **Clone Repository**
```bash
git clone https://github.com/your-username/Heart-Disease-Prediction.git
cd Heart-Disease-Prediction
```

2. **Install Dependencies**
```bash
pip install -r backend/requirements.txt
```

3. **Environment Configuration**
```bash
# Copy and configure environment variables
cp .env backend/.env
# Edit backend/.env with your MongoDB URI
```

4. **Start Backend**
```bash
cd backend
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

5. **Start Frontend**
```bash
cd web_frontend
python -m http.server 3000
```
Visit: http://localhost:3000

## 📈 Model Performance

- **Algorithm**: XGBoost Classifier
- **Training Data**: Cleveland Heart Disease Dataset
- **Features**: 13 medical parameters
- **Accuracy**: ~85-90% (based on training)
- **Output**: Risk probability (0.0-1.0) + Risk level

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- **Dataset**: Cleveland Heart Disease Dataset (UCI Machine Learning Repository)
- **Libraries**: XGBoost, FastAPI, scikit-learn, and many others
- **Platforms**: Vercel, Railway, MongoDB Atlas for hosting

## 📞 Support

If you encounter any issues:
1. Check the deployment logs on Railway/Vercel
2. Verify environment variables are set correctly
3. Ensure MongoDB Atlas connection is working
4. Check browser console for frontend errors

---

**Built with ❤️ for healthcare and machine learning education**