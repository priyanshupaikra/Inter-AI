import React, { useState } from 'react';
import Setup from './pages/Setup';
import Interview from './pages/Interview';
import {
  createInterviewer,
  createStudent,
  createSession,
  startSession,
  initializeAIInterview,
  addQuestions
} from './services/api';
import './index.css';
import './App.css';

function App() {
  const [appState, setAppState] = useState({
    stage: 'setup', // 'setup', 'interview', 'completed'
    interviewData: null,
    error: null,
  });

  const handleStartInterview = async (formData) => {
    try {
      // Step 1: Create student (add timestamp to email to avoid duplicates during testing)
      const uniqueEmail = formData.studentEmail.includes('@')
        ? formData.studentEmail.replace('@', `+${Date.now()}@`)
        : `${formData.studentEmail}_${Date.now()}@test.com`;

      const student = await createStudent(formData.studentName, uniqueEmail);
      console.log('✅ Student created:', student);

      // Step 2: Create or get AI interviewer
      let interviewer;
      try {
        interviewer = await createInterviewer('AI Interviewer', 'ai@interai.com');
        console.log('✅ Interviewer created:', interviewer);
      } catch (err) {
        // If interviewer already exists, that's fine - we can use it
        console.log('Interviewer may already exist, using ID 1');
        interviewer = { id: 1, name: 'AI Interviewer', email: 'ai@interai.com' };
      }

      // Step 3: Create interview session
      console.log('Creating session with:', {
        title: formData.interviewTitle,
        interviewer: interviewer.id,
        student: student.id,
        duration_minutes: parseInt(formData.duration),
      });

      const session = await createSession({
        title: formData.interviewTitle,
        interviewerId: interviewer.id,
        studentId: student.id,
        durationMinutes: parseInt(formData.duration),
        scheduledAt: new Date().toISOString(),
        description: 'Technical interview session',
      });
      console.log('✅ Session created:', session);

      // Step 4: Add some default questions (optional)
      await addQuestions([
        {
          session: session.id,
          question_text: 'Tell me about yourself and your background',
          category: 'Introduction',
          difficulty: 'easy',
          order: 1,
        },
        {
          session: session.id,
          question_text: 'Describe your approach to designing scalable microservices',
          category: 'System Design',
          difficulty: 'medium',
          order: 2,
        },
        {
          session: session.id,
          question_text: 'How would you handle data consistency in a distributed system?',
          category: 'System Design',
          difficulty: 'hard',
          order: 3,
        },
      ]).catch(err => console.log('Questions may already exist:', err));

      // Step 5: Start the session
      await startSession(session.id);

      // Step 6: Initialize AI interview
      const aiResponse = await initializeAIInterview(session.session_id);

      // Update app state to interview stage
      setAppState({
        stage: 'interview',
        interviewData: {
          sessionId: session.id,
          sessionUUID: session.session_id,
          studentName: formData.studentName,
          studentEmail: formData.studentEmail,
          firstQuestion: aiResponse.first_question || 'Hello! Let\'s begin the interview.',
        },
        error: null,
      });

    } catch (error) {
      console.error('Failed to start interview:', error);
      throw new Error(error.message || 'Failed to initialize interview. Please check if the backend is running.');
    }
  };

  const handleEndInterview = () => {
    setAppState({
      stage: 'completed',
      interviewData: null,
      error: null,
    });

    // Reset to setup after a delay
    setTimeout(() => {
      setAppState({
        stage: 'setup',
        interviewData: null,
        error: null,
      });
    }, 3000);
  };

  return (
    <div className="app">
      {appState.stage === 'setup' && (
        <Setup onStartInterview={handleStartInterview} />
      )}

      {appState.stage === 'interview' && appState.interviewData && (
        <Interview
          interviewData={appState.interviewData}
          onEndInterview={handleEndInterview}
        />
      )}

      {appState.stage === 'completed' && (
        <div className="completion-screen">
          <div className="completion-card">
            <div className="completion-icon">✓</div>
            <h1>Interview Completed!</h1>
            <p>Your report has been generated and will download shortly.</p>
            <p className="completion-sub">Redirecting to setup...</p>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
