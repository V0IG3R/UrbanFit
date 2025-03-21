import React, { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import '../styles/HomePage.css';

const exercises = [
  { 
    name: "Bicep Curls", 
    tagline: "Sculpt your arms", 
    path: "bicep_curls", 
    gif: "/assets/gifs/bicep_curls.gif" 
  },
  { 
    name: "Deadlifts", 
    tagline: "Power through with form", 
    path: "deadlifts", 
    gif: "/assets/gifs/deadlifts.gif" 
  },
  { 
    name: "Lunges", 
    tagline: "Strengthen your legs", 
    path: "lunges", 
    gif: "/assets/gifs/lunges.gif" 
  },
  { 
    name: "Pushups", 
    tagline: "Build upper body strength", 
    path: "pushups", 
    gif: "/assets/gifs/pushups.gif" 
  },
  { 
    name: "Situps", 
    tagline: "Engage your core", 
    path: "situps", 
    gif: "/assets/gifs/situps.gif" 
  },
  { 
    name: "Squats", 
    tagline: "Lower body power", 
    path: "squats", 
    gif: "/assets/gifs/squats.gif" 
  }
];

const HomePage = () => {
  const [scrolled, setScrolled] = useState(false);
  const navigate = useNavigate();

  // Check localStorage so we ask for user details only once.
  useEffect(() => {
    if (!localStorage.getItem('userDetailsAsked')) {
      const wantsDetails = window.confirm("Would you like to enter your user details?");
      if (wantsDetails) {
        navigate("/user-details");
      }
      localStorage.setItem('userDetailsAsked', 'true');
    }
  }, [navigate]);

  // Listen for scroll to adjust logo appearance.
  useEffect(() => {
    const handleScroll = () => {
      setScrolled(window.scrollY > 150);
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  return (
    <div className="scroll-container">
      {/* HERO SECTION */}
      <section className="hero-section">
        <div className="video-bg">
          <video autoPlay loop muted playsInline className="bg-video">
            <source src="/assets/video/bgm.mp4" type="video/mp4" />
            Your browser does not support the video tag.
          </video>
        </div>
        <div className={`logo-container ${scrolled ? 'scrolled' : ''}`}>
          <h1 className="logo-text">UrbanFit</h1>
        </div>
      </section>

      {/* EXERCISE SLIDES */}
      {exercises.map((exercise) => (
        <Link 
          key={exercise.path} 
          to={`/setup/${exercise.path}`} 
          className="exercise-slide-link"
        >
          <section 
            className="exercise-slide" 
            style={{ backgroundImage: `url(${exercise.gif})` }}
          >
            <div className="slide-overlay">
              <div className="exercise-info">
                <h2 className="exercise-name">{exercise.name}</h2>
                <p className="exercise-tagline">{exercise.tagline}</p>
              </div>
            </div>
          </section>
        </Link>
      ))}

      {/* ABOUT SECTION */}
      <section className="about-section">
        <div className="about-container">
          <h2>About the Developer</h2>
          <p>
            Developed by Debarun Joardar. Check out my GitHub:{" "}
            <a 
              href="https://www.github.com/V0IG3R" 
              target="_blank" 
              rel="noopener noreferrer"
            >
              www.github.com/V0IG3R
            </a>
          </p>
          <p className="about-tagline">
            Empowering fitness with cutting-edge technology.
          </p>
        </div>
      </section>
    </div>
  );
};

export default HomePage;
