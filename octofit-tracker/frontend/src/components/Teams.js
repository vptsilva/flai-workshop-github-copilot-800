import React, { useState, useEffect } from 'react';

const CODESPACE_NAME = process.env.REACT_APP_CODESPACE_NAME;
const API_URL = CODESPACE_NAME
  ? `https://${CODESPACE_NAME}-8000.app.github.dev/api/teams/`
  : 'http://localhost:8000/api/teams/';

const USERS_API_URL = CODESPACE_NAME
  ? `https://${CODESPACE_NAME}-8000.app.github.dev/api/users/`
  : 'http://localhost:8000/api/users/';

function Teams() {
  const [teams, setTeams] = useState([]);
  const [memberCounts, setMemberCounts] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    console.log('Teams: fetching from', API_URL);
    console.log('Teams: fetching users from', USERS_API_URL);

    Promise.all([
      fetch(API_URL).then((res) => {
        if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);
        return res.json();
      }),
      fetch(USERS_API_URL).then((res) => {
        if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);
        return res.json();
      }),
    ])
      .then(([teamsData, usersData]) => {
        console.log('Teams: fetched teams', teamsData);
        console.log('Teams: fetched users', usersData);

        const teamItems = Array.isArray(teamsData) ? teamsData : teamsData.results || [];
        const userItems = Array.isArray(usersData) ? usersData : usersData.results || [];

        // Count members per team_id
        const counts = {};
        userItems.forEach((user) => {
          if (user.team_id) {
            counts[user.team_id] = (counts[user.team_id] || 0) + 1;
          }
        });

        setTeams(teamItems);
        setMemberCounts(counts);
        setLoading(false);
      })
      .catch((err) => {
        console.error('Teams: fetch error', err);
        setError(err.message);
        setLoading(false);
      });
  }, []);

  if (loading) return <div className="container mt-4"><p>Loading teams...</p></div>;
  if (error) return <div className="container mt-4"><p className="text-danger">Error: {error}</p></div>;

  return (
    <div className="container mt-4">
      <h2>Teams</h2>
      {teams.length === 0 ? (
        <p>No teams found.</p>
      ) : (
        <table className="table table-striped table-bordered">
          <thead className="table-dark">
            <tr>
              <th>Name</th>
              <th>Description</th>
              <th>Members</th>
              <th>Created At</th>
            </tr>
          </thead>
          <tbody>
            {teams.map((team) => (
              <tr key={team.id}>
                <td>{team.name}</td>
                <td>{team.description || 'N/A'}</td>
                <td>{memberCounts[team.id] || 0}</td>
                <td>{new Date(team.created_at).toLocaleDateString()}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}

export default Teams;
