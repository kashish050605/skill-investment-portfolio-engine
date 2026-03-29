import os
import time
import requests
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

TOKEN = os.getenv("VITE_BRIGHTDATA_TOKEN")
DATASET_ID = "gd_lpfll7v5hcjnoi9o5"  # LinkedIn Jobs dataset
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
            # Step 1: Trigger snapshot
            trigger_res = requests.post(
                f"https://api.brightdata.com/datasets/v3/trigger?dataset_id={DATASET_ID}&format=json",
                headers=HEADERS,
                json=[{
                    "keyword": skill,
                    "location": "India",
                    "time_range": "Past week"
                }]
            )
            snapshot_id = trigger_res.json().get("snapshot_id")
            print(f"  Snapshot ID: {snapshot_id}")

            # Step 2: Poll until ready
            jobs = []
            for i in range(10):
                time.sleep(3)
                snap_res = requests.get(
                    f"https://api.brightdata.com/datasets/v3/snapshot/{snapshot_id}?format=json",
                    headers=HEADERS
                )
                snap_data = snap_res.json()
                if snap_data.get("status") == "ready":
                    jobs = snap_data.get("data", [])
                    print(f"  Found {len(jobs)} jobs for {skill}")
                    break

            # Step 3: Build demand signal
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


# Test it
if __name__ == "__main__":
    test_skills = ["Python", "SQL"]
    output = scrape_market_demand(test_skills)
    for skill, data in output.items():
        print(f"\n{skill}: {data}")