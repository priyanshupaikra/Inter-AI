import React from 'react';
import * as Avatar from '@radix-ui/react-avatar';
import './SessionView.css';

const SessionView = ({ conversations = [], currentQuestion = '' }) => {
    return (
        <div className="session-container">
            {/* Left Side: Your View */}
            <div className="view-section user-view-section">
                <h4 className="view-title">Your View</h4>
                <div className="user-feed-container">
                    <div className="video-feed">
                        <img
                            src="https://images.unsplash.com/photo-1539571696357-5a69c17a67c6?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80"
                            alt="User"
                            className="feed-image"
                        />
                    </div>

                    <div className="audio-visualizer">
                        <div className="waveform">
                            {[...Array(20)].map((_, i) => (
                                <div key={i} className="wave-bar" style={{
                                    height: `${20 + Math.random() * 60}%`,
                                    animationDelay: `${i * 0.05}s`
                                }}></div>
                            ))}
                        </div>
                    </div>
                </div>

                {/* Show latest student response */}
                {conversations.length > 0 && (
                    <div className="transcript-box">
                        <div className="transcript-icon-container">
                            <div className="sound-wave-icon">
                                <span></span><span></span><span></span>
                            </div>
                        </div>
                        <p className="transcript-text">
                            {conversations.filter(c => c.speaker === 'student').slice(-1)[0]?.message || 'Waiting for your response...'}
                        </p>
                    </div>
                )}
            </div>

            {/* Right Side: Interviewer View */}
            <div className="view-section agent-view-section">
                <h4 className="view-title">Interviewer's View</h4>
                <div className="agent-interaction-card">
                    <div className="agent-mini-avatar">
                        <Avatar.Root className="AvatarRoot mini-avatar">
                            <Avatar.Image
                                className="AvatarImage"
                                src="https://img.freepik.com/free-psd/3d-illustration-person-with-sunglasses_23-2149436188.jpg?w=100"
                                alt="Alex"
                            />
                            <Avatar.Fallback className="AvatarFallback">AI</Avatar.Fallback>
                        </Avatar.Root>
                    </div>
                    <div className="agent-speech-bubble">
                        <p>{currentQuestion || 'The AI interviewer is preparing...'}</p>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default SessionView;
