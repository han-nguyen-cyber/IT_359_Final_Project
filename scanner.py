import requests
from urllib.parse import urlparse, parse_qs, urlencode, urljoin
from bs4 import BeautifulSoup
from colorama import Fore, Style, init
from tabulate import tabulate

init(autoreset=True)

SESSION = requests.Session()

SQLI = "' OR '1'='1"
XSS = "<script>alert(1)</script>"

# ------------------------
# BANNER
# ------------------------
def banner():
    print(Fore.CYAN + r"""
    
██████╗░░█████╗░██████╗░░█████╗░██████╗░████████╗       ██╗██████╗░
██╔══██╗██╔══██╗██╔══██╗██╔══██╗██╔══██╗╚══██╔══╝       ╚═╝╚════██╗
██████╔╝██║░░██║██████╦╝██║░░██║██████╔╝░░░██║░░░       ░░░░█████╔╝
██╔══██╗██║░░██║██╔══██╗██║░░██║██╔══██╗░░░██║░░░       ░░░░╚═══██╗
██║░░██║╚█████╔╝██████╦╝╚█████╔╝██║░░██║░░░██║░░░       ██╗██████╔╝
╚═╝░░╚═╝░╚════╝░╚═════╝░░╚════╝░╚═╝░░╚═╝░░░╚═╝░░░       ╚═╝╚═════╝░
╔══════════════════════════════════════╗
║            ROBORT :3 SCANNER         ║
╚══════════════════════════════════════╝
""")

# ------------------------
# PARAM INJECTION
# ------------------------
def inject(url, payload):
    parsed = urlparse(url)
    params = parse_qs(parsed.query)

    if not params:
        return []

    urls = []
    for k in params:
        temp = params.copy()
        temp[k] = payload
        urls.append(f"{parsed.scheme}://{parsed.netloc}{parsed.path}?{urlencode(temp, doseq=True)}")
    return urls

# ------------------------
# FORM SCANNING
# ------------------------
def test_forms(url):
    findings = []
    try:
        r = SESSION.get(url)
        soup = BeautifulSoup(r.text, "html.parser")

        for form in soup.find_all("form"):
            action = form.get("action")
            method = form.get("method", "get").lower()
            form_url = urljoin(url, action)

            inputs = form.find_all("input")
            data = {i.get("name"): "test" for i in inputs if i.get("name")}

            for payload in [SQLI, XSS]:
                for key in data:
                    temp = data.copy()
                    temp[key] = payload

                    if method == "post":
                        res = SESSION.post(form_url, data=temp)
                    else:
                        res = SESSION.get(form_url, params=temp)

                    if payload in res.text:
                        findings.append(("XSS (Form)", "HIGH", form_url))

                    if any(e in res.text.lower() for e in ["sql","mysql","syntax"]):
                        findings.append(("SQLi (Form)", "HIGH", form_url))
    except:
        pass

    return findings

# ------------------------
# PARAM TESTING
# ------------------------
def test(url):
    findings = []

    for u in inject(url, SQLI):
        r = SESSION.get(u)
        if any(e in r.text.lower() for e in ["sql","syntax"]):
            findings.append(("SQL Injection", "HIGH", u))

    for u in inject(url, XSS):
        r = SESSION.get(u)
        if XSS in r.text:
            findings.append(("XSS", "MEDIUM", u))

    return findings

# ------------------------
# HEADERS
# ------------------------
def check_headers(url):
    r = SESSION.get(url)
    findings = []

    if "Content-Security-Policy" not in r.headers:
        findings.append(("Missing CSP", "LOW", url))
    if "X-Frame-Options" not in r.headers:
        findings.append(("Missing X-Frame", "LOW", url))
    if "Strict-Transport-Security" not in r.headers:
        findings.append(("Missing HSTS", "LOW", url))

    return findings

# ------------------------
# TABLE OUTPUT
# ------------------------
def print_results(findings):
    if not findings:
        print(Fore.GREEN + "[✓] No vulnerabilities found\n")
        return

    print(Fore.RED + f"\n[!] {len(findings)} vulnerabilities detected\n")

    table = []
    for i, f in enumerate(findings, 1):
        vuln, severity, url = f

        color = {
            "HIGH": Fore.RED,
            "MEDIUM": Fore.YELLOW,
            "LOW": Fore.BLUE
        }.get(severity, Fore.WHITE)

        table.append([i, vuln, color + severity + Style.RESET_ALL, url])

    print(tabulate(table, headers=["#", "Vulnerability", "Severity", "URL"], tablefmt="fancy_grid"))

# ------------------------
# SUMMARY
# ------------------------
def print_summary(findings):
    summary = {"HIGH": 0, "MEDIUM": 0, "LOW": 0}

    for f in findings:
        summary[f[1]] += 1

    print("\n" + Fore.CYAN + "=== SCAN SUMMARY ===")
    print(Fore.RED + f"HIGH:   {summary['HIGH']}")
    print(Fore.YELLOW + f"MEDIUM: {summary['MEDIUM']}")
    print(Fore.BLUE + f"LOW:    {summary['LOW']}")

# ------------------------
# MAIN SCAN
# ------------------------
import json

def scan_site(url):
    findings = []
    findings += test(url)
    findings += test_forms(url)
    findings += check_headers(url)

    print_results(findings)
    return findings

def save_json(findings, filename="report.json"):
    data = [
        {
            "type": f[0],
            "severity": f[1],
            "url": f[2]
        }
        for f in findings
    ]

    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

    print(f"\n[+] Results saved to {filename}")