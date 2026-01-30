from django.db import models
from django.contrib.auth.models import User
import uuid

class Interviewer(models.Model):
    """Model for interviewers who create interview sessions"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='interviewer_profile', null=True, blank=True)
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class Student(models.Model):
    """Model for students who take interviews"""
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class InterviewSession(models.Model):
    """Model for interview sessions"""
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    session_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    interviewer = models.ForeignKey(Interviewer, on_delete=models.CASCADE, related_name='sessions')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='sessions')
    title = models.CharField(max_length=300)
    description = models.TextField(blank=True, null=True)
    duration_minutes = models.IntegerField(help_text="Duration in minutes")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    scheduled_at = models.DateTimeField()
    started_at = models.DateTimeField(null=True, blank=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.student.name}"

class Question(models.Model):
    """Model for interview questions"""
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]
    
    session = models.ForeignKey(InterviewSession, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()
    category = models.CharField(max_length=100, blank=True, null=True)
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='medium')
    order = models.IntegerField(default=0)
    expected_answer = models.TextField(blank=True, null=True, help_text="Optional expected answer for reference")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order', 'created_at']
    
    def __str__(self):
        return f"Q{self.order}: {self.question_text[:50]}..."

class Conversation(models.Model):
    """Model for storing the conversation between AI and student"""
    SPEAKER_CHOICES = [
        ('ai', 'AI'),
        ('student', 'Student'),
    ]
    
    session = models.ForeignKey(InterviewSession, on_delete=models.CASCADE, related_name='conversations')
    question = models.ForeignKey(Question, on_delete=models.SET_NULL, null=True, blank=True, related_name='responses')
    speaker = models.CharField(max_length=10, choices=SPEAKER_CHOICES)
    message = models.TextField()
    audio_file = models.FileField(upload_to='audio_recordings/', null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['timestamp']
    
    def __str__(self):
        return f"{self.speaker} - {self.timestamp}"

class InterviewReport(models.Model):
    """Model for storing generated PDF reports"""
    session = models.OneToOneField(InterviewSession, on_delete=models.CASCADE, related_name='report')
    pdf_file = models.FileField(upload_to='interview_reports/')
    generated_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Report for {self.session.title}"
