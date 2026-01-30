# ✅ Backend Verification Checklist

Complete this checklist to verify your AI Interview backend is properly configured.

---

## 🔧 Prerequisites

### 1. Virtual Environment
```bash
# Activate virtual environment
cd backend
source venv/Scripts/activate

# You should see (venv) in your terminal prompt
```

**Status**: ⬜ Virtual environment activated

---

## 📦 Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

**Required packages**:
- ⬜ Django 5.2.6
- ⬜ djangorestframework
- ⬜ django-cors-headers
- ⬜ psycopg2-binary (PostgreSQL)
- ⬜ reportlab (PDF generation)
- ⬜ SpeechRecognition (Voice-to-text)
- ⬜ python-dotenv (Environment variables)

**Optional packages**:
- ⬜ google-generativeai (for Gemini AI)
- ⬜ openai (for OpenAI GPT)

### Verification Command:
```bash
pip list | grep -E "Django|rest|cors|psycopg2|reportlab|Speech"
```

---

## 🗄️ Step 2: Database Configuration

### Check `.env` file exists:
```bash
ls -la .env
```

### Expected content in `.env`:
```env
DB_NAME=neondb
DB_USER=neondb_owner
DB_PASSWORD=npg_vN4OLwn9ldWB
DB_HOST=ep-young-queen-a1pyg8k4-pooler.ap-southeast-1.aws.neon.tech
DB_PORT=5432
```

**Checklist**:
- ⬜ `.env` file exists
- ⬜ DB_NAME is set
- ⬜ DB_USER is set
- ⬜ DB_PASSWORD is set
- ⬜ DB_HOST is set (Neon endpoint)
- ⬜ DB_PORT is set (5432)

### Test Database Connection:
```bash
python manage.py dbshell
# If it connects, type \q to exit
```

**Status**: ⬜ Database connection successful

---

## 🔄 Step 3: Migrations

### Create migrations:
```bash
python manage.py makemigrations
```

**Expected output**:
```
No changes detected
```
(Migrations already created)

### Run migrations:
```bash
python manage.py migrate
```

**Expected tables**:
- ⬜ interviews_interviewer
- ⬜ interviews_student
- ⬜ interviews_interviewsession
- ⬜ interviews_question
- ⬜ interviews_conversation
- ⬜ interviews_interviewreport

### Verify migrations:
```bash
python manage.py showmigrations interviews
```

All should have [X] marks.

**Status**: ⬜ All migrations applied

---

## 👤 Step 4: Create Admin User

```bash
python manage.py createsuperuser
```

### Default credentials:
- Username: `admin`
- Email: `admin@example.com`
- Password: `admin123` (or your choice)

**Status**: ⬜ Admin user created

---

## 🌱 Step 5: Seed Sample Data (Optional)

```bash
python manage.py seed_database
```

**Expected output**:
- ✅ Created admin user
- ✅ Created 2 interviewers
- ✅ Created 4 students
- ✅ Created 3 interview sessions
- ✅ Created 14 questions

**Status**: ⬜ Database seeded

---

## 🤖 Step 6: AI Configuration

### A. Gemini API (Recommended)

1. Get API key: https://makersuite.google.com/app/apikey
2. Add to `.env`:
   ```env
   GEMINI_API_KEY=your_key_here
   ```
3. Install library:
   ```bash
   pip install google-generativeai
   ```

**Status**: ⬜ Gemini configured

### B. OpenAI API (Alternative)

1. Get API key: https://platform.openai.com/api-keys
2. Add to `.env`:
   ```env
   OPENAI_API_KEY=your_key_here
   ```
3. Install library:
   ```bash
   pip install openai
   ```

**Status**: ⬜ OpenAI configured (optional)

### C. Test AI (Python):
```python
# Test Gemini
python -c "import google.generativeai as genai; print('Gemini OK')"

# Test OpenAI
python -c "from openai import OpenAI; print('OpenAI OK')"
```

---

## 🗣️ Step 7: Speech Recognition

### Install system dependencies (if needed):

**Windows**: No additional setup needed

**Linux**:
```bash
sudo apt-get install portaudio19-dev python3-pyaudio
```

**Mac**:
```bash
brew install portaudio
```

### Test Speech Recognition:
```python
python -c "import speech_recognition as sr; print('Speech Recognition OK')"
```

