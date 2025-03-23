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
  
  // Original rep counter state.
  const [repData, setRepData] = useState({
    counter: 0,
    stage: 'up',
    feedback: 'N/A',
    lightingStatus: 'N/A'
  });
  
  // Workout flow states.
  const totalSets = 3; // Total number of sets
  const repsGoal = 10; // Target reps per set
  const [currentSet, setCurrentSet] = useState(1);

  // Fine-tuning parameters.
  const BRIGHTNESS_THRESHOLD = 80;
  const CONTROLLED_MOVEMENT_THRESHOLD = 0.03;
  const VISIBILITY_THRESHOLD = 0.5;
  const REQUIRED_VISIBLE_RATIO = 0.75;

  // Ref to store previous landmarks.
  const prevLandmarksRef = useRef(null);

  // Helper: compute average brightness.
  const getAverageBrightness = (video) => {
    const tempCanvas = document.createElement('canvas');
    tempCanvas.width = video.videoWidth || video.width;
    tempCanvas.height = video.videoHeight || video.height;
    const tempCtx = tempCanvas.getContext('2d');
    tempCtx.drawImage(video, 0, 0, tempCanvas.width, tempCanvas.height);
    const imageData = tempCtx.getImageData(0, 0, tempCanvas.width, tempCanvas.height);
    const data = imageData.data;
    let totalBrightness = 0;
    const count = data.length / 4;
    for (let i = 0; i < data.length; i += 4) {
      const brightness = 0.2126 * data[i] + 0.7152 * data[i + 1] + 0.0722 * data[i + 2];
      totalBrightness += brightness;
    }
    return totalBrightness / count;
  };

  // Monitor rep count; when the target is reached, update the set and reset the counter.
  useEffect(() => {
    const currentCount = repData.counter || repData.repCount || 0;
    if (currentCount >= repsGoal) {
      setCurrentSet(prev => prev + 1);
      // Reset counter for next set.
      setRepData(prev => ({ ...prev, counter: 0 }));
    }
  }, [repData, repsGoal]);

  useEffect(() => {
    // Reset rep data and previous landmarks on mount.
    setRepData({
      counter: 0,
      stage: 'up',
      feedback: 'N/A',
      lightingStatus: 'N/A'
    });
    prevLandmarksRef.current = null;

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
      minDetectionConfidence: 0.6,
      minTrackingConfidence: 0.6
    });
    
    pose.onResults((results) => {
      if (!canvasRef.current) return;
      canvasCtx.save();
      canvasCtx.clearRect(0, 0, canvasElement.width, canvasElement.height);
      canvasCtx.drawImage(results.image, 0, 0, canvasElement.width, canvasElement.height);

      // Draw pose skeleton.
      if (results.poseLandmarks) {
        drawConnectors(canvasCtx, results.poseLandmarks, POSE_CONNECTIONS, { color: '#00FF00', lineWidth: 2 });
        drawLandmarks(canvasCtx, results.poseLandmarks, { color: '#FF0000', lineWidth: 1 });
      }
      canvasCtx.restore();

      if (results.poseLandmarks) {
        // Check landmark visibility.
        const totalLandmarks = results.poseLandmarks.length;
        const visibleCount = results.poseLandmarks.filter(lm => lm.visibility >= VISIBILITY_THRESHOLD).length;
        if (visibleCount / totalLandmarks < REQUIRED_VISIBLE_RATIO) {
          setRepData(prev => ({
            ...prev,
            feedback: "Pose unstable: Not enough landmarks visible. Adjust your position."
          }));
          return;
        }
        
        // Ensure controlled movement.
        if (prevLandmarksRef.current) {
          const fastMovement = results.poseLandmarks.some((lm, index) => {
            const prevLm = prevLandmarksRef.current[index];
            if (!prevLm) return false;
            const dx = lm.x - prevLm.x;
            const dy = lm.y - prevLm.y;
            const displacement = Math.sqrt(dx * dx + dy * dy);
            return displacement > CONTROLLED_MOVEMENT_THRESHOLD;
          });
          
          if (fastMovement) {
            setRepData(prev => ({
              ...prev,
              feedback: "Movement too fast. Please move slowly and controlled."
            }));
            prevLandmarksRef.current = results.poseLandmarks;
            return; // Skip sending data to backend.
          }
        }
        
        // Update previous landmarks.
        prevLandmarksRef.current = results.poseLandmarks;

        // Send landmark data to backend for rep counting.
        fetch(`http://localhost:8000/landmarks/${exerciseName}`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ landmarks: results.poseLandmarks })
        })
          .then((res) => res.json())
          .then((data) => {
            // Preserve original logic: backend should return counter, repState, etc.
            setRepData(data);
          })
          .catch((err) => console.error(err));
      }
    });
    
    const camera = new Camera(videoRef.current, {
      onFrame: async () => {
        const brightness = getAverageBrightness(videoRef.current);
        if (brightness < BRIGHTNESS_THRESHOLD) {
          setRepData(prev => ({
            ...prev,
            lightingStatus: "Too Dark",
            feedback: "Lighting is too dark. Please improve your lighting."
          }));
          canvasCtx.clearRect(0, 0, canvasElement.width, canvasElement.height);
          return;
        } else {
          setRepData(prev => ({ ...prev, lightingStatus: "Good" }));
          await pose.send({ image: videoRef.current });
        }
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
    // Reset state on navigation.
    setRepData({
      counter: 0,
      stage: 'up',
      feedback: 'N/A',
      lightingStatus: 'N/A'
    });
    prevLandmarksRef.current = null;
    navigate("/");
  };

  return (
    <div className="exercise-page" style={{ backgroundImage: `url(/assets/gifs/${exerciseName}.gif)` }}>
      <header className="exercise-header">
        <h1>{exerciseName.replace("_", " ").toUpperCase()}</h1>
        <button onClick={handleBack} className="back-home">← Back to Home</button>
      </header>
      
      <div className="video-container">
        <video ref={videoRef} style={{ display: 'none' }} />
        <canvas ref={canvasRef} width={640} height={480} />
      </div>
      
      <div className="stats-container">
        <div className="stat-box">
          <h3>Rep Counter</h3>
          <p>{repData.counter || repData.repCount || 0}</p>
        </div>
        <div className="stat-box">
          <h3>Stage</h3>
          <p>{repData.repState || repData.stage}</p>
        </div>
        <div className="stat-box">
          <h3>Feedback</h3>
          <p>{repData.feedback}</p>
        </div>
        <div className="stat-box">
          <h3>Lighting</h3>
          <p>{repData.lightingStatus}</p>
        </div>
        <div className="stat-box">
          <h3>Set</h3>
          <p>{currentSet} / {totalSets}</p>
        </div>
        <div className="stat-box">
          <h3>Target Reps</h3>
          <p>{repData.counter || repData.repCount || 0} / {repsGoal}</p>
        </div>
      </div>
      
    </div>
  );
};

export default ExercisePage;
