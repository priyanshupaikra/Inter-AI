# Inter AI - AI-Powered Interview Platform

An intelligent interview platform that uses Google's Gemini AI to conduct technical interviews, provide real-time questions, and generate comprehensive PDF reports.

## 🎯 Features

- **AI-Powered Interviews**: Gemini LLM conducts adaptive technical interviews
- **Voice & Text Input**: Support for both typed and spoken responses
- **Real-time Interaction**: Dynamic question-answer flow based on candidate responses
- **Interview Reports**: Automated PDF generation with detailed analysis
- **Modern UI**: Responsive React frontend with premium design
- **Full Backend**: Django REST API with PostgreSQL database

## 🏗️ Architecture

```
┌─────────────────┐         ┌──────────────────┐         ┌─────────────────┐
│  React Frontend │ ◄─────► │  Django Backend  │ ◄─────► │  PostgreSQL DB  │
│   (Port 5173)   │  REST   │   (Port 8000)    │         │                 │
└─────────────────┘  API    └──────────────────┘         └─────────────────┘
                                     │
                                     ▼
                            ┌─────────────────┐
                            │  Google Gemini  │
                            │   AI (LLM)      │
                            └─────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Node.js 16+
- PostgreSQL database
- Google AI API key ([Get one here](https://makersuite.google.com/app/apikey))

### 1. Clone the Repository

```bash
git clone <repository-url>
cd AI\ Interview
```

### 2. Backend Setup

```bash
# Navigate to backend
cd backend

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
# Create a .env file with:
# GOOGLE_AI_API_KEY=your_api_key_here
# DB_NAME=your_db_name
# DB_USER=your_db_user
# DB_PASSWORD=your_db_password
# DB_HOST=your_db_host

# Run migrations
python manage.py migrate

# Start the server
python manage.py runserver
```

Backend will be available at `http://localhost:8000`

### 3. Frontend Setup

```bash
# Open a new terminal
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend will be available at `http://localhost:5173`

### 4. Access the Application

Open your browser and navigate to:
- **Application**: `http://localhost:5173`
- **Backend API**: `http://localhost:8000/api/`
- **Admin Panel**: `http://localhost:8000/admin/`

## 📖 Documentation

- **[Getting Started Guide](GETTING_STARTED.md)** - Detailed setup instructions
- **[Integration Summary](INTEGRATION_SUMMARY.md)** - Frontend-backend connection details
- **[Backend Summary](backend/BACKEND_SUMMARY.md)** - Backend architecture and API docs
- **[Frontend README](frontend/README.md)** - Frontend component documentation

## 🧪 Testing the Connection

### Option 1: Use the Application
1. Start both backend and frontend servers
2. Visit `http://localhost:5173`
3. Fill in the setup form
4. Start an interview

### Option 2: Automated Test
Open `frontend/test-connection.html` in your browser to run automated API connectivity tests.

### Option 3: Manual API Test
```bash
# Test creating a student
curl -X POST http://localhost:8000/api/students/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Test User", "email": "test@example.com"}'
```

## 📁 Project Structure

```
Inter-AI/
├── backend/                    # Django backend
│   ├── backend/               # Project settings
│   ├── interviews/            # Main app (models, views, APIs)
│   ├── manage.py
│   ├── requirements.txt
│   └── README.md
│
├── frontend/                   # React frontend
│   ├── src/
│   │   ├── components/        # UI components
│   │   ├── pages/             # Page components
│   │   ├── services/          # API integration
│   │   └── App.jsx
│   ├── package.json
│   └── README.md
│
├── GETTING_STARTED.md         # Quick start guide
├── INTEGRATION_SUMMARY.md     # Integration details
└── README.md                  # This file
```

## 🔧 Technology Stack

### Backend
- **Framework**: Django 5.2
- **API**: Django REST Framework
- **Database**: PostgreSQL
- **AI**: Google Generative AI (Gemini)
- **PDF Generation**: ReportLab
- **CORS**: django-cors-headers

### Frontend
- **Framework**: React 19
- **Build Tool**: Vite
- **UI Components**: Radix UI
- **Icons**: Lucide React
- **Styling**: CSS3 with custom variables
- **HTTP Client**: Fetch API

## 🌟 Key Features Explained

### 1. AI Interview Flow
```
User Setup → Create Session → AI Generates Question → 
User Responds → AI Analyzes → Next Question → ... → 
End Interview → Generate Report
```

### 2. Voice Input
- Uses MediaRecorder API for audio capture
- Backend transcribes audio using Google AI
- Automatically fills response field

### 3. Responsive Design
- Desktop: 3-column grid layout
- Tablet: 2-column layout
- Mobile: Single column, optimized controls

### 4. Real-time Updates
- Dynamic question display
- Live conversation history
- Processing indicators

## 🔒 Security Features

- CSRF protection enabled
- CORS configured for development
- Secure database connections (SSL)
- Environment variables for sensitive data
- Input validation on both frontend and backend

## 📊 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/students/` | POST | Create student profile |
| `/api/interviewers/` | POST | Create interviewer profile |
| `/api/sessions/` | POST/GET | Manage interview sessions |
| `/api/sessions/{id}/start/` | POST | Start a session |
| `/api/sessions/{id}/end/` | POST | End a session |
| `/api/questions/` | POST/GET | Manage questions |
| `/api/ai-interview/` | POST | AI interview operations |
| `/api/conversations/` | POST/GET | Store conversations |
| `/api/reports/generate/` | POST | Generate PDF reports |

Full API documentation: `backend/FRONTEND_INTEGRATION.md`

## 🐛 Troubleshooting

### Backend Issues

**Database connection error:**
```bash
# Check your .env file has correct credentials
# Ensure PostgreSQL is running
```

**Module not found:**
```bash
pip install -r requirements.txt
```

**AI not responding:**
```bash
# Verify GOOGLE_AI_API_KEY in .env
# Check backend console for error messages
```

### Frontend Issues

**Cannot connect to backend:**
- Ensure backend is running on port 8000
- Check CORS settings in `backend/settings.py`

**Voice recording not working:**
- Allow microphone permissions in browser
- Use Chrome/Edge for best compatibility
- Requires HTTPS in production (localhost ok in dev)

## 🚢 Deployment

### Frontend (Production)
```bash
cd frontend
npm run build
# Deploy dist/ folder to Vercel, Netlify, etc.
```

### Backend (Production)
```bash
# Set DEBUG=False in settings
# Configure production database
# Collect static files
python manage.py collectstatic
# Use Gunicorn + Nginx
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is part of the Inter AI platform.

## 👥 Support

For issues, questions, or contributions:
- Check documentation in `docs/` folder
- Review `GETTING_STARTED.md` for setup help
- Use `test-connection.html` for debugging connectivity

---

**Made with ❤️ using Django, React, and Google Gemini AI**
