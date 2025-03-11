import React, { useEffect, useRef, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import '../styles/ExercisePage.css';
import { Pose, POSE_CONNECTIONS } from '@mediapipe/pose';
import { Camera } from '@mediapipe/camera_utils';
import { drawConnectors, drawLandmarks } from '@mediapipe/drawing_utils';

const ExercisePage = () => {
  const { exerciseName } = useParams();
  const navigate = useNavigate();
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const [repData, setRepData] = useState({ counter: 0, stage: 'up', feedback: 'N/A' });

  useEffect(() => {
    // Reset rep data when component mounts or exerciseName changes.
    setRepData({ counter: 0, stage: 'up', feedback: 'N/A' });
    if (!videoRef.current || !canvasRef.current) return;
    
    const canvasElement = canvasRef.current;
    const canvasCtx = canvasElement.getContext('2d');

    // Initialize MediaPipe Pose.
    const pose = new Pose({
      locateFile: (file) => `https://cdn.jsdelivr.net/npm/@mediapipe/pose/${file}`
    });
    pose.setOptions({
      modelComplexity: 1,
      smoothLandmarks: true,
      enableSegmentation: false,
      smoothSegmentation: false,
      minDetectionConfidence: 0.5,
      minTrackingConfidence: 0.5
    });
    
    pose.onResults((results) => {
      // Ensure canvas exists.
      if (!canvasRef.current) return;
      const ctx = canvasRef.current.getContext('2d');
      ctx.save();
      ctx.clearRect(0, 0, canvasElement.width, canvasElement.height);
      ctx.drawImage(results.image, 0, 0, canvasElement.width, canvasElement.height);

      // Draw skeleton: connectors and landmarks.
      if (results.poseLandmarks) {
        drawConnectors(ctx, results.poseLandmarks, POSE_CONNECTIONS, { color: '#00FF00', lineWidth: 2 });
        drawLandmarks(ctx, results.poseLandmarks, { color: '#FF0000', lineWidth: 1 });
      }
      ctx.restore();

      // Send landmark data to backend for rep counting.
      if (results.poseLandmarks) {
        fetch(`http://localhost:8000/landmarks/${exerciseName}`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ landmarks: results.poseLandmarks })
        })
          .then((res) => res.json())
          .then((data) => {
            setRepData(data);
          })
          .catch((err) => console.error(err));
      }
    });
    
    const camera = new Camera(videoRef.current, {
      onFrame: async () => {
        await pose.send({ image: videoRef.current });
      },
      width: 640,
      height: 480
    });
    camera.start();
    
    return () => {
      camera.stop();
    };
  }, [exerciseName]);

  const handleBack = () => {
    // Reset rep data and navigate back.
    setRepData({ counter: 0, stage: 'up', feedback: 'N/A' });
    navigate("/");
  };

  return (
    <div className="exercise-page">
      <header className="exercise-header">
        <h1>{exerciseName.replace("_", " ").toUpperCase()}</h1>
        <button onClick={handleBack} className="back-home">← Back to Home</button>
      </header>
      <div className="video-container">
        {/* Hidden video element for capturing the camera feed */}
        <video ref={videoRef} style={{ display: 'none' }} />
        <canvas ref={canvasRef} width={640} height={480} />
      </div>
      <div className="stats-container">
        {exerciseName === "deadlifts" ? (
          <>
            <div className="stat-box">
              <h3>Correct Reps</h3>
              <p>{repData.correctReps || 0}</p>
            </div>
            <div className="stat-box">
              <h3>Incorrect Reps</h3>
              <p>{repData.incorrectReps || 0}</p>
            </div>
            <div className="stat-box">
              <h3>Stage</h3>
              <p>{repData.repState || repData.stage}</p>
            </div>
            <div className="stat-box">
              <h3>Feedback</h3>
              <p>{repData.feedback}</p>
            </div>
          </>
        ) : (
          <>
            <div className="stat-box">
              <h3>Rep Counter</h3>
              <p>{repData.counter || repData.repCount || 0}</p>
            </div>
            <div className="stat-box">
              <h3>Stage</h3>
              <p>{repData.stage}</p>
            </div>
            <div className="stat-box">
              <h3>Posture</h3>
              <p>{repData.feedback}</p>
            </div>
          </>
        )}
      </div>
    </div>
  );
};

export default ExercisePage;
