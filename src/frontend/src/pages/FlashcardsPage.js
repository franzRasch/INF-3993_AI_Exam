import React, { useState, useRef } from 'react';
import '../css/FlashcardsPage.css';
import { FaVolumeUp, FaMicrophone, FaSyncAlt } from 'react-icons/fa';

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

export default function FlashcardsPage() {
  const [userInput, setUserInput] = useState('');
  const [flashcards, setFlashcards] = useState([
    { front: 'Test Question', back: 'Test Answer' }, // 🧪 Initial test card
  ]);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    console.log('Clicked submit');
    setLoading(true); // Show loading spinner

    try {
      const response = await fetch('http://localhost:8000/flashcards/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ user_input: userInput }),
      });

      if (!response.ok) {
        throw new Error('Failed to fetch flashcards');
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder('utf-8');
      let buffer = '';
      const flashcardsList = [];
      let currentCard = {};

      while (true) {
        const { value, done } = await reader.read();
        if (done) break;
        buffer += decoder.decode(value);

        // Split completed lines
        const lines = buffer.split('\n');
        buffer = lines.pop(); // hold onto incomplete line for next chunk

        for (const line of lines) {
          if (!line.trim()) continue;

          try {
            const parsed = JSON.parse(line);

            if (parsed.q) {
              const qObj = JSON.parse(parsed.q);
              currentCard.front = qObj.question;
            }

            if (parsed.a) {
              const aObj = JSON.parse(parsed.a);
              currentCard.back = aObj.answer;
            }

            if (currentCard.front && currentCard.back) {
              flashcardsList.push({ ...currentCard });
              currentCard = {};
            }
          } catch (err) {
            console.warn('Failed to parse line:', line, err.message);
          }
        }
      }

      // Handle final buffer line
      if (buffer.trim()) {
        try {
          const parsed = JSON.parse(buffer);
          if (parsed.q) currentCard.front = JSON.parse(parsed.q).question;
          if (parsed.a) currentCard.back = JSON.parse(parsed.a).answer;
          if (currentCard.front && currentCard.back) {
            flashcardsList.push({ ...currentCard });
          }
        } catch (err) {
          console.warn('Failed to parse final buffer:', buffer, err.message);
        }
      }

      setFlashcards(flashcardsList);
      console.log('Parsed flashcards:', flashcardsList);
    } catch (err) {
      console.error('Error:', err.message);
    } finally {
      setLoading(false); // Hide loading spinner
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
        {loading ? (
          <div className="loading-spinner">Loading...</div>
        ) : flashcards.length === 0 ? (
          <p>No flashcards yet. Try entering a number and pressing Enter.</p>
        ) : (
          flashcards.map((card, index) => {
            const icon = iconSet[index % iconSet.length];
            const { base, highlight } = colorSet[index % colorSet.length];
            return (
              <Flashcard
                key={index}
                front={card.front}
                back={card.back}
                color={base}
                highlight={highlight}
                icon={icon}
              />
            );
          })
        )}
      </div>
    </div>
  );
}


function Flashcard({ front, back, color, highlight, icon }) {
  const [flipped, setFlipped] = useState(false);
  const audioRef = useRef(null);

  const handleTTS = async () => {
    const text = flipped ? back : front;
    try {
      const response = await fetch('http://localhost:8000/tts/text-to-speech', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text }),
      });

      if (!response.ok) {
        throw new Error('Failed to fetch audio');
      }

      const audioBlob = await response.blob();
      const audioUrl = URL.createObjectURL(audioBlob);

      if (audioRef.current) {
        audioRef.current.src = audioUrl;
        audioRef.current.play();
      }
    } catch (error) {
      console.error('Error playing audio:', error);
    }
  };

  const handleSpeechInput = () => {
    const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    recognition.onresult = event => {
      const spokenText = event.results[0][0].transcript;
      alert(`You said: ${spokenText}`);
    };
    recognition.start();
  };

  return (
    <div
      className={`flashcard-box ${flipped ? 'flipped' : ''}`}
      style={{ backgroundColor: flipped ? highlight : color }}
    >
      <button className="flip-button" onClick={() => setFlipped(!flipped)} title="Flip">
        <FaSyncAlt />
      </button>

      <div className="flashcard-icon">
        <img src={icon} alt="icon" />
      </div>

      <div className="flashcard-text">
        <h3>{flipped ? back : front}</h3>
      </div>

      <div className="flashcard-buttons-bottom">
        <button onClick={handleTTS} title="Play Audio">
          <FaVolumeUp />
        </button>
        <button onClick={handleSpeechInput} title="Answer with Speech">
          <FaMicrophone />
        </button>
      </div>

      <audio ref={audioRef} hidden />
    </div>
  );
}


