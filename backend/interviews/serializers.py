from rest_framework import serializers
from .models import Interviewer, Student, InterviewSession, Question, Conversation, InterviewReport
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class InterviewerSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Interviewer
        fields = ['id', 'user', 'name', 'email', 'created_at']

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'name', 'email', 'created_at']

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'session', 'question_text', 'category', 'difficulty', 
                  'order', 'expected_answer', 'created_at']
        read_only_fields = ['created_at']

class ConversationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversation
        fields = ['id', 'session', 'question', 'speaker', 'message', 
                  'audio_file', 'timestamp']
        read_only_fields = ['timestamp']

class InterviewSessionSerializer(serializers.ModelSerializer):
    interviewer = InterviewerSerializer(read_only=True)
    student = StudentSerializer(read_only=True)
    questions = QuestionSerializer(many=True, read_only=True)
    conversations = ConversationSerializer(many=True, read_only=True)
    interviewer_id = serializers.PrimaryKeyRelatedField(
        queryset=Interviewer.objects.all(), 
        source='interviewer', 
        write_only=True
    )
    student_id = serializers.PrimaryKeyRelatedField(
        queryset=Student.objects.all(), 
        source='student', 
        write_only=True
    )
    
    class Meta:
        model = InterviewSession
        fields = ['id', 'session_id', 'interviewer', 'student', 'title', 
                  'description', 'duration_minutes', 'status', 'scheduled_at', 
                  'started_at', 'ended_at', 'created_at', 'updated_at',
                  'questions', 'conversations', 'interviewer_id', 'student_id']
        read_only_fields = ['session_id', 'created_at', 'updated_at']

class InterviewSessionListSerializer(serializers.ModelSerializer):
    """Simplified serializer for list views"""
    interviewer_name = serializers.CharField(source='interviewer.name', read_only=True)
    student_name = serializers.CharField(source='student.name', read_only=True)
    question_count = serializers.SerializerMethodField()
    
    class Meta:
        model = InterviewSession
        fields = ['id', 'session_id', 'interviewer_name', 'student_name', 
                  'title', 'duration_minutes', 'status', 'scheduled_at', 
                  'created_at', 'question_count']
    
    def get_question_count(self, obj):
        return obj.questions.count()

class InterviewReportSerializer(serializers.ModelSerializer):
    session_title = serializers.CharField(source='session.title', read_only=True)
    
    class Meta:
        model = InterviewReport
        fields = ['id', 'session', 'session_title', 'pdf_file', 'generated_at']
        read_only_fields = ['generated_at']
