import requests, os, json
from dotenv import load_dotenv
load_dotenv()

URL = "http://sushi.it.ilstu.edu:8080/api/chat/completions"
MODEL = "translategemma:latest"

def generate_ai_report(findings, api_key=None):
    token = os.getenv("MY_API_KEY")
    if not token:
        return "[!] MISSING API KEY."

    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system",
	 "content": (
	"You are a senior cybersecurity digital penetration tester specialist. "
	"When answering, provide a detailed report, risk analysis, remediation"
	"suggestions, and MITRE ATT&CK mapping. Avoid em-dashes and keep an"
	"informative, educational tone."
	),
},
            {"role": "user", 
		"content": json.dumps(findings)}
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
