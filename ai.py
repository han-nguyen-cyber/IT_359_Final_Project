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
        "Authorization": f"Bearer {os.getenv('API_KEY')}",
        "Content-Type": "application/json"
    }

    try:
        r = requests.post(
            "http://sushi.it.ilstu.edu:8080/api/chat/completions",
            headers=headers,
            json=payload,
            timeout=15
        )

        try:
            data = r.json()
            return data["choices"][0]["message"]["content"]
        except:
            return f"[!] Unexpected API format:\n{r.text}"

    except Exception as e:
        return f"[!] AI request failed: {e}"