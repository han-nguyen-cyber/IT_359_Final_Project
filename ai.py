import requests, os, json

URL = "http://sushi.it.ilstu.edu:8080/api/chat/completions"
MODEL = "translategemma:latest"

def generate_ai_report(findings, api_key=None):
    token = api_key or os.getenv("API_KEY")
    if not token:
        return "[!] Missing API key"

    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "You are a cybersecurity analyst."},
            {"role": "user", "content": json.dumps(findings)}
        ]
    }

    r = requests.post(URL, json=payload, headers={
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    })

    data = r.json()

    # OpenAI-style
    if "choices" in data:
        return data["choices"][0]["message"]["content"]

    # fallback formats
    return data.get("response") or data.get("message") or str(data)