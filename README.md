#  Skill Investment Portfolio Engine
> Treat your skills like investments. Get AI-powered recommendations on where to focus your time.

---

##  What It Does

Most people learn skills randomly. This system treats your skills like a stock portfolio — analyzing market demand and your current level to tell you exactly where to invest your time for maximum career growth.

**Input:**
- Your name and experience level
- Your current skills
- Weekly hours available

**Output:**
- AI-generated investment plan for each skill
- Risk vs Reward analysis
- Hours per week to allocate to each skill
- Step-by-step agent reasoning

---

##  How It Works (Agent Flow)
```
User fills profile form
        ↓
Agent fetches LIVE market demand (BrightData)
        ↓
Featherless AI reasons step by step:
  → Analyzes user profile
  → Checks market demand
  → Detects skill gaps & conflicts
  → Calculates time allocation
  → Computes risk vs reward
        ↓
Output: Personalized skill investment plan
```

---

##  Tech Stack

| Tool | Purpose |
|---|---|
| Python + Flask | Backend web framework |
| Featherless AI | AI reasoning and recommendations |
| BrightData | Live market demand data |
| HTML + CSS | Frontend UI |
| GitHub | Version control |

---

##  Team

| Name | Role |
|---|---|
| Kashish | GitHub Setup + Core Agent Logic (Featherless AI) |
| Sudeeksha | UI Dashboard + User Profile Form |
| Rethu | Market Demand Signals (BrightData) |
| Bhoomika | Output Display + Risk vs Reward |

---

##  How to Run Locally

**1. Clone the repo:**
```bash
git clone https://github.com/YOUR-USERNAME/skill-investment-portfolio-engine.git
cd skill-investment-portfolio-engine
```

**2. Create virtual environment:**
```bash
python -m venv venv
venv\Scripts\activate
```

**3. Install dependencies:**
```bash
pip install -r requirements.txt
```

**4. Create `.env` file:**
```
FEATHERLESS_API_KEY=your_key_here
BRIGHTDATA_API_KEY=your_key_here
```

**5. Run the app:**
```bash
python app.py
```

**6. Open in browser:**
```
http://127.0.0.1:5000
```

---

##  How It Looks

**Step 1 — Enter your profile:**
- Name, skills, experience level, weekly hours

**Step 2 — Agent thinks:**
- Shows 5-step reasoning process live on screen

**Step 3 — See your plan:**
- Each skill gets: Invest / Hold / Reduce label
- Hours per week allocated
- Risk vs Reward table

---

## 🏆 Built For
Forge Inspira 2026 Codeathon
