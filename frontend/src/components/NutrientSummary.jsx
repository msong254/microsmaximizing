// NutrientSummary.jsx
import React from 'react';

export default function NutrientSummary({ nutrients }) {
  if (!Array.isArray(nutrients)) {
    console.error("Expected nutrients to be an array, got:", nutrients);
    return <div>No nutrient data available.</div>;
  }

  return (
    <div>
      <h2 className="text-xl font-bold mb-2">Nutrient Summary</h2>
      <ul>
        {nutrients.map((nutrient, index) => (
          <li key={index}>
            {nutrient.name}: {nutrient.amount} {nutrient.unit}
          </li>
        ))}
      </ul>
    </div>
  );
}