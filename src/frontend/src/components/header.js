import React from 'react';
import { Link } from 'react-router-dom';
import '../css/header.css';
import logo from '../assets/logo.svg';

export default function Header() {
  return (
    <header className="header">
      <div className="logo">
        <Link to="/">
          <img src={logo} alt="Logo" className="logo-icon" />
        </Link>
        Your <strong>AI</strong> Tutor
      </div>
      <nav className="nav-center">
        <ul className="nav-links">
          <li><Link to="/flashcards">Flashcard generation</Link></li>
          <li><Link to="/questions">Talk to it</Link></li>
          <li><Link to="/procrastination">Procrastinate</Link></li>
        </ul>
      </nav>
      <div className="header-right">
        <button className="cta-button">Frequently asked questions</button>
      </div>
    </header>
  );
}
