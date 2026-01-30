# AI Interview Backend API

A comprehensive Django REST Framework backend for conducting AI-powered interviews.

## Features

- **Interview Management**: Create and manage interview sessions with students
- **AI Interviewer**: GPT-powered AI that conducts natural interviews
- **Voice-to-Text**: Convert student audio responses to text using speech recognition
- **Real-time Conversations**: Track all interactions between AI and students
- **PDF Reports**: Automatically generate professional interview reports
- **Question Bank**: Manage interview questions with categories and difficulty levels

## Tech Stack

- **Django 5.2.6**: Web framework
- **Django REST Framework**: API framework
- **SQLite**: Database (can be switched to PostgreSQL for production)
- **OpenAI GPT**: AI interviewer
- **SpeechRecognition**: Audio transcription
- **ReportLab**: PDF generation
- **django-cors-headers**: CORS handling

## Installation

### 1. Create Virtual Environment

```bash
cd backend
python -m venv venv

# On Windows
venv\Scripts\activate

# On Mac/Linux
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Environment Variables

Create a `.env` file in the backend directory:

```env
# Optional: For production AI interviewer
OPENAI_API_KEY=your_openai_api_key_here

# Django settings
SECRET_KEY=your_secret_key_here
DEBUG=True
```

### 4. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create Superuser (Optional)

```bash
python manage.py createsuperuser
```

### 6. Run Development Server

```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000`

## API Endpoints

### Base URL: `http://localhost:8000/api/`

### 1. Interviewers

- `GET /api/interviewers/` - List all interviewers
- `POST /api/interviewers/` - Create a new interviewer
- `GET /api/interviewers/{id}/` - Get interviewer details
- `PUT /api/interviewers/{id}/` - Update interviewer
- `DELETE /api/interviewers/{id}/` - Delete interviewer

### 2. Students

- `GET /api/students/` - List all students
- `POST /api/students/` - Create a new student
- `GET /api/students/{id}/` - Get student details
- `PUT /api/students/{id}/` - Update student
- `DELETE /api/students/{id}/` - Delete student

### 3. Interview Sessions

- `GET /api/sessions/` - List all interview sessions
- `POST /api/sessions/` - Create a new interview session
- `GET /api/sessions/{id}/` - Get session details
- `PUT /api/sessions/{id}/` - Update session
- `DELETE /api/sessions/{id}/` - Delete session
- `POST /api/sessions/{id}/start/` - Start an interview session
- `POST /api/sessions/{id}/end/` - End an interview session

### 4. Questions

- `GET /api/questions/` - List all questions
- `POST /api/questions/` - Create a new question
- `POST /api/questions/bulk_create/` - Bulk create questions
- `GET /api/questions/{id}/` - Get question details
- `PUT /api/questions/{id}/` - Update question
- `DELETE /api/questions/{id}/` - Delete question

Query Parameters:
- `session_id` - Filter questions by session UUID

### 5. Conversations

- `GET /api/conversations/` - List all conversations
- `POST /api/conversations/` - Create a new conversation entry
- `POST /api/conversations/voice_to_text/` - Convert audio to text
- `GET /api/conversations/{id}/` - Get conversation details

Query Parameters:
- `session_id` - Filter conversations by session UUID

### 6. AI Interview

- `POST /api/ai-interview/` - AI interview interactions

**Actions:**

**Initialize Interview:**
```json
{
  "action": "initialize",
  "session_id": "uuid-here"
}
```

**Get AI Response:**
```json
{
  "action": "respond",
  "session_id": "uuid-here",
  "student_response": "Student's answer here"
}
```

**End Interview:**
```json
{
  "action": "end",
  "session_id": "uuid-here"
}
```

### 7. Reports

- `GET /api/reports/` - List all reports
- `POST /api/reports/generate/` - Generate a new PDF report
- `GET /api/reports/{id}/` - Get report details

**Generate Report:**
```json
{
  "session_id": "uuid-here"
}
```

## Usage Flow

### Complete Interview Workflow

1. **Create Interviewer**
```bash
curl -X POST http://localhost:8000/api/interviewers/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com"
  }'
```

2. **Create Student**
```bash
curl -X POST http://localhost:8000/api/students/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Jane Smith",
    "email": "jane@example.com"
  }'
```

3. **Create Interview Session**
```bash
curl -X POST http://localhost:8000/api/sessions/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Software Engineer Interview",
    "interviewer_id": 1,
    "student_id": 1,
    "duration_minutes": 30,
    "scheduled_at": "2026-02-01T10:00:00Z"
  }'
```

