import React, { useState, useEffect } from 'react';
import Header from '../components/Header';
import HardwareCheck from '../components/HardwareCheck';
import WelcomeCard from '../components/WelcomeCard';
import AgentCard from '../components/AgentCard';
import SessionView from '../components/SessionView';
import Controls from '../components/Controls';
import {
    sendStudentResponse,
    endAIInterview,
    endSession,
    generateReport,
    downloadReport,
    voiceToText
} from '../services/api';
import './Interview.css';

const Interview = ({ interviewData, onEndInterview }) => {
    const [currentQuestion, setCurrentQuestion] = useState(interviewData.firstQuestion || '');
    const [conversations, setConversations] = useState([]);
    const [studentResponse, setStudentResponse] = useState('');
    const [isRecording, setIsRecording] = useState(false);
    const [mediaRecorder, setMediaRecorder] = useState(null);
    const [isProcessing, setIsProcessing] = useState(false);
    const [error, setError] = useState('');

    useEffect(() => {
        if (interviewData.firstQuestion) {
            setConversations([{
                speaker: 'ai',
                message: interviewData.firstQuestion,
                timestamp: new Date().toISOString()
            }]);
        }
    }, [interviewData.firstQuestion]);

    // Handle text response submission
    const handleSubmitResponse = async () => {
        if (!studentResponse.trim() || isProcessing) return;

        setIsProcessing(true);
        setError('');

        try {
            const response = await sendStudentResponse(
                interviewData.sessionUUID,
                studentResponse
            );

            // Add conversations
            setConversations(prev => [
                ...prev,
                { speaker: 'student', message: studentResponse, timestamp: new Date().toISOString() },
                { speaker: 'ai', message: response.ai_response, timestamp: new Date().toISOString() }
            ]);

            setCurrentQuestion(response.ai_response);
            setStudentResponse('');
        } catch (err) {
            console.error('Error submitting response:', err);
            setError('Failed to send response. Please try again.');
        } finally {
            setIsProcessing(false);
        }
    };

    // Voice recording
    const startRecording = async () => {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({
                audio: {
                    echoCancellation: true,
                    noiseSuppression: true,
                    sampleRate: 44100,
                }
            });

            const recorder = new MediaRecorder(stream);
            const chunks = [];

            recorder.ondataavailable = (e) => chunks.push(e.data);

            recorder.onstop = async () => {
                const audioBlob = new Blob(chunks, { type: 'audio/wav' });

                try {
                    setIsProcessing(true);
                    // Convert to text
                    const result = await voiceToText(audioBlob);
                    setStudentResponse(result.text);
                } catch (err) {
                    console.error('Transcription error:', err);
                    setError('Failed to transcribe audio. Please try typing instead.');
                } finally {
                    setIsProcessing(false);
                }

                // Stop stream
                stream.getTracks().forEach(track => track.stop());
            };

            recorder.start();
            setMediaRecorder(recorder);
            setIsRecording(true);

        } catch (err) {
            console.error('Recording error:', err);
            setError('Failed to access microphone. Please check permissions.');
        }
    };

    const stopRecording = () => {
        if (mediaRecorder && mediaRecorder.state !== 'inactive') {
            mediaRecorder.stop();
            setIsRecording(false);
        }
    };

    // End interview
    const handleEndInterview = async () => {
        if (!confirm('Are you sure you want to end this interview?')) return;

        setIsProcessing(true);
        setError('');

        try {
            await endAIInterview(interviewData.sessionUUID);
            await endSession(interviewData.sessionId);

            // Generate and download report
            const report = await generateReport(interviewData.sessionUUID);
            downloadReport(report.pdf_file);

            onEndInterview();
        } catch (err) {
            console.error('Error ending interview:', err);
            setError('Failed to end interview. Please try again.');
            setIsProcessing(false);
        }
    };

    return (
        <div className="app-container">
            <Header studentName={interviewData.studentName} />

            <main className="main-content">
                {/* Top Grid: Hardware - Welcome - Agent */}
                <div className="top-grid">
                    <div className="grid-item hardware-area">
                        <HardwareCheck />
                    </div>

                    <div className="grid-item welcome-area">
                        <WelcomeCard
                            studentName={interviewData.studentName}
                            currentQuestion={currentQuestion}
                            isProcessing={isProcessing}
                        />
                    </div>

                    <div className="grid-item agent-area">
                        <AgentCard />
                    </div>
                </div>

                {/* Middle Section: Session View */}
                <div className="session-area">
                    <SessionView
                        conversations={conversations}
                        currentQuestion={currentQuestion}
                    />
                </div>

                {/* Response Input Area */}
                <div className="response-area">
                    {error && <div className="error-banner">{error}</div>}

                    <div className="response-input-container">
                        <textarea
                            value={studentResponse}
                            onChange={(e) => setStudentResponse(e.target.value)}
                            placeholder="Type your response here..."
                            className="response-textarea"
                            disabled={isProcessing}
                            onKeyDown={(e) => {
                                if (e.key === 'Enter' && e.ctrlKey) {
                                    handleSubmitResponse();
                                }
                            }}
                        />

                        <div className="response-actions">
                            <button
                                onClick={isRecording ? stopRecording : startRecording}
                                className={`record-btn ${isRecording ? 'recording' : ''}`}
                                disabled={isProcessing && !isRecording}
                            >
                                {isRecording ? '⏹ Stop Recording' : '🎤 Record Answer'}
                            </button>

                            <button
                                onClick={handleSubmitResponse}
                                className="submit-btn"
                                disabled={!studentResponse.trim() || isProcessing}
                            >
                                {isProcessing ? 'Processing...' : 'Submit Response'}
                            </button>
                        </div>

                        <div className="response-hint">
                            Press Ctrl+Enter to submit quickly
                        </div>
                    </div>
                </div>

                {/* Bottom Section: Controls & Footer */}
                <div className="controls-area">
                    <Controls onEndInterview={handleEndInterview} isProcessing={isProcessing} />
                </div>
            </main>
        </div>
    );
};

export default Interview;
