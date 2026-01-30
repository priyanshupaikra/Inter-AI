from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    InterviewerViewSet, StudentViewSet, InterviewSessionViewSet,
    QuestionViewSet, ConversationViewSet, InterviewReportViewSet
)
from .ai_views import AIInterviewView

router = DefaultRouter()
router.register(r'interviewers', InterviewerViewSet, basename='interviewer')
router.register(r'students', StudentViewSet, basename='student')
router.register(r'sessions', InterviewSessionViewSet, basename='session')
router.register(r'questions', QuestionViewSet, basename='question')
router.register(r'conversations', ConversationViewSet, basename='conversation')
router.register(r'reports', InterviewReportViewSet, basename='report')

urlpatterns = [
    path('', include(router.urls)),
    path('ai-interview/', AIInterviewView.as_view(), name='ai-interview'),
]
