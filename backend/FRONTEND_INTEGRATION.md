# Frontend Integration Guide

This guide shows how to integrate the AI Interview backend with your frontend application.

## Base Configuration

```javascript
// config.js
export const API_BASE_URL = 'http://localhost:8000/api';

// Helper function for API calls
export const apiCall = async (endpoint, options = {}) => {
  const url = `${API_BASE_URL}${endpoint}`;
  const response = await fetch(url, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
  });
  
  if (!response.ok) {
    throw new Error(`API Error: ${response.statusText}`);
  }
  
  return response.json();
};
```

## 1. Create Interview Session

```javascript
// Create interviewer (one-time setup)
const createInterviewer = async (name, email) => {
  return apiCall('/interviewers/', {
    method: 'POST',
    body: JSON.stringify({ name, email }),
  });
};

// Create student
const createStudent = async (name, email) => {
  return apiCall('/students/', {
    method: 'POST',
    body: JSON.stringify({ name, email }),
  });
};

// Create interview session
const createSession = async (sessionData) => {
  return apiCall('/sessions/', {
    method: 'POST',
    body: JSON.stringify({
      title: sessionData.title,
      interviewer_id: sessionData.interviewerId,
      student_id: sessionData.studentId,
      duration_minutes: sessionData.durationMinutes,
      scheduled_at: sessionData.scheduledAt,
      description: sessionData.description || '',
    }),
  });
};

// Add questions to session
const addQuestions = async (questions) => {
  return apiCall('/questions/bulk_create/', {
    method: 'POST',
    body: JSON.stringify({ questions }),
  });
};
```

## 2. Start Interview

```javascript
// Start the session
const startSession = async (sessionId) => {
  return apiCall(`/sessions/${sessionId}/start/`, {
    method: 'POST',
  });
};

// Initialize AI interview
const initializeAIInterview = async (sessionUUID) => {
  return apiCall('/ai-interview/', {
    method: 'POST',
    body: JSON.stringify({
      action: 'initialize',
      session_id: sessionUUID,
    }),
  });
};
```

## 3. Conduct Interview

```javascript
// Send student response and get AI's next question
const sendStudentResponse = async (sessionUUID, studentResponse) => {
  return apiCall('/ai-interview/', {
    method: 'POST',
    body: JSON.stringify({
      action: 'respond',
      session_id: sessionUUID,
      student_response: studentResponse,
    }),
  });
};

// Convert voice to text
const voiceToText = async (audioBlob) => {
  const formData = new FormData();
  formData.append('audio_file', audioBlob, 'recording.wav');
  
  const response = await fetch(`${API_BASE_URL}/conversations/voice_to_text/`, {
    method: 'POST',
    body: formData,
  });
  
  if (!response.ok) {
    throw new Error('Voice transcription failed');
  }
  
  return response.json();
};

// Save conversation with audio
const saveConversationWithAudio = async (sessionId, speaker, message, audioBlob) => {
  const formData = new FormData();
  formData.append('session', sessionId);
  formData.append('speaker', speaker);
  formData.append('message', message);
  if (audioBlob) {
    formData.append('audio_file', audioBlob, 'recording.wav');
  }
  
  const response = await fetch(`${API_BASE_URL}/conversations/`, {
    method: 'POST',
    body: formData,
  });
  
  return response.json();
};
```

## 4. End Interview & Generate Report

```javascript
// End AI interview
const endAIInterview = async (sessionUUID) => {
  return apiCall('/ai-interview/', {
    method: 'POST',
    body: JSON.stringify({
      action: 'end',
      session_id: sessionUUID,
    }),
  });
};

// End session
const endSession = async (sessionId) => {
  return apiCall(`/sessions/${sessionId}/end/`, {
    method: 'POST',
  });
};

// Generate PDF report
const generateReport = async (sessionUUID) => {
  return apiCall('/reports/generate/', {
    method: 'POST',
    body: JSON.stringify({
      session_id: sessionUUID,
    }),
  });
};

// Download report
const downloadReport = (pdfUrl) => {
  window.open(`http://localhost:8000${pdfUrl}`, '_blank');
};
```

## 5. Get Interview Data

```javascript
// Get all sessions
const getSessions = async () => {
  return apiCall('/sessions/');
};

// Get session details
const getSessionDetails = async (sessionId) => {
  return apiCall(`/sessions/${sessionId}/`);
};

// Get conversations for a session
const getConversations = async (sessionUUID) => {
  return apiCall(`/conversations/?session_id=${sessionUUID}`);
};

// Get questions for a session
const getQuestions = async (sessionUUID) => {
  return apiCall(`/questions/?session_id=${sessionUUID}`);
};
```

## Complete React Example Component

```jsx
import React, { useState, useEffect } from 'react';

