import requests
from scanner import print_results

# Initialize a session to persist login status, to avoid being logged out during testing.
SESSION = requests.Session()

def login(base_url):
    # Authenticate and establish the session.
    # The username is admin, the password is password.
    login_data = {"username": "admin", "password": "password", "Login": "Login"}
    try:
        SESSION.post(f"{base_url}login.php", data=login_data)
    except Exception as e:
        print(f"[!] Connection error: {e}") # Error handling

def scan_dvwa(base_url):
    """
    Perform security testing by analyzing HTTP responses
    for specific vulnerability signatures.
    """
    login(base_url)
    findings = []

    # 1. TEST FOR SQL INJECTION
    # Payload: A single quote (') is the classic test to break a SQL query.
    sqli_url = f"{base_url}vulnerabilities/sqli/?id='&Submit=Submit"
    try:
        response = SESSION.get(sqli_url)
        # If the server returns a database error message, it's vulnerable.
        if "SQL syntax" in response.text or "mysql_fetch" in response.text:
            findings.append(("SQL Injection", "CRITICAL", sqli_url))
    except:
        pass

    # 2. TEST FOR COMMAND INJECTION
    # Payload: Use a semicolon (;) followed by a system command like 'whoami'.
    exec_url = f"{base_url}vulnerabilities/exec/"
    exec_data = {"ip": "127.0.0.1; whoami", "Submit": "Submit"}
    try:
        # We use a POST here because the 'exec' page uses a form
        response = SESSION.post(exec_url, data=exec_data)
        # If the output of 'whoami' (like 'www-data' or 'root') appears, it's vulnerable.
        if "www-data" in response.text or "apache" in response.text:
            findings.append(("Command Injection", "HIGH", exec_url))
    except:
        pass

    # 3. TEST FOR MISSING SECURITY HEADERS (CSP)
    try:
        response = SESSION.get(base_url)
        if "Content-Security-Policy" not in response.headers:
            findings.append(("Missing CSP Header", "LOW", base_url))
    except:
        pass

    print_results(findings)
    return findings