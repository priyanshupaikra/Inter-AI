# AI Interview Platform - Quick Start Guide

This guide will help you get the full AI Interview platform up and running with both frontend and backend connected.

## Prerequisites

- Python 3.8+ installed
- Node.js 16+ installed
- PostgreSQL database (or configured in backend/.env)
- Google AI API key (for Gemini)

## Step 1: Start the Backend

```bash
# Navigate to backend directory
cd backend

# Activate virtual environment (if not already active)
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Apply database migrations (if not done already)
python manage.py migrate

# Start the Django server
python manage.py runserver
```

The backend will be available at `http://localhost:8000`

**Verify Backend:**
- Visit `http://localhost:8000/api/` to see the API root
- Check that you see endpoints like /students/, /sessions/, etc.

## Step 2: Start the Frontend

Open a **new terminal window**:

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies (if not already installed)
npm install

# Start the development server
npm run dev
```

The frontend will be available at `http://localhost:5173`

## Step 3: Use the Application

### 3.1 Setup Interview

1. **Open** `http://localhost:5173` in your browser
2. **Fill in the form:**
   - Your full name
   - Your email address
   - Interview type (default: "Software Engineer Technical Interview")
   - Duration (15, 30, 45, or 60 minutes)
3. **Click "Start Interview"**

The system will:
- Create a student profile
- Create an AI interviewer
- Create an interview session
- Initialize the AI with your first question

### 3.2 During the Interview

**Text Response:**
1. Type your answer in the text area
2. Click "Submit Response" or press `Ctrl+Enter`
3. Wait for the AI to process and ask the next question

**Voice Response:**
1. Click "🎤 Record Answer"
2. Speak your response
3. Click "⏹ Stop Recording"
4. The audio will be transcribed to text automatically
5. Review the transcription and click "Submit Response"

### 3.3 End Interview

1. Click the red "End Interview" button
2. Confirm you want to end the interview
3. A PDF report will be generated and downloaded automatically
4. You'll be redirected to the setup screen

## Troubleshooting

### Backend Issues

**Problem:** `ModuleNotFoundError: No module named 'google.generativeai'`
```bash
cd backend
pip install google-generativeai
```

**Problem:** Database connection error
- Check your `backend/.env` file has correct database credentials
- Ensure PostgreSQL is running

**Problem:** No AI responses or empty questions
- Verify your Google AI API key is set in `backend/.env`:
  ```
  GOOGLE_AI_API_KEY=your_api_key_here
  ```

### Frontend Issues

**Problem:** "Failed to fetch" or CORS errors
- Ensure backend is running on port 8000
- Check backend CORS settings include `http://localhost:5173`
- Verify in backend/settings.py:
  ```python
  CORS_ALLOWED_ORIGINS = [
      "http://localhost:5173",
      ...
  ]
  ```

**Problem:** "Failed to start interview"
- Check browser console for detailed error messages
- Verify backend API is accessible at `http://localhost:8000/api/`
- Ensure backend database is migrated

**Problem:** Voice recording not working
- Allow microphone permissions in your browser
- Use Chrome/Edge for best compatibility
- Check browser console for MediaRecorder errors

### Network Tab Debugging

Open browser DevTools (F12) → Network tab to see API requests:

1. **Creating student** - POST to `/api/students/`
2. **Creating session** - POST to `/api/sessions/`
3. **Starting session** - POST to `/api/sessions/{id}/start/`
4. **Initializing AI** - POST to `/api/ai-interview/` with action: "initialize"
5. **Sending responses** - POST to `/api/ai-interview/` with action: "respond"

## Testing the Integration

### Quick Test

1. **Start both servers** (backend and frontend)
2. **Open frontend** at `http://localhost:5173`
3. **Enter test data:**
   - Name: "Test User"
   - Email: "test@example.com"
4. **Start interview** and verify you see the first AI question
5. **Type a simple response** like "I have 3 years of experience in Python"
6. **Submit** and verify the AI responds with a follow-up question

### Manual API Test

Use curl or Postman to test the backend directly:

```bash
# Test creating a student
curl -X POST http://localhost:8000/api/students/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Test User", "email": "test@example.com"}'

# Expected response:
# {"id": 1, "name": "Test User", "email": "test@example.com", ...}
```

## Features Overview

### ✅ Implemented Features

- User registration (student creation)
- AI interviewer initialization
- Real-time question-answer flow
- Voice-to-text transcription
- Text response submission
- Interview session management
- PDF report generation
- Responsive design (desktop, tablet, mobile)
- Error handling and user feedback

### 🚀 How It Works

```
User enters info → Creates student & session → AI generates first question
                                                          ↓
← PDF Report ← Interview ends ← AI asks more questions ← User responds
```

## Environment Variables

### Backend (.env)

```env
# Database
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=your_db_host
DB_PORT=5432

# Google AI
GOOGLE_AI_API_KEY=your_google_ai_api_key

# Django
SECRET_KEY=your_secret_key
DEBUG=True
```

### Frontend

No environment variables needed for local development. API URL is configured in `src/services/config.js`.

## Production Deployment

### Backend

1. Set `DEBUG=False` in settings
2. Configure proper SECRET_KEY
3. Set up production database
4. Collect static files: `python manage.py collectstatic`
5. Use a production server (Gunicorn + Nginx)

### Frontend

1. Update API_BASE_URL in `src/services/config.js` to production backend URL
2. Build: `npm run build`
3. Deploy `dist/` folder to static hosting (Vercel, Netlify, etc.)
4. Ensure backend CORS includes production frontend URL

## File Structure

```
ProjectRoot/
├── backend/
│   ├── backend/          # Django project settings
│   ├── interviews/       # Django app (models, views, URLs)
│   ├── manage.py
│   └── requirements.txt
│
└── frontend/
    ├── src/
    │   ├── components/   # UI components
    │   ├── pages/        # Setup & Interview pages
    │   ├── services/     # API integration
    │   └── App.jsx       # Main app with routing
    ├── package.json
    └── vite.config.js
```

## Support & Documentation

- **Backend API Docs:** `backend/FRONTEND_INTEGRATION.md`
- **Backend Summary:** `backend/BACKEND_SUMMARY.md`
- **Frontend README:** `frontend/README.md`
- **Gemini Setup:** `backend/GEMINI_SETUP.md`

## Common Commands

### Backend
```bash
python manage.py runserver           # Start dev server
python manage.py makemigrations      # Create migrations
python manage.py migrate             # Apply migrations
python manage.py createsuperuser     # Create admin user
python verify_backend.py             # Verify setup
```

### Frontend
```bash
npm run dev        # Start dev server
npm run build      # Build for production
npm run preview    # Preview production build
npm run lint       # Run ESLint
```

---

**Ready to go!** 🎉 Both frontend and backend are now fully connected and ready for AI-powered interviews.
