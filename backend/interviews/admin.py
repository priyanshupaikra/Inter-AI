from django.contrib import admin
from .models import Interviewer, Student, InterviewSession, Question, Conversation, InterviewReport

@admin.register(Interviewer)
class InterviewerAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'created_at']
    search_fields = ['name', 'email']
    list_filter = ['created_at']

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'created_at']
    search_fields = ['name', 'email']
    list_filter = ['created_at']

@admin.register(InterviewSession)
class InterviewSessionAdmin(admin.ModelAdmin):
    list_display = ['title', 'student', 'interviewer', 'status', 'duration_minutes', 'scheduled_at', 'created_at']
    list_filter = ['status', 'created_at', 'scheduled_at']
    search_fields = ['title', 'student__name', 'interviewer__name']
    readonly_fields = ['session_id', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('session_id', 'title', 'description', 'interviewer', 'student')
        }),
        ('Schedule & Duration', {
            'fields': ('duration_minutes', 'scheduled_at', 'status')
        }),
        ('Timestamps', {
            'fields': ('started_at', 'ended_at', 'created_at', 'updated_at')
        }),
    )

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['question_text_short', 'session', 'category', 'difficulty', 'order', 'created_at']
    list_filter = ['difficulty', 'category', 'created_at']
    search_fields = ['question_text', 'session__title']
    ordering = ['session', 'order']
    
    def question_text_short(self, obj):
        return obj.question_text[:50] + '...' if len(obj.question_text) > 50 else obj.question_text
    question_text_short.short_description = 'Question'

@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ['session', 'speaker', 'message_short', 'timestamp']
    list_filter = ['speaker', 'timestamp']
    search_fields = ['message', 'session__title']
    ordering = ['-timestamp']
    
    def message_short(self, obj):
        return obj.message[:60] + '...' if len(obj.message) > 60 else obj.message
    message_short.short_description = 'Message'

@admin.register(InterviewReport)
class InterviewReportAdmin(admin.ModelAdmin):
    list_display = ['session', 'pdf_file', 'generated_at']
    list_filter = ['generated_at']
    search_fields = ['session__title']
    readonly_fields = ['generated_at']
