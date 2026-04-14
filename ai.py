import requests
import os
import json

URL = "http://sushi.it.ilstu.edu:8080/api/chat/completions"
MODEL = "translategemma:latest"


def generate_ai_report(findings, api_key=None):
    structured = [
        {"type": f[0], "severity": f[1], "url": f[2]}
        for f in findings
    ]

    # allow either passed key OR env var
    token = api_key or os.getenv("API_KEY")

    if not token:
        return "[!] Missing API key (set MY_API_KEY or pass api_key)"

    payload = {
        "model": MODEL,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a cybersecurity analyst. "
                    "Generate a structured report with: risk, remediation, and MITRE ATT&CK mapping."
                )
            },
            {
                "role": "user",
                "content": json.dumps(structured, indent=2)
            }
        ]
    }

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    try:
        r = requests.post(URL, headers=headers, json=payload, timeout=15)

        if r.status_code != 200:
            return f"[!] HTTP {r.status_code} ERROR:\n{r.text}"

        data = r.json()

        if "choices" not in data:
            return f"[!] Unexpected API response format:\n{data}"

        return data["choices"][0]["message"]["content"]

    except requests.exceptions.RequestException as e:
        return f"[!] Request failed: {e}"