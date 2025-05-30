import React, { useState } from 'react';
import axios from 'axios';
import '../css/rps.css';

const RockPaperScissors = () => {
  const [userMove, setUserMove] = useState(null);
  const [aiMove, setAiMove] = useState(null);
  const [result, setResult] = useState(null);
  const [isAnimating, setIsAnimating] = useState(false);

  const moves = ['rock', 'paper', 'scissors'];

  const playMove = async move => {
    setIsAnimating(true);
    setUserMove(null);
    setAiMove(null);
    setResult(null);

    try {
      const res = await axios.post('http://localhost:8000/play', {
        user_move: move,
      });

      // Simulate animation delay
      setTimeout(() => {
        setUserMove(res.data.user_move);
        setAiMove(res.data.ai_move);
        setResult(res.data.result);
        setIsAnimating(false);
      }, 2000); // 2 seconds animation
    } catch (error) {
      console.error('Error playing move:', error);
      setIsAnimating(false);
    }
  };

  const getImagePath = (side, move) => {
    try {
      return require(`../assets/rps-graphics/${side}-${move}.svg`);
    } catch (err) {
      console.warn(`Image not found: ${side}-${move}.svg`);
      return null;
    }
  };

  return (
    <div className="rps-container">
      <h2 className="rps-title">Rock Paper Scissors</h2>
      <div className="rps-buttons">
        {moves.map(move => (
          <button key={move} onClick={() => playMove(move)} className="rps-button" disabled={isAnimating}>
            {move.charAt(0).toUpperCase() + move.slice(1)}
          </button>
        ))}
      </div>
      <div className="rps-hands">
        <div className={`hand left-hand ${isAnimating ? 'shake' : ''}`}>
          {isAnimating || userMove ? (
            <img
              src={isAnimating ? getImagePath('l', 'shake') : userMove ? getImagePath('l', userMove) : null}
              alt={userMove || 'Waiting...'}
            />
          ) : null}
        </div>
        <div className={`hand right-hand ${isAnimating ? 'shake' : ''}`}>
          {isAnimating || aiMove ? (
            <img
              src={isAnimating ? getImagePath('r', 'shake') : aiMove ? getImagePath('r', aiMove) : null}
              alt={aiMove || 'Waiting...'}
            />
          ) : null}
        </div>
      </div>
      {result && (
        <div className="rps-result">
          <p>
            You chose: <strong>{userMove}</strong>
          </p>
          <p>
            AI chose: <strong>{aiMove}</strong>
          </p>
          <p>
            Result: <strong>{result.toUpperCase()}</strong>
          </p>
        </div>
      )}
    </div>
  );
};

export default RockPaperScissors;