**Status**: ⬜ Speech recognition ready

---

## 📄 Step 8: PDF Generation

### Test ReportLab:
```python
python -c "from reportlab.platypus import SimpleDocTemplate; print('PDF Generation OK')"
```

**Status**: ⬜ PDF generation ready

---

## 🚀 Step 9: Start Server

```bash
python manage.py runserver
```

### Expected output:
```
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

**Status**: ⬜ Server started successfully

---

## ✅ Step 10: Test Endpoints

### Open in browser or Postman:

1. **API Root**:
   ```
   http://localhost:8000/api/
   ```
   **Status**: ⬜ API accessible

2. **Admin Panel**:
   ```
   http://localhost:8000/admin/
   ```
   Login with admin credentials
   **Status**: ⬜ Admin panel accessible

3. **API Endpoints**:
   - ⬜ `/api/interviewers/` - Works
   - ⬜ `/api/students/` - Works
   - ⬜ `/api/sessions/` - Works
   - ⬜ `/api/questions/` - Works
   - ⬜ `/api/conversations/` - Works
   - ⬜ `/api/ai-interview/` - Works
   - ⬜ `/api/reports/` - Works

---

## 🔍 Step 11: Run Comprehensive Verification

```bash
python verify_backend.py
```

### Expected tests:
- ⬜ Environment Variables: PASSED
- ⬜ Django Configuration: PASSED
- ⬜ Database Connection: PASSED
- ⬜ Database Models: PASSED
- ⬜ Gemini API: PASSED (or WARNING if not configured)
- ⬜ OpenAI API: WARNING (optional)
- ⬜ Speech Recognition: PASSED
- ⬜ PDF Generation: PASSED

---

## 📋 Complete System Check

Run Django's system check:
```bash
python manage.py check
```

**Expected**: `System check identified no issues (0 silenced).`

**Status**: ⬜ No system issues

---

## 🎯 Final Verification Steps

### 1. Test Complete Interview Flow

```bash
# Get all sessions
curl http://localhost:8000/api/sessions/

# Get all students
curl http://localhost:8000/api/students/

# Get all interviewers
curl http://localhost:8000/api/interviewers/
```

**Status**: ⬜ All API endpoints return data

### 2. Check Media Directories

```bash
ls -la media/
ls -la media/audio_recordings/
ls -la media/interview_reports/
```

**Status**: ⬜ Media directories exist

### 3. Check Logs

Look for any errors in server output.

**Status**: ⬜ No critical errors in logs

---

## 🎉 Summary

### Core Requirements (Must Pass):
- ⬜ Virtual environment activated
- ⬜ All dependencies installed
- ⬜ Database connected (PostgreSQL Neon)
- ⬜ Migrations applied
- ⬜ Admin user created
- ⬜ Server starts successfully
- ⬜ API endpoints accessible

### Optional Features:
- ⬜ Gemini AI configured
- ⬜ Sample data seeded
- ⬜ OpenAI configured (alternative)

---

## 🐛 Troubleshooting

### Issue: Module not found
```bash
# Make sure venv is activated
source venv/Scripts/activate

# Reinstall requirements
pip install -r requirements.txt
```

### Issue: Database connection failed
```bash
# Check .env file
cat .env | grep DB_

# Test connection manually
psql 'postgresql://neondb_owner:npg_vN4OLwn9ldWB@ep-young-queen-a1pyg8k4-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require'
```

### Issue: Migrations not applying
```bash
# Reset migrations (careful!)
python manage.py migrate interviews zero
python manage.py migrate
```

### Issue: Server won't start
```bash
# Check for port conflicts
netstat -ano | findstr :8000

# Try different port
python manage.py runserver 8080
```

---

## 📚 Additional Resources

- **Main Documentation**: `README.md`
- **Frontend Integration**: `FRONTEND_INTEGRATION.md`
- **Gemini Setup**: `GEMINI_SETUP.md`
- **Backend Summary**: `BACKEND_SUMMARY.md`
- **Verification Script**: `verify_backend.py`

---

## ✅ Completion

Once all checkboxes are checked, your backend is **100% ready**!

**Date Completed**: _______________

**Notes**:
_________________________________________________________________
_________________________________________________________________
_________________________________________________________________
