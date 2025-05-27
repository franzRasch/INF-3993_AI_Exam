import logo from './assets/GenAi-Logo-2.svg';
import './App.css';
import React from 'react';
import Header from './components/header';
import Hero from './components/hero';
import CookieBanner from './components/cookieBanner';


function App() {
  return (
    <div className="App">
      <Header />
      <Hero />
      <CookieBanner />
      {/* <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <a className="App-link" href="https://reactjs.org" target="_blank" rel="noOpener noReferrer">
          Learn React
        </a>
      </header> */}
    </div>
    
  );
}

export default App;
