import React from 'react';
import '../styles/DisplayScreen.css';

const DisplayScreen = () => {
  // Update the videoUrl to match your backend or asset path.
  const videoUrl = "http://localhost:8000/video/deadlifts";

  return (
    <div className="display-screen">
      <video autoPlay loop muted className="full-video">
        <source src={videoUrl} type="video/mp4" />
        Your browser does not support the video tag.
      </video>
    </div>
  );
};

export default DisplayScreen;
