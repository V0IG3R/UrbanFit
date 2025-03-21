import React, { useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import '../styles/SetupExercise.css';

const SetupExercise = () => {
  const navigate = useNavigate();
  const { exerciseName } = useParams();
  const [sets, setSets] = useState(3);
  const [reps, setReps] = useState(10);
  const [restTime, setRestTime] = useState(60);

  const handleSubmit = (e) => {
    e.preventDefault();
    navigate(`/exercise/${exerciseName}`, {
      state: { sets: Number(sets), reps: Number(reps), restTime: Number(restTime) }
    });
  };

  return (
    <div className="setup-exercise-container">
      <div className="setup-exercise-card">
        <h2 className="setup-title">Setup Your Workout</h2>
        <h3 className="exercise-title">{exerciseName.replace("_", " ")}</h3>
        <form onSubmit={handleSubmit} className="setup-form">
          <label className="setup-label">
            Number of Sets:
            <input
              type="number"
              value={sets}
              onChange={(e) => setSets(e.target.value)}
              min="1"
              className="setup-input"
            />
          </label>
          <label className="setup-label">
            Reps per Set:
            <input
              type="number"
              value={reps}
              onChange={(e) => setReps(e.target.value)}
              min="1"
              className="setup-input"
            />
          </label>
          <label className="setup-label">
            Rest Time (sec):
            <input
              type="number"
              value={restTime}
              onChange={(e) => setRestTime(e.target.value)}
              min="0"
              className="setup-input"
            />
          </label>
          <button type="submit" className="setup-button">Start Exercise</button>
        </form>
      </div>
    </div>
  );
};

export default SetupExercise;
