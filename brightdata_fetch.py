import os
import time
import requests
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

TOKEN = "146944db-db12-41d1-9626-e53d500a4879"
DATASET_ID = "gd_lpfll7v5hcqtkxl61"
print("Token loaded:", TOKEN[:10] if TOKEN else "NOT FOUND")

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

def scrape_market_demand(skills):
    results = {}

    for skill in skills:
        print(f"Fetching data for: {skill}...")

        try:
            # Using /v3/scrape endpoint (correct for scrapers)
            res = requests.post(
                f"https://api.brightdata.com/datasets/v3/scrape?dataset_id={DATASET_ID}&notify=false&include_errors=true",
                headers=HEADERS,
                json=[{
                    "keyword": skill,
                    "location": "India",
                    "country": "IN",
                    "time_range": "Past month"
                }]
            )
            print("  Status:", res.status_code)
            print("  Response:", res.text[:200])

            data = res.json()
            jobs = data if isinstance(data, list) else data.get("data", [])

            results[skill] = {
                "jobCount": len(jobs),
                "demand": "High" if len(jobs) > 100 else "Medium" if len(jobs) > 40 else "Low",
                "topCompanies": list(set(
                    [j.get("company_name") for j in jobs[:6] if j.get("company_name")]
                )),
                "sampleTitles": [j.get("job_title") for j in jobs[:3]]
            }

        except Exception as e:
            print(f"  Error for {skill}: {e}")
            results[skill] = {
                "jobCount": 0,
                "demand": "Unknown",
                "topCompanies": [],
                "sampleTitles": []
            }

    return results


if __name__ == "__main__":
    test_skills = ["Python", "SQL"]
    output = scrape_market_demand(test_skills)
    for skill, data in output.items():
        print(f"\n{skill}: {data}")