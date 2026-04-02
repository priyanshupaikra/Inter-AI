import { apiCall, API_BASE_URL } from './config';

// ========== Interviewer APIs ==========
export const createInterviewer = async (name, email) => {
  return apiCall('/interviewers/', {
    method: 'POST',
    body: JSON.stringify({ name, email }),
  });
};

// ========== Student APIs ==========
export const createStudent = async (name, email) => {
  return apiCall('/students/', {
    method: 'POST',
    body: JSON.stringify({ name, email }),
  });
};

// ========== Session APIs ==========
export const createSession = async (sessionData) => {
  return apiCall('/sessions/', {
    method: 'POST',
    body: JSON.stringify({
      title: sessionData.title,
      interviewer_id: sessionData.interviewerId,  // Changed from 'interviewer' to 'interviewer_id'
      student_id: sessionData.studentId,          // Changed from 'student' to 'student_id'
      duration_minutes: sessionData.durationMinutes,
      scheduled_at: sessionData.scheduledAt,
      description: sessionData.description || '',
    }),
  });
};

export const startSession = async (sessionId) => {
  return apiCall(`/sessions/${sessionId}/start/`, {
    method: 'POST',
  });
};

export const endSession = async (sessionId) => {
  return apiCall(`/sessions/${sessionId}/end/`, {
    method: 'POST',
  });
};

export const getSessionDetails = async (sessionId) => {
  return apiCall(`/sessions/${sessionId}/`);
};

// ========== Question APIs ==========
export const addQuestions = async (questions) => {
  return apiCall('/questions/bulk_create/', {
    method: 'POST',
    body: JSON.stringify({ questions }),
  });
};

// ========== AI Interview APIs ==========
export const initializeAIInterview = async (sessionUUID) => {
  return apiCall('/ai-interview/', {
    method: 'POST',
    body: JSON.stringify({
      action: 'initialize',
      session_id: sessionUUID,
    }),
  });
};

export const sendStudentResponse = async (sessionUUID, studentResponse) => {
  return apiCall('/ai-interview/', {
    method: 'POST',
    body: JSON.stringify({
      action: 'respond',
      session_id: sessionUUID,
      student_response: studentResponse,
    }),
  });
};

export const endAIInterview = async (sessionUUID) => {
  return apiCall('/ai-interview/', {
    method: 'POST',
    body: JSON.stringify({
      action: 'end',
      session_id: sessionUUID,
    }),
  });
};

// ========== Conversation APIs ==========
export const getConversations = async (sessionUUID) => {
  return apiCall(`/conversations/?session_id=${sessionUUID}`);
};

export const saveConversationWithAudio = async (sessionId, speaker, message, audioBlob) => {
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
  
  if (!response.ok) {
    throw new Error('Failed to save conversation');
  }
  
  return response.json();
};

export const voiceToText = async (audioBlob) => {
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

// ========== Report APIs ==========
export const generateReport = async (sessionUUID) => {
  return apiCall('/reports/generate/', {
    method: 'POST',
    body: JSON.stringify({
      session_id: sessionUUID,
    }),
  });
};

export const downloadReport = (pdfUrl) => {
  window.open(`http://localhost:8000${pdfUrl}`, '_blank');
};
