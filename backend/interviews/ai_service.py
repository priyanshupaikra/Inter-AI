"""
AI Service for conducting interviews
This module handles the AI interviewer logic using OpenAI's GPT models
"""
import os
from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    logger.warning("OpenAI library not installed. AI features will be limited.")

class AIInterviewer:
    """
    AI Interviewer class that handles conversation with students
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the AI Interviewer
        
        Args:
            api_key: OpenAI API key (optional, will use environment variable if not provided)
        """
        if not OPENAI_AVAILABLE:
            raise ImportError("OpenAI library is required. Install with: pip install openai")
        
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OpenAI API key is required. Set OPENAI_API_KEY environment variable or pass it to constructor.")
        
        self.client = OpenAI(api_key=self.api_key)
        self.conversation_history: List[Dict[str, str]] = []
    
    def initialize_interview(self, questions: List[str], context: Dict[str, str] = None) -> str:
        """
        Initialize the interview session
        
        Args:
            questions: List of questions to ask during the interview
            context: Additional context about the interview (position, company, etc.)
        
        Returns:
            Opening message from the AI interviewer
        """
        # Build the system prompt
        system_prompt = self._build_system_prompt(questions, context)
        
        # Reset conversation history
        self.conversation_history = [
            {"role": "system", "content": system_prompt}
        ]
        
        # Get the opening message
        opening_message = self.get_ai_response("Start the interview with a warm greeting.")
        
        return opening_message
    
    def _build_system_prompt(self, questions: List[str], context: Dict[str, str] = None) -> str:
        """Build the system prompt for the AI interviewer"""
        
        prompt = """You are a professional and friendly AI interviewer. Your role is to conduct a structured interview 
with a student/candidate. You should:

1. Be professional yet warm and encouraging
2. Ask the provided questions one at a time
3. Listen carefully to the candidate's responses
4. Ask relevant follow-up questions when appropriate
5. Provide smooth transitions between topics
6. Keep track of which questions have been asked
7. Manage the interview time effectively
8. End the interview gracefully when all questions are covered

IMPORTANT RULES:
- Only ask ONE question at a time
- Wait for the candidate's response before moving to the next question
- Be encouraging and create a comfortable environment
- If the candidate seems confused, rephrase the question
- Keep your responses concise and professional
"""
        
        # Add context if provided
        if context:
            prompt += f"\n\nINTERVIEW CONTEXT:\n"
            for key, value in context.items():
                prompt += f"- {key}: {value}\n"
        
        # Add questions to ask
        prompt += f"\n\nQUESTIONS TO ASK (in order):\n"
        for i, question in enumerate(questions, 1):
            prompt += f"{i}. {question}\n"
        
        return prompt
    
    def get_ai_response(self, student_response: str = None) -> str:
        """
        Get AI's response to student's answer
        
        Args:
            student_response: The student's response to the previous question
        
        Returns:
            AI's next question or response
        """
        if student_response:
            self.conversation_history.append({
                "role": "user",
                "content": student_response
            })
        
        try:
            # Call OpenAI API
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",  # Using cost-effective model, can upgrade to gpt-4 if needed
                messages=self.conversation_history,
                temperature=0.7,
                max_tokens=300
            )
            
            ai_message = response.choices[0].message.content
            
            # Add AI's response to history
            self.conversation_history.append({
                "role": "assistant",
                "content": ai_message
            })
            
            return ai_message
        
        except Exception as e:
            logger.error(f"Error getting AI response: {str(e)}")
            raise Exception(f"AI service error: {str(e)}")
    
    def end_interview(self) -> str:
        """
        End the interview gracefully
        
        Returns:
            Closing message from the AI interviewer
        """
        closing_prompt = "The interview is now complete. Thank the candidate and provide a professional closing statement."
        
        self.conversation_history.append({
            "role": "user",
            "content": closing_prompt
        })
        
        closing_message = self.get_ai_response()
        
        return closing_message
    
    def get_conversation_summary(self) -> Dict[str, any]:
        """
        Get a summary of the interview conversation
        
        Returns:
            Dictionary containing conversation statistics
        """
        return {
            "total_messages": len(self.conversation_history),
            "student_messages": len([msg for msg in self.conversation_history if msg["role"] == "user"]),
            "ai_messages": len([msg for msg in self.conversation_history if msg["role"] == "assistant"]),
            "conversation": self.conversation_history
        }


# Fallback mock implementation for testing without API key
class MockAIInterviewer:
    """
    Mock AI Interviewer for testing purposes
    """
    
    def __init__(self, api_key: Optional[str] = None):
        self.questions: List[str] = []
        self.current_question_index = 0
        self.conversation_history: List[Dict[str, str]] = []
    
    def initialize_interview(self, questions: List[str], context: Dict[str, str] = None) -> str:
        self.questions = questions
        self.current_question_index = 0
        
        opening_message = "Hello! Welcome to this interview. I'm excited to learn more about you. Let's begin!"
        self.conversation_history.append({
            "role": "assistant",
            "content": opening_message
        })
        
        return opening_message
    
    def get_ai_response(self, student_response: str = None) -> str:
        if student_response:
            self.conversation_history.append({
                "role": "user",
                "content": student_response
            })
        
        # Ask the next question
        if self.current_question_index < len(self.questions):
            question = self.questions[self.current_question_index]
            self.current_question_index += 1
            
            self.conversation_history.append({
                "role": "assistant",
                "content": question
            })
            
            return question
        else:
            return "Thank you for your responses! That concludes our interview."
    
    def end_interview(self) -> str:
        closing_message = "Thank you for taking the time to interview with us today. We appreciate your interest and will be in touch soon. Have a great day!"
        
        self.conversation_history.append({
            "role": "assistant",
            "content": closing_message
        })
        
        return closing_message
    
    def get_conversation_summary(self) -> Dict[str, any]:
        return {
            "total_messages": len(self.conversation_history),
            "student_messages": len([msg for msg in self.conversation_history if msg["role"] == "user"]),
            "ai_messages": len([msg for msg in self.conversation_history if msg["role"] == "assistant"]),
            "conversation": self.conversation_history
        }
