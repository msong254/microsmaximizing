import React, { useState } from 'react';

function FoodSearch({ onLog }) {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [selectedFood, setSelectedFood] = useState(null);
  const [amount, setAmount] = useState('');

  const handleSearch = async () => {
    if (!query.trim()) return;
    try {
      const response = await fetch(`/api/foods/search?query=${query}`);
      const data = await response.json();
      setResults(data);
    } catch (error) {
      console.error('Search error:', error);
    }
  };

  const handleLog = async () => {
    if (!selectedFood || !amount) return;
    try {
      await fetch('/api/log', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          food_id: selectedFood.id,
          amount: parseFloat(amount)
        })
      });
      setQuery('');
      setResults([]);
      setSelectedFood(null);
      setAmount('');
      if (onLog) onLog(); // refresh summary in App.js
    } catch (error) {
      console.error('Log error:', error);
    }
  };

  return (
    <div>
      <h2>Search for Food</h2>
      <input
        type="text"
        placeholder="Enter food name"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
      />
      <button onClick={handleSearch}>Search</button>

      {results.length > 0 && (
        <ul>
          {results.map((food) => (
            <li
              key={food.id}
              onClick={() => setSelectedFood(food)}
              style={{ cursor: 'pointer', fontWeight: selectedFood?.id === food.id ? 'bold' : 'normal' }}
            >
              {food.name}
            </li>
          ))}
        </ul>
      )}

      {selectedFood && (
        <div>
          <h3>Selected: {selectedFood.name}</h3>
          <input
            type="number"
            placeholder="Amount in grams"
            value={amount}
            onChange={(e) => setAmount(e.target.value)}
          />
          <button onClick={handleLog}>Log</button>
        </div>
      )}
    </div>
  );
}

export default FoodSearch;