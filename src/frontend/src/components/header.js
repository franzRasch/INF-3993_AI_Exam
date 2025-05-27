import React from 'react';
import '../css/header.css';
import logo from '../assets/logo.svg';

export default function Header() {
  return (
    <header className="header">
      <div className="logo">
        <img src={logo} alt="Logo" className="logo-icon" />
        Your <strong>AI</strong> Tutor
      </div>
      <nav className="nav-center">
        <ul className="nav-links">
          <li>Flashcard generation</li>
          <li>Talk to it</li>
          <li>Procrastinate</li>
          <li>About the team behind AiT</li>
        </ul>
      </nav>
      <div className="header-right">
        <button className="cta-button">Frequently asked questions</button>
      </div>
    </header>
  );
}
