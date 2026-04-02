import React from 'react';
import * as Avatar from '@radix-ui/react-avatar';
import './AgentCard.css';

const AgentCard = () => {
    return (
        <div className="card agent-card">
            <div className="agent-avatar-wrapper">
                <Avatar.Root className="AvatarRoot agent-avatar-large">
                    <Avatar.Image
                        className="AvatarImage"
                        src="https://img.freepik.com/free-psd/3d-illustration-person-with-sunglasses_23-2149436188.jpg?w=200" // Placeholder 3D avatar
                        alt="Alex"
                    />
                    <Avatar.Fallback className="AvatarFallback">AG</Avatar.Fallback>
                </Avatar.Root>
            </div>

            <div className="agent-info">
                <h3>Meet "<span className="highlight">Alex</span>", your<br />Technical Specialist today</h3>
                <p className="agent-bio">
                    Alex is trained to assess your skills in React, System Design, and Algorithms
                </p>
            </div>
        </div>
    );
};

export default AgentCard;
