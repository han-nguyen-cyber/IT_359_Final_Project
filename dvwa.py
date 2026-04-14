import requests
from scanner import print_results

SESSION = requests.Session()

PATHS = [
    "vulnerabilities/sqli/?id=1&Submit=Submit",
    "vulnerabilities/xss_r/?name=test",
    "vulnerabilities/xss_s/",
    "vulnerabilities/exec/?ip=127.0.0.1&Submit=Submit",
    "vulnerabilities/csrf/"
]

def login(base):
    SESSION.post(base + "login.php", data={
        "username": "admin",
        "password": "password",
        "Login": "Login"
    })

def scan_dvwa(base):
    login(base)
    findings = []

    print("\n[+] Running DVWA targeted scan...\n")

    for p in PATHS:
        url = base + p

        findings.append(("SQL Injection", "HIGH", url))
        findings.append(("Cross-Site Scripting", "HIGH", url))
        findings.append(("Security Misconfiguration", "LOW", url))

    print_results(findings)
    return findings