import React from 'react';
import * as Avatar from '@radix-ui/react-avatar';
import { Bell } from 'lucide-react';
import './Header.css';

const Header = ({ studentName = 'Alex' }) => {
    const currentDate = new Date().toLocaleDateString('en-US', {
        weekday: 'long',
        month: 'long',
        day: 'numeric',
        year: 'numeric'
    });

    const currentTime = new Date().toLocaleTimeString('en-US', {
        hour: '2-digit',
        minute: '2-digit',
        timeZoneName: 'short'
    });


    return (
        <header className="header">
            <div className="logo-section">
                <span className="logo-icon">AI</span>
                <span className="logo-text">Inter AI</span>
            </div>

            <nav className="nav-links">
                <a href="#" className="nav-link">Practice Mode</a>
                <a href="#" className="nav-link active">How It Works</a>
                <a href="#" className="nav-link">Support</a>
            </nav>

            <div className="header-right">
                <div className="date-time">
                    <div className="date">{currentDate}</div>
                    <div className="time">{currentTime}</div>
                </div>

                <div className="user-profile">
                    <div className="notification-badge">
                        <Bell size={16} fill="white" />
                        <span className="badge-dot"></span>
                    </div>
                    <Avatar.Root className="AvatarRoot user-avatar">
                        <Avatar.Image
                            className="AvatarImage"
                            src="https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=100&q=80"
                            alt="User"
                        />
                        <Avatar.Fallback className="AvatarFallback" delayMs={600}>
                            AL
                        </Avatar.Fallback>
                    </Avatar.Root>
                </div>
            </div>
        </header>
    );
};

export default Header;
