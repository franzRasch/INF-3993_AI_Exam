import React from 'react';
import '../css/hero.css';
import heroImage from '../assets/doodles/27.svg';
import hero from '../assets/hero2.svg';

// const Hero = () => (
// <section className="hero">
//   <div className="hero-content">

//     <h1>
//       LET'S CHANGE
//       <br />
//       <strong>AI supported learning</strong>
//     </h1>
//     <img src={heroImage} alt="Hero illustration" className="hero-img" />
//     <p className="subtitle">A project from INF-3993</p>
//   </div>
// </section>
// );

// export default Hero;

export default function Hero() {
  return (
    <section className="hero">
      <div className="hero-content">
        <img src={hero} alt="Hero illustration" className="hero-img" />
        <h1>
          LET'S CHANGE
          <br />
          <strong>AI supported learning</strong>
        </h1>

        <p className="subtitle">A project from INF-3993</p>
      </div>
    </section>
  );
}
