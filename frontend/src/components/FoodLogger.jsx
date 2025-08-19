import { useState } from "react";
import config from './config';

export default function FoodLogger() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);

  const searchFoods = async () => {
    if (!query.trim()) return;
    const res = await fetch(`${config.BASE_URL}/foods/search?query=${encodeURIComponent(query)}`);
    const data = await res.json();

    const resultsWithGrams = data.map((item) => ({
      ...item,
      grams: "",
    }));

    setResults(resultsWithGrams);
  };

  const logFood = async (food) => {
    const grams = parseFloat(food.grams || 0);
    if (!grams || grams <= 0) {
      alert("Please enter a valid gram amount.");
      return;
    }

    const logEntry = {
      food_id: food.id,
      amount: grams
    };

    const res = await fetch(`${config.BASE_URL}/log`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(logEntry),
    });

    if (res.ok) {
      alert(`✅ Logged ${grams}g of ${food.name}`);
      setQuery("");
      setResults([]);
    } else {
      const errorText = await res.text();
      alert(`❌ Failed to log food: ${res.status} ${errorText}`);
    }
  };

  const updateGrams = (id, value) => {
    setResults((prev) =>
      prev.map((item) =>
        item.id === id ? { ...item, grams: value } : item
      )
    );
  };

  return (
    <div className="p-6 max-w-2xl mx-auto bg-white shadow-md rounded-md space-y-6">
      <h1 className="text-2xl font-bold">🍽️ Log Your Food</h1>

      <div className="flex gap-2">
        <input
          type="text"
          placeholder="Search food..."
          className="border p-2 rounded w-full"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />
        <button
          className="bg-blue-500 text-white px-4 py-2 rounded"
          onClick={searchFoods}
        >
          Search
        </button>
      </div>

      {results.length > 0 && (
        <ul className="border rounded p-2 space-y-2 max-h-[500px] overflow-y-auto">
          {results.map((food) => (
            <li
              key={food.id}
              className="flex flex-col md:flex-row md:items-center md:justify-between gap-2 p-2 border-b"
            >
              <span className="font-medium">{food.name}</span>
              <div className="flex gap-2 items-center">
                <input
                  type="number"
                  placeholder="Grams"
                  className="border rounded p-1 w-24"
                  value={food.grams}
                  onChange={(e) => updateGrams(food.id, e.target.value)}
                />
                <button
                  className="bg-green-600 text-white px-3 py-1 rounded"
                  onClick={() => logFood(food)}
                >
                  Log
                </button>
              </div>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}