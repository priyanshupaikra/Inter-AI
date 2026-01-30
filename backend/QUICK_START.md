# 🎯 QUICK START GUIDE - AI Interview Backend

## ⚡ Run These Commands (In Order)

### 1. Navigate to backend directory
```bash
cd "d:/AI Interview/backend"
```

### 2. Activate virtual environment
```bash
source venv/Scripts/activate
```
✅ You should see `(venv)` in your prompt

### 3. Run the verification script
```bash
python verify_backend.py
```

This will check:
- ✅ Database connection (PostgreSQL Neon)
- ✅ All installed packages
- ✅ Django models
- ✅ Speech recognition
- ✅ PDF generation
- ⚠️ Gemini API (shows warning if not configured)
- ⚠️ OpenAI API (optional)

---

## 🤖 To Enable Gemini AI (Optional but Recommended)

### Step 1: Get Gemini API Key
Visit: https://makersuite.google.com/app/apikey

Click "Get API Key" or "Create API Key"

### Step 2: Add to .env file
Open: `d:\AI Interview\backend\.env`

Add your key:
```env
GEMINI_API_KEY=your_api_key_here
```

### Step 3: Install Gemini library
```bash
pip install google-generativeai
```

### Step 4: Test again
```bash
python verify_backend.py
```

Now you should see: ✅ Gemini API: WORKING

---

## 🚀 Start the Server

```bash
python manage.py runserver
```

Server will start at: http://localhost:8000

---

## 🔍 Access Points

### 1. API Root
http://localhost:8000/api/

**Available endpoints:**
- `/api/interviewers/` - Manage interviewers
- `/api/students/` - Manage students
- `/api/sessions/` - Interview sessions
- `/api/questions/` - Interview questions
- `/api/conversations/` - AI-student conversations
- `/api/ai-interview/` - AI interview conductor
- `/api/reports/` - PDF report generation

### 2. Admin Panel
http://localhost:8000/admin/

**Login with:**
- Username: `admin`
- Password: `admin123`

### 3. Sample Data
Already loaded in database:
- 2 Interviewers
- 4 Students
- 3 Interview Sessions
- 14 Questions

---

## 📊 Database Info

**Type:** PostgreSQL (Neon Cloud)

**Connection Details:**
- Host: ep-young-queen-a1pyg8k4-pooler.ap-southeast-1.aws.neon.tech
- Database: neondb
- User: neondb_owner
- SSL: Required

✅ Already configured in `.env` file

---

## 🎬 Test the System

### Quick API Test (using curl or browser):

1. **Get all sessions:**
```bash
curl http://localhost:8000/api/sessions/
```

2. **Get all students:**
```bash
curl http://localhost:8000/api/students/
```

3. **Get all questions:**
```bash
curl http://localhost:8000/api/questions/
```

---

## 📚 Documentation Files

1. **BACKEND_SUMMARY.md** - Complete backend overview
2. **VERIFICATION_CHECKLIST.md** - Step-by-step verification
3. **GEMINI_SETUP.md** - Detailed Gemini setup guide
4. **FRONTEND_INTEGRATION.md** - How to connect frontend
5. **README.md** - Full documentation

---

## ❓ Troubleshooting

### "Module not found" error
```bash
# Make sure venv is activated
source venv/Scripts/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### "Database connection failed"
Check that your `.env` file has correct database credentials

### "Port already in use"
```bash
# Try a different port
python manage.py runserver 8080
```

---

## ✅ What's Working Right Now

- ✅ **Database**: PostgreSQL on Neon (connected)
- ✅ **Models**: All 6 models created
- ✅ **API**: All REST endpoints functional
- ✅ **Admin**: Full admin panel access
- ✅ **Speech Recognition**: Voice-to-text ready
- ✅ **PDF Generation**: Report generation ready
- ⚠️ **AI Interviewer**: Uses Mock AI (add Gemini key for real AI)

---

## 🎯 Next Steps

1. ✅ Run `python verify_backend.py` to check all connections
2. ⚠️ Add Gemini API key (optional but recommended)
3. ✅ Start server with `python manage.py runserver`
4. ✅ Test API endpoints in browser or Postman
5. ✅ Connect your frontend application

---

## 💡 Current AI Status

**Without Gemini API Key:**
- System uses **Mock AI Interviewer**
- Questions are asked in sequence
- No natural AI conversation
- Perfect for testing backend/frontend integration

**With Gemini API Key:**
- System uses **Real AI Interviewer**  
- Natural conversational responses
- Context-aware follow-up questions
- Professional interview experience
- **FREE tier**: 15 requests per minute

---

## 🔗 Important Links

- Get Gemini API: https://makersuite.google.com/app/apikey
- Neon Database: https://neon.tech
- Django Docs: https://docs.djangoproject.com
- DRF Docs: https://www.django-rest-framework.org

---

**Your backend is ready to use! 🚀**

For detailed verification, see: `VERIFICATION_CHECKLIST.md`
