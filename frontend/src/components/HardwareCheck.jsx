import React from 'react';
import { Camera, Mic, CheckCircle2 } from 'lucide-react';
import './HardwareCheck.css';

const HardwareCheck = () => {
    return (
        <div className="card hardware-card">
            <h3 className="card-title">Hardware Check</h3>

            <div className="camera-preview">
                <img
                    src="https://images.unsplash.com/photo-1539571696357-5a69c17a67c6?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80"
                    alt="Camera Feed"
                    className="preview-image"
                />
            </div>

            <div className="status-list">
                <div className="status-item success">
                    <div className="status-icon-bg">
                        <CheckCircle2 size={18} />
                    </div>
                    <span>Camera: Active</span>
                    <CheckCircle2 size={18} className="check-trailing" />
                </div>

                <div className="status-item success">
                    <div className="status-icon-bg">
                        <Mic size={18} />
                    </div>
                    <span>Microphone: Good</span>
                    <div className="mic-level-indicator">
                        <Mic size={18} className="mic-active" />
                    </div>
                </div>
            </div>
        </div>
    );
};

export default HardwareCheck;
