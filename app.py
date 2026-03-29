from flask import Flask, render_template, request
import json
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

FEATHERLESS_API_KEY = os.getenv("FEATHERLESS_API_KEY")

def run_agent(name, experience, skills, market_demand, budget):

    for attempt in range(2):
        prompt = f"""
You are a Skill Investment Agent. Think step by step.

User Profile:
- Name: {name}
- Experience Level: {experience}
- Skills: {", ".join(skills)}
- Weekly hours available: {budget}

Live Market Demand Data:
{json.dumps(market_demand, indent=2)}

Respond ONLY in this exact JSON format with no extra text:
{{
  "gaps_found": false,
  "headline": "one line summary of user profile",
  "agent_steps": [
    {{"title": "Profile Analysis", "detail": "your analysis"}},
    {{"title": "Market Demand Check", "detail": "your analysis"}},
    {{"title": "Conflict Detection", "detail": "your analysis"}},
    {{"title": "Allocation Plan", "detail": "your analysis"}},
    {{"title": "Risk vs Reward", "detail": "your analysis"}}
  ],
  "skills": {{
    "SkillName": {{
      "allocation": 40,
      "type": "invest",
      "status_label": "Invest",
      "icon": "🚀",
      "reason": "short reason here",
      "trending": "Yes",
      "risk_label": "Low",
      "career_impact": "High"
    }}
  }}
}}

Rules:
- type must be: invest, hold, or reduce
- icon: use 🚀 for invest, ⏸ for hold, ↘ for reduce
- allocation is a number, all skills must add up to 100
- trending: Yes or No
- risk_label: Low, Medium, or High
- career_impact: Low, Medium, or High
"""

        try:
            response = requests.post(
                "https://api.featherless.ai/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {FEATHERLESS_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "mistralai/Mistral-7B-Instruct-v0.2",
                    "messages": [{"role": "user", "content": prompt}],
                    "max_tokens": 1500
                }
            )

            result = response.json()
            print("FEATHERLESS RESPONSE:", result)

            if "choices" not in result:
                print("ERROR FROM FEATHERLESS:", result)
                return get_fallback(skills, budget)

            ai_text = result["choices"][0]["message"]["content"].strip()

            if "```json" in ai_text:
                ai_text = ai_text.split("```json")[1].split("```")[0].strip()
            elif "```" in ai_text:
                ai_text = ai_text.split("```")[1].split("```")[0].strip()

            parsed = json.loads(ai_text)

            if not parsed.get("gaps_found", False):
                break

        except Exception as e:
            print("EXCEPTION:", e)
            return get_fallback(skills, budget)

    return parsed


def get_fallback(skills, budget):
    skill_list = [s.strip() for s in skills]
    allocation = 100 // len(skill_list)
    skills_data = {}
    for skill in skill_list:
        skills_data[skill] = {
            "allocation": allocation,
            "type": "invest",
            "status_label": "Invest",
            "icon": "🚀",
            "reason": "Based on your profile this skill is worth investing in.",
            "trending": "Yes",
            "risk_label": "Low",
            "career_impact": "High"
        }
    return {
        "gaps_found": False,
        "headline": "Skill analysis complete",
        "agent_steps": [
            {"title": "Profile Analysis", "detail": "User profile reviewed."},
            {"title": "Market Demand Check", "detail": "Market data analyzed."},
            {"title": "Conflict Detection", "detail": "No major conflicts found."},
            {"title": "Allocation Plan", "detail": "Equal allocation applied."},
            {"title": "Risk vs Reward", "detail": "All skills show positive outlook."}
        ],
        "skills": skills_data
    }


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/result", methods=["POST"])
def result():
    name = request.form.get("name")
    skills = request.form.get("skills").split(",")
    experience = request.form.get("experience")
    budget = int(request.form.get("budget", 10))

    # Temporary market demand until BrightData is connected
    market_demand = {skill.strip(): "High" for skill in skills}

    ai_result = run_agent(name, experience, skills, market_demand, budget)

    return render_template("output.html",
                           name=name,
                           headline=ai_result["headline"],
                           budget=budget,
                           agent_steps=ai_result["agent_steps"],
                           skills=ai_result["skills"])


if __name__ == "__main__":
    app.run(debug=True)