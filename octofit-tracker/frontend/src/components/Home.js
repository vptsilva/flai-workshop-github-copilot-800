import React from 'react';
import { Link } from 'react-router-dom';

function Home() {
  return (
    <div className="container mt-5">
      <div className="text-center mb-5">
        <h1 className="display-4 fw-bold">Welcome to OctoFit Tracker</h1>
        <p className="lead text-muted">
          Your superhero fitness companion — track activities, compete on the leaderboard, and manage your team.
        </p>
      </div>
      <div className="row row-cols-1 row-cols-md-3 g-4">
        <div className="col">
          <div className="card h-100 text-center">
            <div className="card-body">
              <h5 className="card-title">Users</h5>
              <p className="card-text">View and manage hero profiles.</p>
              <Link to="/users" className="btn btn-dark">Go to Users</Link>
            </div>
          </div>
        </div>
        <div className="col">
          <div className="card h-100 text-center">
            <div className="card-body">
              <h5 className="card-title">Teams</h5>
              <p className="card-text">See team rosters and member counts.</p>
              <Link to="/teams" className="btn btn-dark">Go to Teams</Link>
            </div>
          </div>
        </div>
        <div className="col">
          <div className="card h-100 text-center">
            <div className="card-body">
              <h5 className="card-title">Activities</h5>
              <p className="card-text">Browse logged fitness activities.</p>
              <Link to="/activities" className="btn btn-dark">Go to Activities</Link>
            </div>
          </div>
        </div>
        <div className="col">
          <div className="card h-100 text-center">
            <div className="card-body">
              <h5 className="card-title">Leaderboard</h5>
              <p className="card-text">Check the rankings and top performers.</p>
              <Link to="/leaderboard" className="btn btn-dark">Go to Leaderboard</Link>
            </div>
          </div>
        </div>
        <div className="col">
          <div className="card h-100 text-center">
            <div className="card-body">
              <h5 className="card-title">Workouts</h5>
              <p className="card-text">Explore personalised workout suggestions.</p>
              <Link to="/workouts" className="btn btn-dark">Go to Workouts</Link>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Home;
