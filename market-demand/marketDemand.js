// feature/market-demand — Rethu's module

const demandData = {
  "Python": { "demand": "High", "trend": "Rising", "category": "Programming" },
  "SQL": { "demand": "High", "trend": "Stable", "category": "Data" },
  "Excel": { "demand": "Medium", "trend": "Stable", "category": "Productivity" },
  "Machine Learning": { "demand": "High", "trend": "Rising", "category": "AI/ML" },
  "Power BI": { "demand": "Medium", "trend": "Rising", "category": "Data" },
  "Tableau": { "demand": "Medium", "trend": "Stable", "category": "Data" },
  "JavaScript": { "demand": "High", "trend": "Stable", "category": "Programming" },
  "Blockchain": { "demand": "Low", "trend": "Declining", "category": "Emerging" },
  "R": { "demand": "Medium", "trend": "Stable", "category": "Data" },
  "Cloud (AWS/Azure)": { "demand": "High", "trend": "Rising", "category": "Infrastructure" }
};

const DEMAND_SCORES = {
  High:   1.0,
  Medium: 0.6,
  Low:    0.2
};

const TREND_MULTIPLIERS = {
  Rising:    1.2,
  Stable:    1.0,
  Declining: 0.7
};

function getDemandSignal(skill) {
  const entry = demandData[skill];
  if (!entry) return { demand: "Unknown", trend: "Unknown", score: 0.5 };

  const score = DEMAND_SCORES[entry.demand] * TREND_MULTIPLIERS[entry.trend];
  return {
    demand: entry.demand,
    trend: entry.trend,
    category: entry.category,
    score: parseFloat(score.toFixed(2))
  };
}

function getDemandSignals(skills) {
  const result = {};
  for (const skill of skills) {
    result[skill] = getDemandSignal(skill);
  }
  return result;
}

function getAllDemandSignals() {
  return getDemandSignals(Object.keys(demandData));
}
