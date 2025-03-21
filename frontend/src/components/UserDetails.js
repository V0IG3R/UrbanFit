import React, { useState } from 'react';
import '../styles/UserDetails.css';

const UserDetails = () => {
  const [userInfo, setUserInfo] = useState({
    name: "",
    age: "",
    height: "",
    weight: "",
    goalWeight: "",
    fitnessGoal: ""
  });

  const [submitted, setSubmitted] = useState(false);

  const handleChange = (e) => {
    setUserInfo({
      ...userInfo,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    setSubmitted(true);
  };

  return (
    <div className="user-details-container">
      <h2 className="user-details-title">Enter Your Details</h2>
      <form onSubmit={handleSubmit} className="user-details-form">
        <div className="form-row">
          <label>
            Name:
            <input 
              type="text" 
              name="name" 
              value={userInfo.name} 
              onChange={handleChange} 
              required 
            />
          </label>
          <label>
            Age:
            <input 
              type="number" 
              name="age" 
              value={userInfo.age} 
              onChange={handleChange} 
              required 
            />
          </label>
        </div>
        <div className="form-row">
          <label>
            Height (cm):
            <input 
              type="number" 
              name="height" 
              value={userInfo.height} 
              onChange={handleChange} 
              required 
            />
          </label>
          <label>
            Weight (kg):
            <input 
              type="number" 
              name="weight" 
              value={userInfo.weight} 
              onChange={handleChange} 
              required 
            />
          </label>
        </div>
        <div className="form-row">
          <label>
            Goal Weight (kg):
            <input 
              type="number" 
              name="goalWeight" 
              value={userInfo.goalWeight} 
              onChange={handleChange} 
              required 
            />
          </label>
          <label>
            Fitness Goal:
            <input 
              type="text" 
              name="fitnessGoal" 
              value={userInfo.fitnessGoal} 
              onChange={handleChange} 
              required 
            />
          </label>
        </div>
        <button type="submit" className="user-details-button">Submit Details</button>
      </form>

      {submitted && (
        <div className="user-details-table-container">
          <h3>Your Details</h3>
          <table className="user-details-table">
            <thead>
              <tr>
                <th>Name</th>
                <th>Age</th>
                <th>Height (cm)</th>
                <th>Weight (kg)</th>
                <th>Goal Weight (kg)</th>
                <th>Fitness Goal</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>{userInfo.name}</td>
                <td>{userInfo.age}</td>
                <td>{userInfo.height}</td>
                <td>{userInfo.weight}</td>
                <td>{userInfo.goalWeight}</td>
                <td>{userInfo.fitnessGoal}</td>
              </tr>
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};

export default UserDetails;
