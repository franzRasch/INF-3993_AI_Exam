import React, { useState } from 'react';
import '../css/FlashcardsPage.css';
import icon1 from '../assets/doodles/11.svg';
import icon2 from '../assets/doodles/12.svg';
import icon3 from '../assets/doodles/13.svg';
import icon4 from '../assets/doodles/14.svg';
import icon5 from '../assets/doodles/15.svg';
import icon6 from '../assets/doodles/16.svg';

const iconSet = [icon1, icon2, icon3, icon4, icon5, icon6];
const colorSet = [
  { base: 'var(--peach-cream)', highlight: 'var(--yellow-lime)' },
  { base: 'var(--peach-cream)', highlight: 'var(--light-pink)' },
  { base: 'var(--peach-cream)', highlight: 'var(--orange)' },
  { base: 'var(--peach-cream)', highlight: 'var(--hot-pink)' },
  { base: 'var(--peach-cream)', highlight: 'var(--aqua)' },
  { base: 'var(--peach-cream)', highlight: 'var(--soft-yellow)' },
];

const flashcards = [
  { front: 'What is React?', back: 'A JS library for building UIs' },
  { front: 'What is JSX?', back: 'A syntax extension for JavaScript' },
  { front: 'What is a hook?', back: 'Functions to manage state and side effects' },
  { front: 'What is useState?', back: 'A hook to manage component state' },
  { front: 'What is useEffect?', back: 'A hook to manage side effects' },
  { front: 'What is props?', back: 'Inputs passed into components' },
  { front: 'What is JSX?', back: 'A syntax extension for JavaScript' },
];
export default function FlashcardsPage() {
  const [userInput, setUserInput] = useState('');

  const handleSubmit = async () => {
    console.log('Clicked submit');
    try {
      const response = await fetch('http://localhost:8000/flashcards/create', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ user_input: userInput }), // ✅ use userInput here
      });

      if (!response.ok) {
        throw new Error('Failed to fetch flashcards');
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder('utf-8');
      let result = '';

      while (true) {
        const { value, done } = await reader.read();
        if (done) break;
        result += decoder.decode(value);
      }

      console.log('Raw stream result:', result);
    } catch (err) {
      console.error('Error:', err.message);
    }
  };

  return (
    <div className="flashcards-page">
      <h1 className="flashcard-title">Create Flashcards!</h1>
      <div className="user-input-wrapper">
        <label htmlFor="userInput">Enter a number:</label>
        <div className="input-group">
          <input type="text" id="userInput" value={userInput} onChange={e => setUserInput(e.target.value)} />
          <button className="submit-button" onClick={handleSubmit}>
            Enter
          </button>
        </div>
      </div>

      <div className="flashcard-grid">
        {flashcards.map((card, index) => {
          const icon = iconSet[index % iconSet.length];
          const { base, highlight } = colorSet[index % colorSet.length];
          return (
            <Flashcard key={index} front={card.front} back={card.back} color={base} highlight={highlight} icon={icon} />
          );
        })}
      </div>
    </div>
  );
}

function Flashcard({ front, back, color, highlight, icon }) {
  const [flipped, setFlipped] = useState(false);

  return (
    <div
      className={`flashcard-box ${flipped ? 'flipped' : ''}`}
      style={{ backgroundColor: flipped ? highlight : color }}
      onClick={() => setFlipped(!flipped)}
    >
      <div className="flashcard-icon">
        <img src={icon} alt="icon" />
      </div>
      <div className="flashcard-text">
        <h3>{flipped ? back : front}</h3>
      </div>
    </div>
  );
}
