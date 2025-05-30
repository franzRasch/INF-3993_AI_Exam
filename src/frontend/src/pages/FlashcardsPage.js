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
  const [flashcards, setFlashcards] = useState([{ front: 'What is a quorum?', back: 'Test Answer' }]);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    setLoading(true);
    try {
      const response = await fetch('http://localhost:8000/flashcards/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user_input: userInput }),
      });

      if (!response.ok) throw new Error('Failed to fetch flashcards');

      const reader = response.body.getReader();
      const decoder = new TextDecoder('utf-8');
      let buffer = '';
      const flashcardsList = [];
      let currentCard = {};

      while (true) {
        const { value, done } = await reader.read();
        if (done) break;
        buffer += decoder.decode(value);
        const lines = buffer.split('\n');
        buffer = lines.pop();

        for (const line of lines) {
          if (!line.trim()) continue;
          try {
            const parsed = JSON.parse(line);
            if (parsed.q) currentCard.front = JSON.parse(parsed.q).question;
            if (parsed.a) currentCard.back = JSON.parse(parsed.a).answer;
            if (currentCard.front && currentCard.back) {
              flashcardsList.push({ ...currentCard });
              currentCard = {};
            }
          } catch (err) {
            console.warn('Failed to parse line:', line, err.message);
          }
        }
      }

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
    } catch (err) {
      console.error('Error:', err.message);
    } finally {
      setLoading(false);
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
  const [recording, setRecording] = useState(false);
  const [evaluation, setEvaluation] = useState(null);
  const [mediaRecorder, setMediaRecorder] = useState(null);
  const [audioChunks, setAudioChunks] = useState([]);
  const [recordingError, setRecordingError] = useState(null);
  const [isProcessing, setIsProcessing] = useState(false);

  const audioRef = useRef(null);

  const handleTTS = async text => {
    if (!text?.trim()) return;
    try {
      const response = await fetch('http://localhost:8000/tts/text-to-speech', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text }),
      });

      if (!response.ok) throw new Error(`TTS failed with status ${response.status}`);
      const audioBlob = await response.blob();
      const audioUrl = URL.createObjectURL(audioBlob);

      if (audioRef.current) {
        audioRef.current.src = audioUrl;
        audioRef.current.play().catch(err => console.error('Playback error:', err));
      }
    } catch (err) {
      console.error('TTS error:', err.message || err);
    }
  };

  const handleSpeechInput = async () => {
    if (recording) {
      stopRecording();
      return;
    }

    setEvaluation(null);
    setRecordingError(null);
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const options = { mimeType: 'audio/webm;codecs=opus' };
      const recorder = new MediaRecorder(stream, options);

      const chunks = [];
      recorder.ondataavailable = e => e.data.size > 0 && chunks.push(e.data);

      recorder.onstop = async () => {
        setIsProcessing(true);
        const audioBlob = new Blob(chunks, { type: 'audio/webm' });

        if (audioBlob.size < 2048) {
          setRecordingError('Recording too short or silent. Try again.');
          setIsProcessing(false);
          return;
        }

        const formData = new FormData();
        formData.append('topic', 'advanced distributed databases');
        formData.append('question', front);
        formData.append('audio', audioBlob, 'recording.webm');

        try {
          const response = await fetch('http://localhost:8000/evaluate/oral', {
            method: 'POST',
            body: formData,
          });

          if (!response.ok) throw new Error('Evaluation failed');
          const feedback = await response.json();
          setEvaluation(feedback);
        } catch (error) {
          setRecordingError('Failed to evaluate the recording.');
          console.error(error);
        } finally {
          setIsProcessing(false);
          setRecording(false);
        }
      };

      setAudioChunks([]);
      setMediaRecorder(recorder);
      recorder.start();
      setRecording(true);
    } catch (err) {
      setRecordingError('Microphone access denied or not available.');
      console.error(err);
    }
  };

  const stopRecording = () => {
    if (mediaRecorder && recording) {
      mediaRecorder.stop();
    }
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
        <button onClick={() => handleTTS(flipped ? back : front)} title="Play Audio" disabled={isProcessing}>
          <FaVolumeUp />
        </button>

        <button onClick={handleSpeechInput} title="Answer with Speech" disabled={recording || isProcessing}>
          <FaMicrophone />
        </button>

        {recording && (
          <button onClick={stopRecording} title="Stop Recording" disabled={isProcessing}>
            {isProcessing ? 'Processing...' : 'Stop'}
          </button>
        )}
      </div>

      <audio ref={audioRef} hidden />

      {recordingError && (
        <div className="flashcard-evaluation error">
          <p>{recordingError}</p>
        </div>
      )}

      {evaluation && (
        <div className="flashcard-evaluation">
          <h4>Evaluation Feedback:</h4>
          <p>{evaluation.feedback}</p>
          {evaluation.feedback?.toLowerCase().includes('incomplete') && (
            <p className="hint">Try expanding your answer with examples or explanations.</p>
          )}
        </div>
      )}
    </div>
  );
}
