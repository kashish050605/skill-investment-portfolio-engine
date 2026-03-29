from flask import Flask, render_template, request
import json
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

FEATHERLESS_API_KEY = os.getenv("FEATHERLESS_API_KEY")

def run_agent(name, experience, skills, market_demand):
    
    # AGENT LOOP — runs up to 2 times if gaps are found
    for attempt in range(2):

        prompt = f"""
You are a Skill Investment Agent. Think step by step.

User Profile:
- Name: {name}
- Experience Level: {experience}
- Skills: {", ".join(skills)}

Live Market Demand Data:
{json.dumps(market_demand, indent=2)}

Follow these steps:

STEP 1 - ANALYZE USER PROFILE:
Look at experience level and skills. Identify strengths and weaknesses.

STEP 2 - ANALYZE MARKET DEMAND:
Look at the live market data. Which skills are high/medium/low demand?

STEP 3 - IDENTIFY CONFLICTS AND GAPS:
Are there skills the user has that are low demand?
Are there high demand skills missing? Flag them.
If gaps exist, write "GAPS FOUND" in your step 3 response.

STEP 4 - CALCULATE ALLOCATION:
Decide time/effort % for each skill.
Higher demand + lower user level = invest more.

STEP 5 - RISK VS REWARD:
Calculate risk and reward for each skill.

STEP 6 - FINAL RECOMMENDATION:
One clear advice like "Invest more in X, reduce Y because..."

Respond ONLY in this exact JSON format:
{{
  "gaps_found": true or false,
  "agent_steps": {{
    "step1_user_profile": "analysis here",
    "step2_market_analysis": "analysis here",
    "step3_conflicts": "analysis here",
    "step4_allocation": "analysis here",
    "step5_risk_reward": "analysis here"
  }},
  "recommendation": "overall advice here",
  "skills": {{
    "SkillName": {{
      "allocation": "40%",
      "risk": "Low",
      "reward": "High",
      "reason": "short reason here"
    }}
  }}
}}
"""

        response = requests.post(
            "https://api.featherless.ai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {FEATHERLESS_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "mistralai/Mistral-7B-Instruct-v0.2",
                "messages": [
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": 1500
            }
        )

        result = response.json()
        ai_text = result["choices"][0]["message"]["content"].strip()

        # Clean JSON response
        if "```json" in ai_text:
            ai_text = ai_text.split("```json")[1].split("```")[0].strip()
        elif "```" in ai_text:
            ai_text = ai_text.split("```")[1].split("```")[0].strip()

        parsed = json.loads(ai_text)

        # AGENT DECISION — if no gaps, stop loop. If gaps, run again.
        if not parsed.get("gaps_found", False):
            break

    return parsed


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/result", methods=["POST"])
def result():
    name = request.form.get("name")
    skills = request.form.get("skills").split(",")
    experience = request.form.get("experience")

    # Import Rethu's live market data fetch
    from brightdata_fetch import fetch_market_demand
    market_demand = fetch_market_demand(skills)

    # Run the agent
    ai_result = run_agent(name, experience, skills, market_demand)

    return render_template("output.html",
                           name=name,
                           experience=experience,
                           recommendation=ai_result["recommendation"],
                           agent_steps=ai_result["agent_steps"],
                           skills=ai_result["skills"])


if __name__ == "__main__":
    app.run(debug=True)
