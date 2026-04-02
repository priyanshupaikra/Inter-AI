"""
Quick Gemini API Test
Run this to verify your API key is working
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

print("=" * 60)
print("  GEMINI API QUICK TEST")
print("=" * 60)
print()

# Check API key
api_key = os.getenv('GEMINI_API_KEY')
if not api_key:
    print("❌ GEMINI_API_KEY not found in .env file")
    print("Add your API key to .env file:")
    print("   GEMINI_API_KEY=your_key_here")
    exit(1)

print(f"✅ API Key found: {api_key[:8]}...{api_key[-4:]}")
print()

# Try to import library
try:
    from google import genai
    from google.genai import types
    print("✅ google-genai library installed")
except ImportError as e:
    print("❌ google-genai library not installed")
    print("Install with: pip install google-genai")
    print(f"Error: {e}")
    exit(1)

print()
print("Testing Gemini API connection...")
print("-" * 60)

try:
    # Create client
    client = genai.Client(api_key=api_key)
    
    # Test with a simple message
    response = client.models.generate_content(
        model='gemini-flash-latest',
        contents=types.Content(
            role='user',
            parts=[types.Part(text="Say 'Hello! Gemini is working!' in exactly those words.")]
        )
    )
    
    print(f"✅ Gemini API Response:")
    print(f"   {response.text}")
    print()
    print("=" * 60)
    print("🎉 SUCCESS! Your Gemini API is working perfectly!")
    print("=" * 60)
    print()
    print("Next steps:")
    print("  1. Run: python manage.py runserver")
    print("  2. Test AI interview endpoints")
    print()
    
except Exception as e:
    print(f"❌ Gemini API Error: {str(e)}")
    print()
    print("Troubleshooting:")
    print("  1. Check your API key is correct")
    print("  2. Make sure you have internet connection")
    print("  3. Verify your API key has Gemini API enabled")
    print("  4. Get a new key from: https://makersuite.google.com/app/apikey")
    print()
    exit(1)
