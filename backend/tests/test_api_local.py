import requests
import json

url = "http://127.0.0.1:8000/astro/compute"
payload = {
    "dt_local": "1977-11-16T00:10:00",
    "lat": 33.8938,
    "lon": 35.5018,
    "tz_name": "",
    "include_angles_in_aspects": True
}

response = requests.post(url, json=payload, timeout=300)

print("Status Code:", response.status_code)
print("Response JSON:\n", json.dumps(response.json(), indent=2, ensure_ascii=False))

# Save to file
with open("astro_response.json", "w", encoding="utf-8") as f:
    json.dump(response.json(), f, indent=2, ensure_ascii=False)
