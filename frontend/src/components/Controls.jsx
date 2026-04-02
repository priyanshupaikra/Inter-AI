import React from 'react';
import { ArrowRight } from 'lucide-react';
import './Controls.css';

const Controls = ({ onEndInterview, isProcessing = false }) => {
    return (
        <div className="controls-container">
            {/* End Interview Button */}
            <div className="control-group end-interview-group">
                <button className="end-interview-btn" onClick={onEndInterview} disabled={isProcessing}>
                    <span>End Interview</span>
                    <div className="pulse-circle">
                        <div className="inner-pulse"></div>
                    </div>
                </button>
                <span className="practice-label">Practice Mode available</span>
            </div>

            {/* Vibe Meter */}
            <div className="control-group vibe-group">
                <div className="vibe-meter">
                    <div className="vibe-icon-down">↓</div>
                </div>
                <div className="vibe-text">
                    <span className="vibe-label">Vibe Meter</span>
                    <span className="vibe-status">Good Connection</span>
                </div>
            </div>

            {/* Compliance Footer */}
            <div className="compliance-container">
                <div className="gdpr-pill">
                    GDPR Compliant
                </div>

                <div className="encryption-pill">
                    <span>Data Encrypted</span>
                    <svg width="16" height="16" viewBox="0 0 16 16" fill="none" className="shield-icon">
                        <path d="M8 1L3 3v4c0 3.5 2.5 6.5 5 7 2.5-.5 5-3.5 5-7V3l-5-2z" stroke="currentColor" strokeWidth="1.5" fill="none" />
                        <path d="M6 8l1.5 1.5L11 6" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" />
                    </svg>
                </div>
            </div>
        </div>
    );
};

export default Controls;
