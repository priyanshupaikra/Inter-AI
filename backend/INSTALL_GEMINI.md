# 🚀 Quick Installation & Testing Guide

## Step 1: Install the New Google GenAI Package

```bash
# Make sure venv is activated
source venv/Scripts/activate

# Uninstall old package (if installed)
pip uninstall google-generativeai -y

# Install new package
pip install google-genai
```

## Step 2: Test Your Gemini API Key

```bash
python verify_backend.py
```

### Expected Output:
You should see:
- ✅ GEMINI_API_KEY: Set
- ✅ Gemini API: WORKING
- ✅ Test Response: "Hello" (or similar)

## Step 3: Start the Server

```bash
python manage.py runserver
```

## Step 4: Test AI Interview

### Using API (Postman/curl):

1. **Create a session** (if you don't have one)
2. **Initialize AI Interview:**
   ```json
   POST http://localhost:8000/api/ai-interview/
   {
     "action": "initialize",
     "session_id": "your-session-uuid"
   }
   ```

### Expected Response:
```json
{
  "success": true,
  "opening_message": "Hello! Welcome to...",
  "first_question": "Tell me about yourself..."
}
```

## Troubleshooting

### Error: "Module 'google.generativeai' has no attribute 'Client'"
**Solution:** You need to install the new package:
```bash
pip uninstall google-generativeai -y
pip install google-genai
```

### Error: "404 models/gemini-1.5-flash not found"
**Solution:** Updated to use `gemini-2.0-flash-exp` model (already done)

### Error: "GEMINI_API_KEY not set"
**Solution:** Check your `.env` file has:
```env
GEMINI_API_KEY=AIzaSy...your_key_here
```

## What Changed?

1. ✅ **Updated Package**: `google-generativeai` → `google-genai`
2. ✅ **Updated Model**: `gemini-1.5-flash` → `gemini-2.0-flash-exp`
3. ✅ **New API Client**: Using `genai.Client()` instead of `genai.GenerativeModel()`
4. ✅ **Message Format**: Using new `types.Content` and `types.Part` structure

## Current Setup

- **Primary AI**: Google Gemini (google-genai 0.3.0)
- **Fallback**: Mock AI (no API required)
- **Model**: gemini-2.0-flash-exp (Latest, free tier)

---

**Your backend is ready to use real AI! 🤖**
