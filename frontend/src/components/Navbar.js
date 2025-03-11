import React from 'react';
import { Link } from 'react-router-dom';
import '../styles/Navbar.css';

const Navbar = () => {
  return (
    <nav className="navbar">
      <h1>UrbanFit</h1>
      <ul className="nav-links">
        <li><Link to="/">Home</Link></li>
      </ul>
    </nav>
  );
};

export default Navbar;
