import React, { useState } from 'react';

export default function FlashcardsPage() {
  const [number, setNumber] = useState('');
  const [response, setResponse] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async e => {
    e.preventDefault();
    setResponse('');
    setLoading(true);

    const res = await fetch('http://localhost:8000/flashcards/create', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ user_input: number }),
    });

    if (!res.ok) {
      setResponse('Error from server.');
      setLoading(false);
      return;
    }

    const reader = res.body.getReader();
    const decoder = new TextDecoder();

    let fullText = '';
    while (true) {
      const { value, done } = await reader.read();
      if (done) break;

      const chunk = decoder.decode(value, { stream: true });
      const lines = chunk.split('\n').filter(Boolean);

      for (const line of lines) {
        const data = JSON.parse(line);
        if (data.stream) {
          fullText += data.stream;
          setResponse(prev => prev + data.stream);
        }
      }
    }

    setLoading(false);
  };

  return (
    <div style={{ padding: '2rem' }}>
      <h1>Flashcards Generator</h1>
      <form onSubmit={handleSubmit}>
        <label>
          Enter a number:
          <input
            type="number"
            value={number}
            onChange={e => setNumber(e.target.value)}
            required
            style={{ marginLeft: '1rem' }}
          />
        </label>
        <button type="submit" style={{ marginLeft: '1rem' }}>
          Submit
        </button>
      </form>

      {loading && <p>Loading...</p>}

      {response && (
        <div style={{ marginTop: '2rem', whiteSpace: 'pre-wrap' }}>
          <strong>Response:</strong>
          <p>{response}</p>
        </div>
      )}
    </div>
  );
}
