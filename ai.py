import requests, os, json

def generate_ai_report(findings):
    structured = [{"type":f[0],"severity":f[1],"url":f[2]} for f in findings]

    payload = {
        "model": "translategemma:latest",
        "messages": [
            {"role": "system", "content": "Generate a cybersecurity report with risk, remediation, and MITRE ATT&CK mapping."},
            {"role": "user", "content": json.dumps(structured, indent=2)}
        ]
    }

    headers = {
        "Authorization": f"Bearer {os.getenv('MY_API_KEY')}",
        "Content-Type": "application/json"
    }

    r = requests.post(
        "https://sushi.it.ilstu.edu:8080/api/chat/completions",
        headers=headers,
        json=payload
    )

    return r.json()["choices"][0]["message"]["content"]