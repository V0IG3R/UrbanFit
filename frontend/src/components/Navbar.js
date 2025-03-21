import React from 'react';
import { Link } from 'react-router-dom';
import '../styles/Navbar.css';

const NavBar = () => {
  return (
    <nav className="navbar">
      <div className="nav-logo">
        <Link to="/" className="nav-logo-link">UrbanFit</Link>
      </div>
      <ul className="nav-links">
        <li>
          <Link to="/" className="nav-link">Home</Link>
        </li>
        <li>
          <Link to="/user-details" className="nav-link">User Details</Link>
        </li>
      </ul>
    </nav>
  );
};

export default NavBar;
