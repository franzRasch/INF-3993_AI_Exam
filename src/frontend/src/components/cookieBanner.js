import React, { useState } from 'react';
import '../css/cookieBanner.css';

export default function CookieBanner() {
  const [visible, setVisible] = useState(true);
  if (!visible) return null;

  return (
    <div className="cookie-banner">
      <p>Wij gebruiken Google Analytics om ons dataverkeer te analyseren.</p>
      <div className="cookie-buttons">
        <button onClick={() => setVisible(false)}>WEIGEREN</button>
        <button onClick={() => setVisible(false)}>ACCEPTEREN</button>
      </div>
    </div>
  );
}
