import React from 'react';
import '../css/backgroundVideo.css';

const BackgroundVideo = () => {
  return (
    <video autoPlay muted loop playsInline className="absolute top-0 left-0 w-full h-full object-cover z-0">
      <source src="/videos/bg.mp4" type="video/mp4" />
    </video>
  );
};

export default BackgroundVideo;
