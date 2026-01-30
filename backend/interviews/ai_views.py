from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404
from .models import InterviewSession, Question, Conversation
from .gemini_service import GeminiAIInterviewer, MockAIInterviewer
from .ai_service import AIInterviewer
import logging
import os

logger = logging.getLogger(__name__)

# Store active AI interviewer sessions in memory
# In production, consider using Redis or similar for session management
active_ai_sessions = {}

class AIInterviewView(APIView):
    """
    API endpoint for AI interview interactions
    """
    permission_classes = [AllowAny]
    
    def post(self, request):
        """
        Handle AI interview actions
        
        Actions:
        - initialize: Start a new AI interview session
        - respond: Get AI's response to student's answer
        - end: End the interview session
        """
        action = request.data.get('action')
        session_id = request.data.get('session_id')
        
        if not session_id:
            return Response(
                {'error': 'session_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get the session
        try:
            session = InterviewSession.objects.get(session_id=session_id)
        except InterviewSession.DoesNotExist:
            return Response(
                {'error': 'Session not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        if action == 'initialize':
            return self._initialize_interview(request, session)
        elif action == 'respond':
            return self._get_ai_response(request, session)
        elif action == 'end':
            return self._end_interview(request, session)
        else:
            return Response(
                {'error': 'Invalid action. Must be one of: initialize, respond, end'},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    def _initialize_interview(self, request, session):
        """Initialize AI interview session"""
        try:
            # Get questions for this session
            questions = list(session.questions.all().order_by('order').values_list('question_text', flat=True))
            
            if not questions:
                return Response(
                    {'error': 'No questions found for this session'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Create context
            context = {
                'title': session.title,
                'student_name': session.student.name,
                'duration': f"{session.duration_minutes} minutes"
            }
            
            # Try to use AI interviewer in order of preference:
            # 1. Gemini (if GEMINI_API_KEY is set)
            # 2. OpenAI (if OPENAI_API_KEY is set)
            # 3. Mock (fallback - no API key needed)
            ai_interviewer = None
            
            # Try Gemini first
            if os.getenv('GEMINI_API_KEY'):
                try:
                    ai_interviewer = GeminiAIInterviewer()
                    logger.info("Using Gemini AI interviewer")
                except Exception as e:
                    logger.warning(f"Failed to initialize Gemini AI: {str(e)}")
            
            # Try OpenAI if Gemini failed or not configured
            if not ai_interviewer and os.getenv('OPENAI_API_KEY'):
                try:
                    ai_interviewer = AIInterviewer()
                    logger.info("Using OpenAI interviewer")
                except Exception as e:
                    logger.warning(f"Failed to initialize OpenAI: {str(e)}")
            
            # Fall back to Mock if no AI is available
            if not ai_interviewer:
                logger.info("Using Mock AI interviewer (no API keys configured)")
                ai_interviewer = MockAIInterviewer()
            
            # Initialize the interview
            opening_message = ai_interviewer.initialize_interview(questions, context)
            
            # Store the AI session
            active_ai_sessions[str(session.session_id)] = ai_interviewer
            
            # Save the opening message to conversation
            Conversation.objects.create(
                session=session,
                speaker='ai',
                message=opening_message
            )
            
            # Get the first question
            first_question = ai_interviewer.get_ai_response("Please ask the first question.")
            
            # Save the first question
            Conversation.objects.create(
                session=session,
                speaker='ai',
                message=first_question,
                question=session.questions.first()
            )
            
            return Response({
                'success': True,
                'opening_message': opening_message,
                'first_question': first_question
            })
        
        except Exception as e:
            logger.error(f"Error initializing AI interview: {str(e)}")
            return Response(
                {'error': f'Failed to initialize interview: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def _get_ai_response(self, request, session):
        """Get AI's response to student's answer"""
        student_response = request.data.get('student_response')
        
        if not student_response:
            return Response(
                {'error': 'student_response is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        session_key = str(session.session_id)
        
        # Check if AI session exists
        if session_key not in active_ai_sessions:
            return Response(
                {'error': 'AI session not found. Please initialize the interview first.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            ai_interviewer = active_ai_sessions[session_key]
            
            # Save student's response
            Conversation.objects.create(
                session=session,
                speaker='student',
                message=student_response
            )
            
            # Get AI's response
            ai_response = ai_interviewer.get_ai_response(student_response)
            
            # Save AI's response
            Conversation.objects.create(
                session=session,
                speaker='ai',
                message=ai_response
            )
            
            return Response({
                'success': True,
                'ai_response': ai_response
            })
        
        except Exception as e:
            logger.error(f"Error getting AI response: {str(e)}")
            return Response(
                {'error': f'Failed to get AI response: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def _end_interview(self, request, session):
        """End the AI interview session"""
        session_key = str(session.session_id)
        
        if session_key not in active_ai_sessions:
            return Response(
                {'error': 'AI session not found'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            ai_interviewer = active_ai_sessions[session_key]
            
            # Get closing message
            closing_message = ai_interviewer.end_interview()
            
            # Save closing message
            Conversation.objects.create(
                session=session,
                speaker='ai',
                message=closing_message
            )
            
            # Get conversation summary
            summary = ai_interviewer.get_conversation_summary()
            
            # Remove from active sessions
            del active_ai_sessions[session_key]
            
            return Response({
                'success': True,
                'closing_message': closing_message,
                'summary': summary
            })
        
        except Exception as e:
            logger.error(f"Error ending AI interview: {str(e)}")
            return Response(
                {'error': f'Failed to end interview: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
