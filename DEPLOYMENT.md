# Vercel Deployment Guide

## Issues Fixed

### 1. Git Submodule Error
- **Problem**: The `model` folder was a git repository causing submodule conflicts
- **Solution**: Removed the `.git` folder from the model directory and committed it as regular files

### 2. FastAPI Entrypoint Error
- **Problem**: Vercel couldn't find the FastAPI app in expected locations
- **Solution**: Created `api/index.py` with the FastAPI application and proper model loading

## Deployment Steps

1. **Push to GitHub**: Make sure all changes are committed and pushed to your GitHub repository

2. **Deploy to Vercel**:
   - Go to [vercel.com](https://vercel.com)
   - Import your GitHub repository
   - Vercel will automatically detect the configuration from `vercel.json`

3. **Environment Variables**: In Vercel dashboard, add these environment variables:
   - `MONGO_URI`: Your MongoDB connection string
   - `API_KEY`: Your API key (Heart_disease_api.)

## File Structure for Vercel

```
├── api/
│   ├── index.py          # FastAPI app (Vercel serverless function)
│   └── heart_model.pkl   # ML model file
├── web_frontend/         # Static frontend files
│   ├── index.html
│   ├── css/
│   └── js/
├── vercel.json          # Vercel configuration
├── requirements.txt     # Python dependencies
└── .env                 # Environment variables (for local development)
```

## API Endpoints

- **Frontend**: `https://your-app.vercel.app/`
- **API**: `https://your-app.vercel.app/api/predict`
- **API Docs**: `https://your-app.vercel.app/api/docs`

## Testing Locally

1. Install Vercel CLI: `npm i -g vercel`
2. Run: `vercel dev`
3. Access: `http://localhost:3000`

## Notes

- The frontend automatically detects the deployment URL
- Model file is included in the `api/` directory for serverless deployment
- CORS is configured to allow all origins (adjust for production)