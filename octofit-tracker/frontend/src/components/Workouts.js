import React, { useState, useEffect } from 'react';

const CODESPACE_NAME = process.env.REACT_APP_CODESPACE_NAME;
const API_URL = CODESPACE_NAME
  ? `https://${CODESPACE_NAME}-8000.app.github.dev/api/workouts/`
  : 'http://localhost:8000/api/workouts/';

function Workouts() {
  const [workouts, setWorkouts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    console.log('Workouts: fetching from', API_URL);
    fetch(API_URL)
      .then((res) => {
        if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);
        return res.json();
      })
      .then((data) => {
        console.log('Workouts: fetched data', data);
        const items = Array.isArray(data) ? data : data.results || [];
        setWorkouts(items);
        setLoading(false);
      })
      .catch((err) => {
        console.error('Workouts: fetch error', err);
        setError(err.message);
        setLoading(false);
      });
  }, []);

  if (loading) return <div className="container mt-4"><p>Loading workouts...</p></div>;
  if (error) return <div className="container mt-4"><p className="text-danger">Error: {error}</p></div>;

  return (
    <div className="container mt-4">
      <h2>Workouts</h2>
      {workouts.length === 0 ? (
        <p>No workouts found.</p>
      ) : (
        <div className="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4">
          {workouts.map((workout) => (
            <div className="col" key={workout.id}>
              <div className="card h-100">
                <div className="card-header bg-dark text-white">
                  <strong>{workout.name}</strong>
                </div>
                <div className="card-body">
                  <p className="card-text">{workout.description}</p>
                  <ul className="list-group list-group-flush">
                    <li className="list-group-item"><strong>Activity Type:</strong> {workout.activity_type}</li>
                    <li className="list-group-item"><strong>Difficulty:</strong> {workout.difficulty}</li>
                    <li className="list-group-item"><strong>Duration:</strong> {workout.duration} min</li>
                    <li className="list-group-item"><strong>Est. Calories:</strong> {workout.calories_estimate}</li>
                  </ul>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default Workouts;
