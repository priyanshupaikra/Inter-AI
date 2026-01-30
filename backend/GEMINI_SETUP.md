# Setting Up Google Gemini API for AI Interview

## Why Gemini?

- **Free Tier**: Generous free quota (15 requests per minute)
- **Fast**: Gemini 1.5 Flash is optimized for speed
- **Powerful**: Excellent conversational AI capabilities
- **Easy**: Simple setup process

## Step 1: Get Your Gemini API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click **"Get API Key"** or **"Create API Key"**
4. Copy your API key

## Step 2: Add API Key to Your Backend

Open `backend/.env` file and add your Gemini API key:

```env
GEMINI_API_KEY=your_api_key_here
```

## Step 3: Install Gemini Library

```bash
# Make sure virtual environment is activated
source venv/Scripts/activate

# Install the library
pip install google-generativeai
```

## Step 4: Test It!

Your backend is already configured to use Gemini automatically if the API key is set.

Start the server:
```bash
python manage.py runserver
```

## How It Works

When you initialize an AI interview, the system will:

1. **First try Gemini** (if `GEMINI_API_KEY` is set) ✅
2. Fall back to OpenAI (if `OPENAI_API_KEY` is set)
3. Use Mock Interviewer (if no API keys)

## API Pricing (as of 2026)

### Gemini 1.5 Flash (Free Tier)
- **Free**: 15 RPM (requests per minute)
- **Paid**: $0.075 per 1M input tokens, $0.30 per 1M output tokens

### Comparison: Cost per Interview
Assuming 20 messages per interview (~2000 tokens total):
- **Gemini**: ~$0.0005 per interview (practically FREE for testing!)
- **OpenAI GPT-4**: ~$0.06 per interview
- **OpenAI GPT-3.5**: ~$0.004 per interview

## Testing Without API Key

The system includes a **Mock AI Interviewer** that works without any API key. It will:
- Ask questions in sequence
- Not provide natural AI responses
- Perfect for frontend/backend integration testing

## Troubleshooting

### Error: "No module named 'google.generativeai'"
```bash
pip install google-generativeai
```

### Error: "API key is required"
Make sure your `.env` file has:
```env
GEMINI_API_KEY=your_actual_api_key
```

### Testing if it's working
Check the server logs when initializing an interview:
```
INFO - Using Gemini AI interviewer  ✅ (Working!)
INFO - Using Mock AI interviewer     ⚠️  (No API key)
```

## Using OpenAI Instead

If you prefer OpenAI, just set:
```env
OPENAI_API_KEY=your_openai_key
# Leave GEMINI_API_KEY empty
```

Get OpenAI key from: https://platform.openai.com/api-keys

## Advanced: Custom AI Configuration

You can modify `interviews/ai_views.py` to change the priority order or add more AI providers!

---

**Need help?** Check the main README.md or FRONTEND_INTEGRATION.md files.
