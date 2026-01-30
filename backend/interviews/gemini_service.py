"""
AI Service using Google Gemini API for conducting interviews
"""
import os
from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    logger.warning("Google Gemini library not installed. AI features will be limited.")


class GeminiAIInterviewer:
    """
    AI Interviewer class using Google Gemini API
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the Gemini AI Interviewer
        
        Args:
            api_key: Gemini API key (optional, will use environment variable if not provided)
        """
        if not GEMINI_AVAILABLE:
            raise ImportError("Google Gemini library is required. Install with: pip install google-generativeai")
        
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            raise ValueError("Gemini API key is required. Set GEMINI_API_KEY environment variable or pass it to constructor.")
        
        # Configure Gemini
        genai.configure(api_key=self.api_key)
        
        # Use Gemini 1.5 Flash (fast and free tier available)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        self.chat = None
        self.conversation_history: List[Dict[str, str]] = []
        self.system_prompt = ""
    
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
        self.system_prompt = self._build_system_prompt(questions, context)
        
        # Start a new chat session with system instructions
        self.chat = self.model.start_chat(history=[])
        
        # Reset conversation history
        self.conversation_history = []
        
        # Get the opening message
        opening_message = self._send_message("Start the interview with a warm greeting.")
        
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
    
    def _send_message(self, message: str) -> str:
        """
        Send a message to Gemini and get response
        
        Args:
            message: The message to send
        
        Returns:
            AI's response
        """
        try:
            # Prepend system prompt to first message
            if not self.conversation_history:
                full_message = f"{self.system_prompt}\n\n{message}"
            else:
                full_message = message
            
            # Send message and get response
            response = self.chat.send_message(full_message)
            ai_message = response.text
            
            # Store in conversation history
            self.conversation_history.append({
                "role": "user",
                "content": message
            })
            self.conversation_history.append({
                "role": "assistant",
                "content": ai_message
            })
            
            return ai_message
        
        except Exception as e:
            logger.error(f"Error getting Gemini response: {str(e)}")
            raise Exception(f"AI service error: {str(e)}")
    
    def get_ai_response(self, student_response: str = None) -> str:
        """
        Get AI's response to student's answer
        
        Args:
            student_response: The student's response to the previous question
        
        Returns:
            AI's next question or response
        """
        if not self.chat:
            raise Exception("Interview not initialized. Call initialize_interview first.")
        
        if student_response:
            return self._send_message(student_response)
        else:
            # Just getting the next question without student response
            return self._send_message("Please ask the next question.")
    
    def end_interview(self) -> str:
        """
        End the interview gracefully
        
        Returns:
            Closing message from the AI interviewer
        """
        if not self.chat:
            return "Thank you for your time."
        
        closing_message = self._send_message(
            "The interview is now complete. Thank the candidate and provide a professional closing statement."
        )
        
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


# Mock AI Interviewer for testing without API key
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
