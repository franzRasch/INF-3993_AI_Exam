import React from 'react';
import '../css/header.css';

export default function Header() {
  return (
    <header className="header">
      <div className="logo">Your <strong>AI</strong> Tutor</div>
      <nav>
        <ul>
          <li>Flashcard generation</li>
          <li>Talk to it</li>
          <li>About the team behind AiT</li>
        </ul>
      </nav>
      <div className="actions">
        <a href="#contact">Q&A</a>
        <button className="button">Frequently asked questions</button>
      </div>
    </header>
  );
}
