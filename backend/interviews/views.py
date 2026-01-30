from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.utils import timezone
from django.shortcuts import get_object_or_404
from .models import Interviewer, Student, InterviewSession, Question, Conversation, InterviewReport
from .serializers import (
    InterviewerSerializer, StudentSerializer, InterviewSessionSerializer,
    QuestionSerializer, ConversationSerializer, InterviewReportSerializer,
    InterviewSessionListSerializer
)
from .utils import generate_pdf_report, transcribe_audio
import logging

logger = logging.getLogger(__name__)

class InterviewerViewSet(viewsets.ModelViewSet):
    """ViewSet for Interviewer operations"""
    queryset = Interviewer.objects.all()
    serializer_class = InterviewerSerializer
    # permission_classes = [IsAuthenticated]  # Uncomment when authentication is ready
    permission_classes = [AllowAny]

class StudentViewSet(viewsets.ModelViewSet):
    """ViewSet for Student operations"""
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [AllowAny]

class InterviewSessionViewSet(viewsets.ModelViewSet):
    """ViewSet for Interview Session operations"""
    queryset = InterviewSession.objects.all().select_related('interviewer', 'student').prefetch_related('questions', 'conversations')
    permission_classes = [AllowAny]
    
    def get_serializer_class(self):
        if self.action == 'list':
            return InterviewSessionListSerializer
        return InterviewSessionSerializer
    
    @action(detail=True, methods=['post'])
    def start(self, request, pk=None):
        """Start an interview session"""
        session = self.get_object()
        
        if session.status != 'scheduled':
            return Response(
                {'error': 'Session can only be started if it is scheduled'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        session.status = 'in_progress'
        session.started_at = timezone.now()
        session.save()
        
        serializer = self.get_serializer(session)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def end(self, request, pk=None):
        """End an interview session"""
        session = self.get_object()
        
        if session.status != 'in_progress':
            return Response(
                {'error': 'Session can only be ended if it is in progress'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        session.status = 'completed'
        session.ended_at = timezone.now()
        session.save()
        
        serializer = self.get_serializer(session)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def by_session_id(self, request, pk=None):
        """Get session by session_id (UUID)"""
        session_id = pk
        session = get_object_or_404(InterviewSession, session_id=session_id)
        serializer = self.get_serializer(session)
        return Response(serializer.data)

class QuestionViewSet(viewsets.ModelViewSet):
    """ViewSet for Question operations"""
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        session_id = self.request.query_params.get('session_id', None)
        
        if session_id:
            queryset = queryset.filter(session__session_id=session_id)
        
        return queryset
    
    @action(detail=False, methods=['post'])
    def bulk_create(self, request):
        """Bulk create questions for a session"""
        questions_data = request.data.get('questions', [])
        
        if not questions_data:
            return Response(
                {'error': 'No questions provided'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = self.get_serializer(data=questions_data, many=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ConversationViewSet(viewsets.ModelViewSet):
    """ViewSet for Conversation operations"""
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        session_id = self.request.query_params.get('session_id', None)
        
        if session_id:
            queryset = queryset.filter(session__session_id=session_id)
        
        return queryset
    
    def create(self, request, *args, **kwargs):
        """Create a new conversation entry with optional audio transcription"""
        data = request.data.copy()
        
        # If audio file is provided and it's a student message, transcribe it
        if 'audio_file' in request.FILES and data.get('speaker') == 'student':
            audio_file = request.FILES['audio_file']
            try:
                # Transcribe audio to text
                transcribed_text = transcribe_audio(audio_file)
                data['message'] = transcribed_text
            except Exception as e:
                logger.error(f"Error transcribing audio: {str(e)}")
                return Response(
                    {'error': f'Audio transcription failed: {str(e)}'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        serializer = self.get_serializer(data=data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'])
    def voice_to_text(self, request):
        """Convert voice to text without saving to database"""
        if 'audio_file' not in request.FILES:
            return Response(
                {'error': 'No audio file provided'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        audio_file = request.FILES['audio_file']
        
        try:
            transcribed_text = transcribe_audio(audio_file)
            return Response({'text': transcribed_text})
        except Exception as e:
            logger.error(f"Error transcribing audio: {str(e)}")
            return Response(
                {'error': f'Audio transcription failed: {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST
            )

class InterviewReportViewSet(viewsets.ModelViewSet):
    """ViewSet for Interview Report operations"""
    queryset = InterviewReport.objects.all()
    serializer_class = InterviewReportSerializer
    permission_classes = [AllowAny]
    
    @action(detail=False, methods=['post'])
    def generate(self, request):
        """Generate a PDF report for a session"""
        session_id = request.data.get('session_id')
        
        if not session_id:
            return Response(
                {'error': 'session_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            session = InterviewSession.objects.get(session_id=session_id)
        except InterviewSession.DoesNotExist:
            return Response(
                {'error': 'Session not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Check if report already exists
        if hasattr(session, 'report'):
            serializer = self.get_serializer(session.report)
            return Response(serializer.data)
        
        try:
            # Generate PDF report
            pdf_file = generate_pdf_report(session)
            
            # Create report record
            report = InterviewReport.objects.create(
                session=session,
                pdf_file=pdf_file
            )
            
            serializer = self.get_serializer(report)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            logger.error(f"Error generating report: {str(e)}")
            return Response(
                {'error': f'Report generation failed: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
