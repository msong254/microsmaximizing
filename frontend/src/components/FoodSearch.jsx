import { useState } from "react";
import config from '../config'; // ✅ If config.js is inside components folder

function FoodSearch({ onFoodSelect }) {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);

  const handleSearch = async () => {
    if (!query.trim()) return;
    try {
      const res = await fetch(`${config.BASE_URL}/foods/search?query=${encodeURIComponent(query)}`);
      const data = await res.json();
      setResults(data);
    } catch (err) {
      console.error("Search error:", err);
    }
  };

  return (
    <div>
      <input
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Search food"
      />
      <button onClick={handleSearch}>Search</button>
      <ul>
        {results.map((food) => (
          <li key={food.id} onClick={() => onFoodSelect(food)}>
            {food.name}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default FoodSearch;