import React, { useState } from 'react';
import '../css/QuestionsPage.css';
import userIcon from '../assets/doodles/25.svg';
import botIcon from '../assets/doodles/26.svg';

export default function QuestionsPage() {
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState([]);

  const handleSubmit = async () => {
    if (!input.trim()) return;

    const userMessage = { sender: 'user', text: input };
    setMessages(prev => [...prev, userMessage]);
    setInput('');

    try {
      const response = await fetch('http://localhost:8000/questions', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question: input }),
      });

      const data = await response.json();
      const botMessage = { sender: 'bot', text: data.answer || 'No answer provided.' };

      setMessages(prev => [...prev, botMessage]);
    } catch (err) {
      console.error('Error fetching answer:', err.message);
    }
  };

  return (
    <div className="questions-page">
      <h1>Ask a Question</h1>
      <div className="chat-box">
        {messages.map((msg, index) => (
          <div key={index} className={`chat-row ${msg.sender}`}>
            <img
              src={msg.sender === 'user' ? userIcon : botIcon}
              alt={`${msg.sender} avatar`}
              className="chat-avatar"
            />
            <div className={`chat-message ${msg.sender}`}>{msg.text}</div>
          </div>
        ))}
      </div>

      <div className="chat-input-group">
        <input type="text" placeholder="Ask me anything..." value={input} onChange={e => setInput(e.target.value)} />
        <button onClick={handleSubmit}>Send</button>
      </div>
    </div>
  );
}
