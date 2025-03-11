import React from 'react';

const DisplayScreen = () => {
  // Set the video stream endpoint from your backend.
  // Change 'deadlifts' to the desired exercise endpoint if needed.
  const videoUrl = "http://localhost:8000/video/deadlifts";

  return (
    <div
      style={{
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        height: "100vh",
        backgroundColor: "#000",
      }}
    >
      <img
        src={videoUrl}
        alt="Live Video Stream"
        style={{ maxWidth: "100%", maxHeight: "100%" }}
      />
    </div>
  );
};

export default DisplayScreen;
