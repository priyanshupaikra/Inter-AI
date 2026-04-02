import React from 'react';
import { Loader2 } from 'lucide-react';
import './WelcomeCard.css';

const WelcomeCard = ({ studentName = 'Alex', currentQuestion = '', isProcessing = false }) => {
    return (
        <div className="card welcome-card">
            <div className="welcome-header">
                <h2 className="welcome-title">Welcome, {studentName}!</h2>
                <p className="welcome-text">
                    Your interview will walk me through your approach to scalable microservices.
                </p>
            </div>

            <div className="processing-section">
                <h3 className="section-label">Current Question:</h3>

                <div className="current-question-text">
                    {isProcessing ? (
                        <div className="processing-indicator">
                            <Loader2 className="spinner" size={20} />
                            <span>Processing your response...</span>
                        </div>
                    ) : (
                        <p>{currentQuestion || 'Waiting to begin...'}</p>
                    )}
                </div>
            </div>
        </div>
    );
};

export default WelcomeCard;
