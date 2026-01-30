"""
Comprehensive Backend Verification Script
Tests all connections and components
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.db import connection
from django.core.exceptions import ImproperlyConfigured
from interviews.models import Interviewer, Student, InterviewSession, Question, Conversation, InterviewReport
import logging

# Color codes for terminal output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

def print_header(text):
    print(f"\n{BLUE}{'=' * 60}{RESET}")
    print(f"{BLUE}{text.center(60)}{RESET}")
    print(f"{BLUE}{'=' * 60}{RESET}\n")

def print_success(text):
    print(f"{GREEN}✅ {text}{RESET}")

def print_error(text):
    print(f"{RED}❌ {text}{RESET}")

def print_warning(text):
    print(f"{YELLOW}⚠️  {text}{RESET}")

def print_info(text):
    print(f"{BLUE}ℹ️  {text}{RESET}")

# ==================== 1. DATABASE CONNECTION ====================
def test_database_connection():
    print_header("DATABASE CONNECTION TEST")
    
    try:
        # Test basic connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT version();")
            db_version = cursor.fetchone()[0]
            print_success(f"PostgreSQL Connection: WORKING")
            print_info(f"Database Version: {db_version}")
            
        # Test database name
        db_name = connection.settings_dict['NAME']
        db_host = connection.settings_dict['HOST']
        db_user = connection.settings_dict['USER']
        
        print_info(f"Database: {db_name}")
        print_info(f"Host: {db_host}")
        print_info(f"User: {db_user}")
        
        # Test tables exist
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name LIKE 'interviews_%'
            """)
            tables = cursor.fetchall()
            
        if tables:
            print_success(f"Found {len(tables)} interview tables")
            for table in tables:
                print(f"   - {table[0]}")
        else:
            print_warning("No interview tables found. Run migrations!")
            
        return True
        
    except Exception as e:
        print_error(f"Database connection failed: {str(e)}")
        return False

# ==================== 2. MODELS TEST ====================
def test_models():
    print_header("DATABASE MODELS TEST")
    
    models_to_test = [
        ('Interviewer', Interviewer),
        ('Student', Student),
        ('InterviewSession', InterviewSession),
        ('Question', Question),
        ('Conversation', Conversation),
        ('InterviewReport', InterviewReport),
    ]
    
    all_passed = True
    
    for model_name, model_class in models_to_test:
        try:
            count = model_class.objects.count()
            print_success(f"{model_name}: {count} records")
        except Exception as e:
            print_error(f"{model_name}: Failed - {str(e)}")
            all_passed = False
    
    return all_passed

# ==================== 3. GEMINI API TEST ====================
def test_gemini_api():
    print_header("GEMINI API TEST")
    
    gemini_key = os.getenv('GEMINI_API_KEY')
    
    if not gemini_key:
        print_warning("GEMINI_API_KEY not found in environment")
        print_info("Add your Gemini API key to .env file to enable AI features")
        print_info("Get key from: https://makersuite.google.com/app/apikey")
        return False
    
    try:
        import google.generativeai as genai
        print_success("google-generativeai library installed")
        
        # Configure and test
        genai.configure(api_key=gemini_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        print_info("Testing Gemini API connection...")
        response = model.generate_content("Say 'Hello' in one word")
        
        if response and response.text:
            print_success(f"Gemini API: WORKING")
            print_info(f"Test Response: {response.text.strip()}")
            return True
        else:
            print_warning("API responded but no text returned")
            return False
            
    except ImportError:
        print_error("google-generativeai not installed")
        print_info("Install with: pip install google-generativeai")
        return False
    except Exception as e:
        print_error(f"Gemini API test failed: {str(e)}")
        return False

# ==================== 4. OPENAI API TEST ====================
def test_openai_api():
    print_header("OPENAI API TEST (Optional)")
    
    openai_key = os.getenv('OPENAI_API_KEY')
    
    if not openai_key:
        print_warning("OPENAI_API_KEY not found (This is optional)")
        return False
    
    try:
        from openai import OpenAI
        print_success("openai library installed")
        
        client = OpenAI(api_key=openai_key)
        print_info("Testing OpenAI API connection...")
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Say 'Hello' in one word"}],
            max_tokens=10
        )
        
        if response and response.choices:
            print_success("OpenAI API: WORKING")
            print_info(f"Test Response: {response.choices[0].message.content.strip()}")
            return True
        else:
            print_warning("API responded but no response returned")
            return False
            
    except ImportError:
        print_warning("openai library not installed (optional)")
        return False
    except Exception as e:
        print_error(f"OpenAI API test failed: {str(e)}")
        return False

# ==================== 5. SPEECH RECOGNITION TEST ====================
def test_speech_recognition():
    print_header("SPEECH RECOGNITION TEST")
    
    try:
        import speech_recognition as sr
        print_success("SpeechRecognition library installed")
        
        recognizer = sr.Recognizer()
        print_success("Speech Recognizer initialized")
        
        # Check for microphone (optional)
        try:
            mics = sr.Microphone.list_microphone_names()
            if mics:
                print_info(f"Found {len(mics)} microphone(s)")
        except:
            print_warning("Could not detect microphones (optional)")
        
        return True
        
    except ImportError:
        print_error("SpeechRecognition not installed")
        print_info("Install with: pip install SpeechRecognition")
        return False
    except Exception as e:
        print_error(f"Speech Recognition test failed: {str(e)}")
        return False