const InterviewComponent = () => {
  const [interviewData, setInterviewData] = useState({
    sessionId: null,
    sessionUUID: null,
    status: 'not_started', // not_started, in_progress, completed
    currentQuestion: '',
    conversations: [],
  });
  
  const [studentResponse, setStudentResponse] = useState('');
  const [isRecording, setIsRecording] = useState(false);
  const [mediaRecorder, setMediaRecorder] = useState(null);

  // Setup interview
  const setupInterview = async () => {
    try {
      // Create student
      const student = await createStudent('John Doe', 'john@example.com');
      
      // Create interviewer (or get existing)
      const interviewer = await createInterviewer('AI Interviewer', 'ai@company.com');
      
      // Create session
      const session = await createSession({
        title: 'Software Engineer Interview',
        interviewerId: interviewer.id,
        studentId: student.id,
        durationMinutes: 30,
        scheduledAt: new Date().toISOString(),
      });
      
      // Add questions
      await addQuestions([
        {
          session: session.id,
          question_text: 'Tell me about yourself',
          category: 'Introduction',
          difficulty: 'easy',
          order: 1,
        },
        {
          session: session.id,
          question_text: 'What are your strengths?',
          category: 'Behavioral',
          difficulty: 'medium',
          order: 2,
        },
      ]);
      
      // Start session
      await startSession(session.id);
      
      // Initialize AI
      const aiResponse = await initializeAIInterview(session.session_id);
      
      setInterviewData({
        sessionId: session.id,
        sessionUUID: session.session_id,
        status: 'in_progress',
        currentQuestion: aiResponse.first_question,
        conversations: [],
      });
      
    } catch (error) {
      console.error('Setup error:', error);
    }
  };

  // Submit student response
  const submitResponse = async () => {
    if (!studentResponse.trim()) return;
    
    try {
      const response = await sendStudentResponse(
        interviewData.sessionUUID,
        studentResponse
      );
      
      setInterviewData(prev => ({
        ...prev,
        currentQuestion: response.ai_response,
        conversations: [
          ...prev.conversations,
          { speaker: 'student', message: studentResponse },
          { speaker: 'ai', message: response.ai_response },
        ],
      }));
      
      setStudentResponse('');
      
    } catch (error) {
      console.error('Submit error:', error);
    }
  };

  // Voice recording
  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const recorder = new MediaRecorder(stream);
      const chunks = [];
      
      recorder.ondataavailable = (e) => chunks.push(e.data);
      
      recorder.onstop = async () => {
        const audioBlob = new Blob(chunks, { type: 'audio/wav' });
        
        // Convert to text
        const result = await voiceToText(audioBlob);
        setStudentResponse(result.text);
        
        // Stop stream
        stream.getTracks().forEach(track => track.stop());
      };
      
      recorder.start();
      setMediaRecorder(recorder);
      setIsRecording(true);
      
    } catch (error) {
      console.error('Recording error:', error);
    }
  };

  const stopRecording = () => {
    if (mediaRecorder) {
      mediaRecorder.stop();
      setIsRecording(false);
    }
  };

  // End interview
  const finishInterview = async () => {
    try {
      await endAIInterview(interviewData.sessionUUID);
      await endSession(interviewData.sessionId);
      
      // Generate report
      const report = await generateReport(interviewData.sessionUUID);
      
      setInterviewData(prev => ({ ...prev, status: 'completed' }));
      
      // Download report
      downloadReport(report.pdf_file);
      
    } catch (error) {
      console.error('End interview error:', error);
    }
  };

  return (
    <div className="interview-container">
      <h1>AI Interview</h1>
      
      {interviewData.status === 'not_started' && (
        <button onClick={setupInterview}>Start Interview</button>
      )}
      
      {interviewData.status === 'in_progress' && (
        <>
          <div className="question-box">
            <h2>Current Question:</h2>
            <p>{interviewData.currentQuestion}</p>
          </div>
          
          <div className="conversation-history">
            {interviewData.conversations.map((conv, index) => (
              <div key={index} className={`message ${conv.speaker}`}>
                <strong>{conv.speaker === 'ai' ? 'AI' : 'You'}:</strong>
                <p>{conv.message}</p>
              </div>
            ))}
          </div>
          
          <div className="response-section">
            <textarea
              value={studentResponse}
              onChange={(e) => setStudentResponse(e.target.value)}
              placeholder="Type your response..."
            />
            
            <div className="controls">
              <button onClick={submitResponse}>Submit Response</button>
              
              <button 
                onClick={isRecording ? stopRecording : startRecording}
                className={isRecording ? 'recording' : ''}
              >
                {isRecording ? 'Stop Recording' : 'Record Answer'}
              </button>
              
              <button onClick={finishInterview}>End Interview</button>
            </div>
          </div>
        </>
      )}
      
      {interviewData.status === 'completed' && (
        <div className="completion-message">
          <h2>Interview Completed!</h2>
          <p>Your report has been generated and downloaded.</p>
        </div>
      )}
    </div>
  );
};

export default InterviewComponent;
```

## WebSocket Support (Advanced)

For real-time updates, you can implement WebSocket support:

```javascript
// Install: pip install channels channels-redis

// In your frontend:
const socket = new WebSocket(`ws://localhost:8000/ws/interview/${sessionUUID}/`);

socket.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('Real-time update:', data);
};

socket.send(JSON.stringify({
  type: 'student_response',
  message: 'My answer...',
}));
```

## Audio Recording Best Practices

```javascript
// Use proper audio constraints
const stream = await navigator.mediaDevices.getUserMedia({
  audio: {
    echoCancellation: true,
    noiseSuppression: true,
    sampleRate: 44100,
  }
});

// Convert to WAV format for better compatibility
// You may want to use a library like 'recordrtc' for this
```

## Error Handling

```javascript
const handleAPIError = (error) => {
  if (error.response) {
    // Server responded with error
    console.error('Server error:', error.response.data);
  } else if (error.request) {
    // Request made but no response
    console.error('Network error:', error.request);
  } else {
    // Other errors
    console.error('Error:', error.message);
  }
};
```

## Testing

```javascript
// Mock data for testing
const mockInterviewData = {
  sessionId: 1,
  sessionUUID: '123e4567-e89b-12d3-a456-426614174000',
  status: 'in_progress',
  currentQuestion: 'Tell me about yourself',
  conversations: [],
};
```

This integration guide provides everything you need to connect your frontend to the AI Interview backend!
