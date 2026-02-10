# Web Frontend Configuration

## API Configuration
- **Backend URL**: http://127.0.0.1:8000
- **API Key**: Heart_disease_api

## Setup Instructions

1. **Start the Backend Server**:
   ```bash
   cd backend
   uvicorn main:app --reload --host 127.0.0.1 --port 8000
   ```

2. **Open the Frontend**:
   - Simply open `index.html` in your web browser
   - Or use a local server:
     ```bash
     cd web_frontend
     python -m http.server 3000
     ```
   - Then visit: http://localhost:3000

## Features
- Modern responsive design
- Real-time form validation
- Loading animations
- Error handling
- Beautiful result visualization
- Mobile-friendly interface

## Troubleshooting
- Ensure the backend server is running on port 8000
- Check browser console for any JavaScript errors
- Verify API key matches between frontend and backend