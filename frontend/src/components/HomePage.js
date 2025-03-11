import React from 'react';
import { Link } from 'react-router-dom';
import '../styles/HomePage.css';

const exercises = [
  { name: "Bicep Curls", path: "bicep_curls" },
  { name: "Deadlifts", path: "deadlifts" },
  { name: "Lunges", path: "lunges" },
  { name: "Pushups", path: "pushups" },
  { name: "Situps", path: "situps" },
  { name: "Squats", path: "squats" }
];

const HomePage = () => {
  return (
    <div className="home-container">
      <h2>Choose Your Exercise</h2>
      <div className="exercise-buttons">
        {exercises.map((exercise) => (
          <Link key={exercise.path} to={`/exercise/${exercise.path}`}>
            <button className="exercise-button">{exercise.name}</button>
          </Link>
        ))}
      </div>
    </div>
  );
};

export default HomePage;
