import React from 'react';
import ServiceCard from './card.js';
import '../css/services.css';

import flashcardsImg from '../assets/doodles/15.svg';
import questionsImg from '../assets/doodles/12.svg';
import procrastinationImg from '../assets/doodles/16.svg';

export default function ServicesSection() {
  const services = [
    {
      titleTop: 'Create',
      titleBottom: 'Flashcards',
      image: flashcardsImg,
      color: '#C4F4F8',
      highlightColor: '#A0EBF4',
      route: '/flashcards',
    },
    {
      titleTop: 'Ask',
      titleBottom: 'Questions',
      image: questionsImg,
      color: '#F9D8D8',
      highlightColor: '#F4BFC2',
      route: '/questions',
    },
    {
      titleTop: 'Procrastination',
      titleBottom: 'Station',
      image: procrastinationImg,
      color: '#FFF495',
      highlightColor: '#FFE850',
      route: '/procrastination',
    },
  ];

  return (
    <section>
      <h2>
        <span className="highlight">Services</span>
      </h2>
      <div className="card-container">
        {services.map(service => (
          <ServiceCard key={service.route} {...service} />
        ))}
      </div>
    </section>
  );
}