# ==================== 6. PDF GENERATION TEST ====================
def test_pdf_generation():
    print_header("PDF GENERATION TEST")
    
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.platypus import SimpleDocTemplate
        from io import BytesIO
        
        print_success("ReportLab library installed")
        
        # Test basic PDF creation
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        print_success("PDF generator initialized")
        
        return True
        
    except ImportError:
        print_error("ReportLab not installed")
        print_info("Install with: pip install reportlab")
        return False
    except Exception as e:
        print_error(f"PDF generation test failed: {str(e)}")
        return False

# ==================== 7. ENVIRONMENT VARIABLES ====================
def test_environment():
    print_header("ENVIRONMENT VARIABLES")
    
    required_vars = {
        'DB_NAME': os.getenv('DB_NAME'),
        'DB_USER': os.getenv('DB_USER'),
        'DB_PASSWORD': os.getenv('DB_PASSWORD'),
        'DB_HOST': os.getenv('DB_HOST'),
        'DB_PORT': os.getenv('DB_PORT'),
        'SECRET_KEY': os.getenv('SECRET_KEY'),
        'DEBUG': os.getenv('DEBUG'),
    }
    
    optional_vars = {
        'GEMINI_API_KEY': os.getenv('GEMINI_API_KEY'),
        'OPENAI_API_KEY': os.getenv('OPENAI_API_KEY'),
    }
    
    print("Required Variables:")
    all_present = True
    for var, value in required_vars.items():
        if value:
            # Mask sensitive values
            if 'PASSWORD' in var or 'KEY' in var:
                display_value = f"{value[:4]}...{value[-4:]}" if len(value) > 8 else "***"
            else:
                display_value = value
            print_success(f"{var}: {display_value}")
        else:
            print_error(f"{var}: NOT SET")
            all_present = False
    
    print("\nOptional Variables (AI):")
    for var, value in optional_vars.items():
        if value:
            display_value = f"{value[:4]}...{value[-4:]}" if len(value) > 8 else "***"
            print_success(f"{var}: {display_value}")
        else:
            print_warning(f"{var}: Not set (AI features limited)")
    
    return all_present

# ==================== 8. DJANGO SETTINGS ====================
def test_django_settings():
    print_header("DJANGO CONFIGURATION")
    
    from django.conf import settings
    
    print_info(f"Debug Mode: {settings.DEBUG}")
    print_info(f"Database Engine: {settings.DATABASES['default']['ENGINE']}")
    print_info(f"Installed Apps: {len(settings.INSTALLED_APPS)}")
    
    # Check for required apps
    required_apps = ['rest_framework', 'corsheaders', 'interviews']
    for app in required_apps:
        if app in settings.INSTALLED_APPS:
            print_success(f"App '{app}' installed")
        else:
            print_error(f"App '{app}' NOT installed")
    
    # Check CORS
    if hasattr(settings, 'CORS_ALLOWED_ORIGINS'):
        print_success(f"CORS configured: {len(settings.CORS_ALLOWED_ORIGINS)} origins")
    
    return True

# ==================== MAIN ====================
def main():
    print(f"\n{BLUE}{'*' * 60}")
    print(f"   AI INTERVIEW BACKEND - COMPREHENSIVE VERIFICATION")
    print(f"{'*' * 60}{RESET}\n")
    
    results = {
        'Environment Variables': test_environment(),
        'Django Configuration': test_django_settings(),
        'Database Connection': test_database_connection(),
        'Database Models': test_models(),
        'Gemini API': test_gemini_api(),
        'OpenAI API': test_openai_api(),
        'Speech Recognition': test_speech_recognition(),
        'PDF Generation': test_pdf_generation(),
    }
    
    # Summary
    print_header("VERIFICATION SUMMARY")
    
    total = len(results)
    passed = sum(1 for v in results.values() if v)
    
    for test, result in results.items():
        if result:
            print_success(f"{test}: PASSED")
        else:
            print_error(f"{test}: FAILED")
    
    print(f"\n{BLUE}Results: {passed}/{total} tests passed{RESET}")
    
    if passed == total:
        print(f"\n{GREEN}🎉 ALL TESTS PASSED! Your backend is ready to use!{RESET}\n")
    elif passed >= total - 2:
        print(f"\n{YELLOW}⚠️  Most tests passed. Review failed tests above.{RESET}\n")
    else:
        print(f"\n{RED}❌ Several tests failed. Please fix the issues.{RESET}\n")
    
    # Next steps
    print_header("NEXT STEPS")
    
    if not results['Gemini API'] and not results['OpenAI API']:
        print_info("To enable AI features:")
        print("  1. Get Gemini API key: https://makersuite.google.com/app/apikey")
        print("  2. Add to .env: GEMINI_API_KEY=your_key")
        print("  3. Run: pip install google-generativeai")
        print("  4. Run this test again")
    
    print_info("\nStart the server:")
    print("  python manage.py runserver")
    
    print_info("\nAccess points:")
    print("  - API: http://localhost:8000/api/")
    print("  - Admin: http://localhost:8000/admin/")
    print("  - Documentation: See BACKEND_SUMMARY.md\n")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{YELLOW}Test interrupted by user{RESET}")
    except Exception as e:
        print(f"\n{RED}Fatal error: {str(e)}{RESET}")
        import traceback
        traceback.print_exc()
