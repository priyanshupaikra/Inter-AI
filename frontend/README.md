# AI Interview Frontend

A modern, responsive React frontend for the AI Interview platform, built with Radix UI components and connected to a Django backend.

## Features

- ✅ **Modern UI Design**: Premium interface with glassmorphism, gradients, and micro-animations
- ✅ **Radix UI Components**: Accessible and composable UI primitives
- ✅ **Backend Integration**: Fully connected to Django REST API
- ✅ **Voice Recording**: Speech-to-text functionality for interview responses
- ✅ **Real-time Updates**: Dynamic question/answer flow
- ✅ **Responsive Design**: Works seamlessly on desktop, tablet, and mobile
- ✅ **Interview Flow**: Complete workflow from setup to completion with PDF report generation

## Tech Stack

- **React 19** - UI framework
- **Vite** - Build tool and dev server
- **Radix UI** - Headless UI components
- **Lucide React** - Icon library
- **CSS3** - Custom styling with CSS variables

## Getting Started

### Prerequisites

1. Backend server running on `http://localhost:8000`
2. Node.js 16+ installed

### Installation

```bash
# Install dependencies
npm install

# Start development server
npm run dev
```

The app will be available at `http://localhost:5173`

## Project Structure

```
src/
├── components/          # Reusable UI components
│   ├── Header.jsx      # Top navigation bar
│   ├── HardwareCheck.jsx  # Camera/mic status
│   ├── WelcomeCard.jsx    # Interview info card
│   ├── AgentCard.jsx      # AI interviewer profile
│   ├── SessionView.jsx    # Live interview view
│   └── Controls.jsx       # End interview controls
├── pages/              # Page-level components
│   ├── Setup.jsx       # Pre-interview setup form
│   └── Interview.jsx   # Main interview interface
├── services/           # API integration
│   ├── config.js       # API configuration
│   └── api.js          # API service functions
├── App.jsx             # Main app with state management
└── index.css           # Global styles and CSS variables

```

## Backend Connection

### API Configuration

The frontend connects to the backend at `http://localhost:8000/api`. To change this, edit `src/services/config.js`:

```javascript
export const API_BASE_URL = 'http://your-backend-url/api';
```

### API Endpoints Used

- **POST** `/api/students/` - Create student profile
- **POST** `/api/interviewers/` - Create interviewer profile
- **POST** `/api/sessions/` - Create interview session
- **POST** `/api/sessions/{id}/start/` - Start session
- **POST** `/api/sessions/{id}/end/` - End session
- **POST** `/api/questions/bulk_create/` - Add questions
- **POST** `/api/ai-interview/` - AI interview interactions (initialize, respond, end)
- **POST** `/api/conversations/` - Save conversations
- **POST** `/api/conversations/voice_to_text/` - Transcribe audio
- **POST** `/api/reports/generate/` - Generate PDF report

## Interview Flow

### 1. Setup Stage
- User enters name and email
- Selects interview type and duration
- System creates student, interviewer, and session

### 2. Interview Stage
- AI asks initial question
- Student responds via text or voice
- AI processes response and asks follow-up questions
- Conversation continues until session ends

### 3. Completion Stage
- Interview ends
- PDF report is generated and downloaded
- User returns to setup screen

## Features in Detail

### Voice Recording

The app supports voice input using the browser's MediaRecorder API:

```javascript
// Request microphone access with noise suppression
const stream = await navigator.mediaDevices.getUserMedia({ 
  audio: {
    echoCancellation: true,
    noiseSuppression: true,
    sampleRate: 44100,
  }
});
```

Recorded audio is sent to the backend for transcription via the `/conversations/voice_to_text/` endpoint.

### State Management

App state is managed using React's useState hook:

```javascript
const [appState, setAppState] = useState({
  stage: 'setup',    // 'setup' | 'interview' | 'completed'
  interviewData: null,
  error: null,
});
```

### Error Handling

All API calls include try-catch blocks with user-friendly error messages:

```javascript
try {
  await sendStudentResponse(sessionUUID, response);
} catch (err) {
  setError('Failed to send response. Please try again.');
}
```

## Responsive Design

The layout adapts to different screen sizes:

- **Desktop** (>1024px): 3-column grid layout
- **Tablet** (768px-1024px): 2-column grid
- **Mobile** (<768px): Single column, simplified navigation

## Browser Compatibility

- Chrome/Edge 90+
- Firefox 88+
- Safari 14+

**Note**: Voice recording requires HTTPS in production (or localhost for development).

## Building for Production

```bash
# Create optimized production build
npm run build

# Preview production build
npm run preview
```

## Troubleshooting

### Backend Connection Issues

1. **CORS errors**: Ensure Django CORS settings allow frontend origin:
   ```python
   # backend/settings.py
   CORS_ALLOWED_ORIGINS = ['http://localhost:5173']
   ```

2. **API not found**: Verify backend is running on port 8000:
   ```bash
   cd backend
   python manage.py runserver
   ```

### Voice Recording Not Working

1. Check browser permissions for microphone access
2. Ensure using HTTPS (or localhost)
3. Check browser console for MediaRecorder errors

### Questions Not Loading

1. Verify session was created successfully
2. Check browser network tab for failed API calls
3. Ensure backend database migrations are up to date

## Development Tips

### Quick Submit

Press `Ctrl+Enter` in the response textarea to quickly submit without clicking the button.

### Auto-run Mode

For testing, you can modify the interview flow to use mock data instead of real API calls.

## License

This project is part of the Inter AI interview platform.

## Support

For issues or questions, check:
- Backend documentation: `backend/README.md`
- API integration guide: `backend/FRONTEND_INTEGRATION.md`
