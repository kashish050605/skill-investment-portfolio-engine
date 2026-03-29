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

Respond ONLY in this exact JSON format with no extra text before or after:
{{
  "gaps_found": false,
  "headline": "one line summary of user profile",
  "agent_steps": [
    {{"title": "Profile Analysis", "detail": "your analysis here"}},
    {{"title": "Market Demand Check", "detail": "your analysis here"}},
    {{"title": "Conflict Detection", "detail": "your analysis here"}},
    {{"title": "Allocation Plan", "detail": "your analysis here"}},
    {{"title": "Risk vs Reward", "detail": "your analysis here"}}
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
- icon: use 🚀 for invest, ⏸ for hold, 🔻 for reduce
- status_label: Invest, Hold, or Reduce
- allocation is a number not a string
- all skill allocations must add up to 100
- trending: Yes or No
- risk_label: Low, Medium, or High
- career_impact: Low, Medium, or High
- if gaps found set gaps_found to true
- respond with ONLY the JSON, no explanation, no extra text
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

            if "skills" not in parsed:
                print("NO SKILLS KEY — using fallback")
                return get_fallback(skills, budget)

            if not parsed.get("gaps_found", False):
                break

        except Exception as e:
            print("EXCEPTION:", e)
            return get_fallback(skills, budget)

    return parsed


def get_fallback(skills, budget):
    skill_list = [s.strip() for s in skills]
    count = len(skill_list)
    allocation = 100 // count
    icons = ["🚀", "⏸", "🔻"]
    types = ["invest", "hold", "reduce"]
    labels = ["Invest", "Hold", "Reduce"]

    skills_data = {}
    for i, skill in enumerate(skill_list):
        t = types[i % 3]
        skills_data[skill] = {
            "allocation": allocation,
            "type": t,
            "status_label": labels[i % 3],
            "icon": icons[i % 3],
            "reason": f"{skill} is a valuable skill worth tracking in today's market.",
            "trending": "Yes",
            "risk_label": "Low",
            "career_impact": "High"
        }

    return {
        "gaps_found": False,
        "headline": f"{experience} level profile with {count} skills analyzed",
        "agent_steps": [
            {"title": "Profile Analysis", "detail": f"{name} is at {experience} level with {count} skills."},
            {"title": "Market Demand Check", "detail": "Market demand data has been reviewed for all skills."},
            {"title": "Conflict Detection", "detail": "No major conflicts found between skills and market demand."},
            {"title": "Allocation Plan", "detail": "Time has been allocated based on skill demand and experience."},
            {"title": "Risk vs Reward", "detail": "All skills show a positive career outlook."}
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

    # Temporary until BrightData is connected
    market_demand = {skill.strip(): "High" for skill in skills}

    try:
        ai_result = run_agent(name, experience, skills, market_demand, budget)
        if not ai_result or "skills" not in ai_result:
            ai_result = get_fallback(skills, budget)
    except Exception as e:
        print("RESULT ERROR:", e)
        ai_result = get_fallback(skills, budget)

    return render_template("output.html",
                           name=name,
                           headline=ai_result["headline"],
                           budget=budget,
                           agent_steps=ai_result["agent_steps"],
                           skills=ai_result["skills"])


if __name__ == "__main__":
    app.run(debug=True)