import { useState } from "react";
import FoodSearch from './components/FoodSearch.jsx';
import config from './config';

function App() {
  const [summary, setSummary] = useState([]);

  const fetchSummary = async () => {
    const res = await fetch(`${config.BASE_URL}/summary`);
    const data = await res.json();
    setSummary(data);
  };

  return (
    <div>
      <h1>Micros Tracker</h1>
      <FoodSearch onFoodSelect={(food) => console.log("Selected:", food)} />
      <button onClick={fetchSummary}>Get Summary</button>
      <ul>
        {summary.map((n) => (
          <li key={n.id}>
            {n.name}: {n.total} {n.unit} / {n.rda} {n.unit}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;