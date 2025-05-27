import logo from './assets/GenAi-Logo-2.svg';
import './App.css';
import React from 'react';
import Header from './components/header';
import Hero from './components/hero';
import CookieBanner from './components/cookieBanner';
import ServicesSection from './components/services';

function App() {
  return (
    <div className="App">
      <Header />
      <Hero />
      <ServicesSection />
    </div>
  );
}

export default App;
