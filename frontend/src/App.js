import React, { useState, useEffect } from 'react';
import FoodSearch from './components/FoodSearch';
import './App.css';

function App() {
  const [summary, setSummary] = useState([]);
  const [loggedFoods, setLoggedFoods] = useState([]);

  const fetchSummary = async () => {
    const response = await fetch('/api/summary');
    const data = await response.json();
    setSummary(data);
  };

  const fetchLogHistory = async () => {
    try {
      const response = await fetch('/api/log-history');
      const data = await response.json();
      setLoggedFoods(Array.isArray(data) ? data : []);
    } catch (err) {
      setLoggedFoods([]);
    }
  };

  const handleLog = async () => {
    await fetchSummary();
    await fetchLogHistory();
  };

  const handleReset = async () => {
    await fetch('/api/clear-log', { method: 'DELETE' });
    await fetchSummary();
    await fetchLogHistory();
  };

  useEffect(() => {
    fetchSummary();
    fetchLogHistory();
  }, []);

  return (
    <div className="container">
      <h1>Micronutrient Tracker</h1>

      <div className="search-section">
        <FoodSearch onLog={handleLog} />
      </div>

      <div className="summary-section">
        <h2>Daily Summary</h2>
        <table className="summary-table">
          <thead>
            <tr>
              <th>Nutrient</th>
              <th>Amount</th>
              <th>Unit</th>
              <th>RDA</th>
            </tr>
          </thead>
          <tbody>
            {summary.map((item) => (
              <tr key={item.id}>
                <td>{item.name}</td>
                <td>{item.total}</td>
                <td>{item.unit}</td>
                <td>{item.rda || '—'}</td>
              </tr>
            ))}
          </tbody>
        </table>
        <button onClick={handleReset}>Reset Daily Totals</button>
      </div>

      <div className="log-history-section">
        <h2>Foods Logged Today</h2>
        <ul>
          {loggedFoods.map((entry, index) => (
            <li key={index}>
              {entry.name} – {entry.amount}g
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}

export default App;