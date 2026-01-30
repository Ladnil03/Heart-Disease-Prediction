# Vercel Deployment Guide

## Issues Fixed ✅

### 1. Git Submodule Error
- **Problem**: The `model` folder was a git repository causing submodule conflicts
- **Solution**: Completely removed git submodule reference and committed model files as regular project files

### 2. FastAPI Runtime Error
- **Problem**: Invalid runtime version specification in vercel.json
- **Solution**: Updated to use `@vercel/python@4.0.0` runtime

## Deployment Steps

1. **Push to GitHub**: 
   ```bash
   git push origin main
   ```

2. **Deploy to Vercel**:
   - Go to [vercel.com](https://vercel.com)
   - Import your GitHub repository
   - Vercel will automatically detect the configuration from `vercel.json`

3. **Environment Variables**: In Vercel dashboard, add these environment variables:
   - `MONGO_URI`: `mongodb+srv://nil:6837@cluster0.5zulwui.mongodb.net/?appName=Cluster0`
   - `API_KEY`: `Heart_disease_api.`

## File Structure for Vercel

```
├── api/
│   ├── index.py          # FastAPI app (Vercel serverless function)
│   └── heart_model.pkl   # ML model file
├── web_frontend/         # Static frontend files
│   ├── index.html
│   ├── css/style.css
│   ├── js/script.js
│   └── assets/
├── vercel.json          # Vercel configuration
├── requirements.txt     # Python dependencies
└── .env                 # Environment variables (for local development)
```

## API Endpoints

- **Frontend**: `https://your-app.vercel.app/`
- **API**: `https://your-app.vercel.app/api/predict`
- **API Root**: `https://your-app.vercel.app/api/`

## Vercel Configuration

The `vercel.json` file configures:
- Python runtime: `@vercel/python@4.0.0`
- API routing: `/api/*` → `api/index.py`
- Frontend routing: `/*` → `web_frontend/*`

## Testing Locally

1. Install Vercel CLI: `npm i -g vercel`
2. Run: `vercel dev`
3. Access: `http://localhost:3000`

## Notes

- ✅ Git submodule issues completely resolved
- ✅ Proper Vercel runtime configuration
- ✅ Frontend automatically detects deployment URL
- ✅ Model file included in API directory
- ✅ CORS configured for all origins

## Troubleshooting

If you still get errors:
1. Check Vercel function logs in the dashboard
2. Ensure environment variables are set correctly
3. Verify the model file exists in `api/heart_model.pkl`