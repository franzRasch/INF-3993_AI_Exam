import React from 'react';
import { useNavigate } from 'react-router-dom';
import '../css/card.css';

export default function ServiceCard({ titleTop, titleBottom, image, color, highlightColor, route }) {
  const navigate = useNavigate();

  return (
    <div className="service-card" onClick={() => navigate(route)} style={{ cursor: 'pointer' }}>
      <div className="card-image" style={{ backgroundColor: color }}>
        <img src={image} alt={`${titleTop} ${titleBottom}`} />
      </div>
      <div className="card-text">
        <h3>
          {titleTop}
          <br />
          <span style={{ backgroundColor: highlightColor }}>{titleBottom}</span>
        </h3>
      </div>
    </div>
  );
}