4. **Add Questions**
```bash
curl -X POST http://localhost:8000/api/questions/bulk_create/ \
  -H "Content-Type: application/json" \
  -d '{
    "questions": [
      {
        "session": 1,
        "question_text": "Tell me about yourself",
        "category": "Introduction",
        "difficulty": "easy",
        "order": 1
      },
      {
        "session": 1,
        "question_text": "What are your strengths?",
        "category": "Behavioral",
        "difficulty": "medium",
        "order": 2
      }
    ]
  }'
```

5. **Start Session**
```bash
curl -X POST http://localhost:8000/api/sessions/1/start/
```

6. **Initialize AI Interview**
```bash
curl -X POST http://localhost:8000/api/ai-interview/ \
  -H "Content-Type: application/json" \
  -d '{
    "action": "initialize",
    "session_id": "session-uuid-here"
  }'
```

7. **Student Responds (AI asks next question)**
```bash
curl -X POST http://localhost:8000/api/ai-interview/ \
  -H "Content-Type: application/json" \
  -d '{
    "action": "respond",
    "session_id": "session-uuid-here",
    "student_response": "I am a passionate software engineer..."
  }'
```

8. **End Interview**
```bash
curl -X POST http://localhost:8000/api/ai-interview/ \
  -H "Content-Type: application/json" \
  -d '{
    "action": "end",
    "session_id": "session-uuid-here"
  }'
```

9. **End Session**
```bash
curl -X POST http://localhost:8000/api/sessions/1/end/
```

10. **Generate PDF Report**
```bash
curl -X POST http://localhost:8000/api/reports/generate/ \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "session-uuid-here"
  }'
```

## Voice-to-Text Usage

```bash
curl -X POST http://localhost:8000/api/conversations/voice_to_text/ \
  -F "audio_file=@recording.wav"
```

## Database Models

### Interviewer
- `id`: Primary key
- `user`: Link to Django User (optional)
- `name`: Full name
- `email`: Email address
- `created_at`: Timestamp

### Student
- `id`: Primary key
- `name`: Full name
- `email`: Email address
- `created_at`: Timestamp

### InterviewSession
- `id`: Primary key
- `session_id`: UUID for external reference
- `interviewer`: Foreign key to Interviewer
- `student`: Foreign key to Student
- `title`: Session title
- `description`: Optional description
- `duration_minutes`: Duration in minutes
- `status`: scheduled, in_progress, completed, cancelled
- `scheduled_at`: Scheduled datetime
- `started_at`: Actual start time
- `ended_at`: Actual end time
- `created_at`, `updated_at`: Timestamps

### Question
- `id`: Primary key
- `session`: Foreign key to InterviewSession
- `question_text`: The question
- `category`: Question category
- `difficulty`: easy, medium, hard
- `order`: Display order
- `expected_answer`: Optional expected answer
- `created_at`: Timestamp

### Conversation
- `id`: Primary key
- `session`: Foreign key to InterviewSession
- `question`: Optional foreign key to Question
- `speaker`: ai or student
- `message`: The text message
- `audio_file`: Optional audio recording
- `timestamp`: When the message was sent

### InterviewReport
- `id`: Primary key
- `session`: One-to-one with InterviewSession
- `pdf_file`: Generated PDF file
- `generated_at`: Timestamp

## Admin Panel

Access the Django admin panel at `http://localhost:8000/admin/`

All models are registered and can be managed through the admin interface.

## Production Deployment

### PostgreSQL Setup

Update `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'ai_interview_db',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### Environment Variables

Set these in production:
- `SECRET_KEY`: Strong secret key
- `DEBUG=False`
- `ALLOWED_HOSTS`: Your domain
- `OPENAI_API_KEY`: Your OpenAI API key

### Collect Static Files

```bash
python manage.py collectstatic
```

## Troubleshooting

### Audio Transcription Issues

If you encounter issues with audio transcription:

1. Install PyAudio dependencies (Windows):
```bash
pip install pipwin
pipwin install pyaudio
```

2. For Linux/Mac:
```bash
# Linux
sudo apt-get install portaudio19-dev python3-pyaudio

# Mac
brew install portaudio
pip install pyaudio
```

### OpenAI API Issues

The system falls back to a mock AI interviewer if OpenAI is not available. For production:

1. Get an API key from https://platform.openai.com/
2. Set `OPENAI_API_KEY` in your environment

## License

MIT License

## Support

For issues and questions, please create an issue in the repository.
