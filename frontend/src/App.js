import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import HomePage from './components/HomePage';
import ExercisePage from './components/ExercisePage';
import './styles/App.css';

function App() {
  return (
    <Router>
      <Navbar />
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/exercise/:exerciseName" element={<ExercisePage />} />
      </Routes>
    </Router>
  );
}

export default App;
