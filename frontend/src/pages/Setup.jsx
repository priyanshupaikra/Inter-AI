import React, { useState } from 'react';
import { User, Mail, Clock } from 'lucide-react';
import './Setup.css';

const Setup = ({ onStartInterview }) => {
    const [formData, setFormData] = useState({
        studentName: '',
        studentEmail: '',
        interviewTitle: 'Software Engineer Technical Interview',
        duration: 30,
    });
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    const handleChange = (e) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value,
        });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();

        if (!formData.studentName.trim() || !formData.studentEmail.trim()) {
            setError('Please fill in all required fields');
            return;
        }

        setLoading(true);
        setError('');

        try {
            await onStartInterview(formData);
        } catch (err) {
            setError(err.message || 'Failed to start interview. Please try again.');
            setLoading(false);
        }
    };

    return (
        <div className="setup-container">
            <div className="setup-card">
                <div className="setup-header">
                    <div className="logo-section-setup">
                        <span className="logo-icon">AI</span>
                        <span className="logo-text">Inter AI</span>
                    </div>
                    <h1 className="setup-title">Welcome to AI Interview</h1>
                    <p className="setup-subtitle">
                        Prepare for your technical interview with our AI-powered interviewer
                    </p>
                </div>

                <form onSubmit={handleSubmit} className="setup-form">
                    <div className="form-group">
                        <label htmlFor="studentName">
                            <User size={18} />
                            Full Name *
                        </label>
                        <input
                            type="text"
                            id="studentName"
                            name="studentName"
                            value={formData.studentName}
                            onChange={handleChange}
                            placeholder="Enter your full name"
                            required
                        />
                    </div>

                    <div className="form-group">
                        <label htmlFor="studentEmail">
                            <Mail size={18} />
                            Email Address *
                        </label>
                        <input
                            type="email"
                            id="studentEmail"
                            name="studentEmail"
                            value={formData.studentEmail}
                            onChange={handleChange}
                            placeholder="your.email@example.com"
                            required
                        />
                    </div>

                    <div className="form-group">
                        <label htmlFor="interviewTitle">
                            Interview Type
                        </label>
                        <input
                            type="text"
                            id="interviewTitle"
                            name="interviewTitle"
                            value={formData.interviewTitle}
                            onChange={handleChange}
                        />
                    </div>

                    <div className="form-group">
                        <label htmlFor="duration">
                            <Clock size={18} />
                            Duration (minutes)
                        </label>
                        <select
                            id="duration"
                            name="duration"
                            value={formData.duration}
                            onChange={handleChange}
                        >
                            <option value={15}>15 minutes</option>
                            <option value={30}>30 minutes</option>
                            <option value={45}>45 minutes</option>
                            <option value={60}>60 minutes</option>
                        </select>
                    </div>

                    {error && <div className="error-message">{error}</div>}

                    <button type="submit" className="start-btn" disabled={loading}>
                        {loading ? 'Setting up interview...' : 'Start Interview'}
                    </button>
                </form>

                <div className="setup-features">
                    <div className="feature-item">
                        <div className="feature-icon">✓</div>
                        <span>AI-powered questions</span>
                    </div>
                    <div className="feature-item">
                        <div className="feature-icon">✓</div>
                        <span>Real-time feedback</span>
                    </div>
                    <div className="feature-item">
                        <div className="feature-icon">✓</div>
                        <span>Detailed report</span>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Setup;
