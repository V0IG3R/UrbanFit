// frontend/src/App.js
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import NavBar from './components/Navbar';
import HomePage from './components/HomePage';
import SetupExercise from './components/SetupExercise';
import ExercisePage from './components/ExercisePage';
import UserDetails from './components/UserDetails';
import './styles/App.css';

function App() {
  return (
    <Router>
      <NavBar />
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/setup/:exerciseName" element={<SetupExercise />} />
        <Route path="/exercise/:exerciseName" element={<ExercisePage />} />
        <Route path="/user-details" element={<UserDetails />} />
      </Routes>
    </Router>
  );
}

export default App;
