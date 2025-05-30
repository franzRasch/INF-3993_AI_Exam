import React, { useState, useRef, useEffect } from 'react';
import '../css/QuestionsPage.css';
import userIcon from '../assets/doodles/chatUser.svg';
import botIcon from '../assets/doodles/chatBot.svg';

export default function QuestionsPage() {
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [isTyping, setIsTyping] = useState(false);
  const chatEndRef = useRef(null);

  useEffect(() => {
    if (chatEndRef.current) {
      chatEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [messages]);

  const handleSubmit = async () => {
    if (!input.trim()) return;

    const userMessage = { sender: 'user', text: input };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setLoading(true);
    setIsTyping(true);

    try {
      const response = await fetch('http://localhost:8000/chat/stream', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user_input: input }),
      });

      if (!response.ok || !response.body) {
        throw new Error('Failed to get response');
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder('utf-8');
      let buffer = '';
      let botText = '';
      let done = false;
      let firstChunkReceived = false;

      while (!done) {
        const { value, done: readerDone } = await reader.read();
        done = readerDone;

        buffer += decoder.decode(value || new Uint8Array(), { stream: true });
        const lines = buffer.split('\n');
        buffer = lines.pop(); // Hold onto incomplete line

        for (const line of lines) {
          if (!line.trim()) continue;
          try {
            const json = JSON.parse(line);
            if (json.chunk) {
              if (!firstChunkReceived) {
                setIsTyping(false); // Immediately hide the typing indicator
                firstChunkReceived = true;
              }

              botText += json.chunk;
              setMessages(prev => [
                ...prev.filter(m => !(m.sender === 'bot' && m.temp)),
                { sender: 'bot', text: botText, temp: true },
              ]);
            }
          } catch (err) {
            console.warn('Error parsing stream chunk:', err.message);
          }
        }
      }

      // Final bot message after stream ends
      setMessages(prev => [...prev.filter(m => !(m.sender === 'bot' && m.temp)), { sender: 'bot', text: botText }]);
    } catch (err) {
      console.error('Error during fetch:', err.message);
    } finally {
      setLoading(false);
      setIsTyping(false);
    }
  };

  return (
    <div className="questions-page">
      <h1>Ask me a question</h1>

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

        {isTyping && (
          <div className="chat-row bot">
            <img src={botIcon} alt="bot avatar" className="chat-avatar" />
            <div className="chat-message bot typing-indicator">Bot is typing...</div>
          </div>
        )}
        <div ref={chatEndRef} />
      </div>

      <div className="chat-input-group">
        <input
          type="text"
          placeholder="Ask me anything..."
          value={input}
          onChange={e => setInput(e.target.value)}
          onKeyDown={e => e.key === 'Enter' && handleSubmit()}
        />
        <button onClick={handleSubmit} disabled={loading}>
          Send
        </button>
      </div>
    </div>
  );
}
