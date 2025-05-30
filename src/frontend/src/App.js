import logo from './assets/GenAi-Logo-2.svg';
import './App.css';
import React from 'react';
import { Routes, Route } from 'react-router-dom';
import Header from './components/header';
import Hero from './components/hero';
import CookieBanner from './components/cookieBanner';
import ServicesSection from './components/services';
import BackgroundVideo from './components/backgroundVideo.js';
import HomePage from './pages/homepage.js';
import FlashcardsPage from './pages/FlashcardsPage.js';
import QuestionsPage from './pages/QuestionsPage.js';
import ProcrastinationPage from './pages/ProcrastinationPage.js';

function App() {
  return (
    <div className="App">
      <Header />

      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/flashcards" element={<FlashcardsPage />} />
        <Route path="/questions" element={<QuestionsPage />} />
        <Route path="/procrastination" element={<ProcrastinationPage />} />
      </Routes>
    </div>
  );
}

export default App;
