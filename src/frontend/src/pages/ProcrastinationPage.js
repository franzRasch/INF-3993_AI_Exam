import React from 'react';
import RockPaperScissors from '../components/rps';

export default function ProcrastinationPage() {
  return (
    <div style={{ padding: '2rem' }}>
      <h1>Procrastination</h1>
      <p>Procrastinate here!</p>

      <RockPaperScissors />
    </div>
  );
}
