import requests
import os
import json
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Configuration for API communication
API_URL = "http://sushi.it.ilstu.edu:8080/api/chat/completions"
MODEL_NAME = "translategemma:latest"


def generate_ai_report(findings, api_key=None):
    """
    Sends vulnerability findings to a local LLM and returns a professional security report.

    Args:
        findings (dict/list): The raw security data to be analyzed.
        api_key (str, optional): Overwrite for the API key. Defaults to environment variable.

    Returns:
        str: The generated report from the AI or an error message.
    """
    # Prioritize provided api_key argument, fallback to environment variable
    token = api_key or os.getenv("MY_API_KEY")

    if not token:
        return "ERROR: Missing API Key."

    # Define the persona and formatting constraints for the AI model
    system_prompt = (
        "### CONTEXT\n"
        "You are processing raw findings from a security scan targeting a controlled web environment. "
        "The data provided is JSON-formatted and contains vulnerabilities ranging from low to critical.\n\n"

        "### ROLE\n"
        "Act as a Senior Cybersecurity Penetration Tester with 10+ years of experience in "
        "digital forensics and ethical hacking. Your tone must be clinical, objective, and authoritative.\n\n"

        "### EXPLICIT INSTRUCTIONS\n"
        "1. Analyze findings for logical patterns (e.g., chains of vulnerabilities).\n"
        "2. Avoid using em-dashes and flowery language.\n"
        "3. Use professional security terminology (e.g., 'Least Privilege', 'Input Sanitization').\n"
        "4. Prioritize high-impact vulnerabilities at the top of the report.\n\n"

        "### DETAILS\n"
        "Include a dedicated section for MITRE ATT&CK techniques (e.g., T1190 for Exploit Public-Facing Application). "
        "For each remediation, provide a code-level example or a configuration fix.\n\n"

        "### OUTPUT\n"
        "Format the response in clear Markdown with the following headers:\n"
        "- Executive Summary\n"
        "- Detailed Technical Findings\n"
        "- Risk Impact Assessment\n"
        "- Remediation Strategy\n"
        "- MITRE ATT&CK Mapping"
    )

    # Prepare the JSON payload for the POST request
    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": json.dumps(findings)}
        ]
    }

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    try:
        # Execute the request to the AI orchestration server
        response = requests.post(API_URL, json=payload, headers=headers, timeout=30)
        response.raise_for_status()  # Check for HTTP errors (4xx or 5xx)

        data = response.json()

        # Extract content using OpenAI-style schema
        if "choices" in data:
            return data["choices"][0]["message"]["content"]

        # Handle fallback response formats from different providers (Ollama/Custom)
        return data.get("response") or data.get("message") or str(data)

    except requests.exceptions.RequestException as e:
        return f"[!] Network error occurred: {str(e)}"
    except Exception as e:
        return f"[!] An unexpected error occurred: {str(e)}"