import { useState } from 'react';
import axios from 'axios';

const GamePage = () => {
  const [userMove, setUserMove] = useState(null);
  const [aiMove, setAiMove] = useState(null);
  const [result, setResult] = useState(null);

  const moves = ['rock', 'paper', 'scissors'];

  const playMove = async move => {
    try {
      const res = await axios.post('http://localhost:8000/play', {
        user_move: move,
      });
      setUserMove(res.data.user_move);
      setAiMove(res.data.ai_move);
      setResult(res.data.result);
    } catch (error) {
      console.error('Error playing move:', error);
    }
  };

  return (
    <div style={{ textAlign: 'center', paddingTop: '50px' }}>
      <h1>Rock Paper Scissors</h1>
      <div>
        {moves.map(move => (
          <button key={move} onClick={() => playMove(move)} style={{ margin: '10px', padding: '10px 20px' }}>
            {move.charAt(0).toUpperCase() + move.slice(1)}
          </button>
        ))}
      </div>
      {result && (
        <div style={{ marginTop: '30px' }}>
          <h2>You chose: {userMove}</h2>
          <h2>AI chose: {aiMove}</h2>
          <h2>Result: {result.toUpperCase()}</h2>
        </div>
      )}
    </div>
  );
};

export default GamePage;
