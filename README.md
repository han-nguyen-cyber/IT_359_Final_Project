# IT\_359\_Final\_Project

# Project Proposal – Custom Web Vulnerability Scanner
Roles: 
- Technical Lead: Han Nguyen
- Presentation lead: Carter Steiling
- Documentation Lead: Michael Mui

## Project Overview:
Robort is a custom-built web application vulnerability scanner with an AI integration, designed to identify common security issues in web applications, including SQL injection, cross-site scripting (XSS), and security misconfigurations. This tool is built to provide transparency on how automated scanners work, allowing users to understand detection logic, rather than relying on "black box" tools.

Robort combines automated scanning techniques with AI-powered reporting to generate detailed security assessments, which include risk analysis, remediation recommendations, and mapping to the MITRE ATT&CK framework.

This project also includes a containerized testing environment using Docker, allowing users to scan intentionally vulnerable targets such as Damn Vulnerable Web Application (DVWA), and a vulnerable vibe-coded web application.

## List of Features:

1. Automated Vulnerability Scanning
   a. Detects SQL Injection (SQLi)
   b. Detects Cross-Site Scripting (XSS)
   c. Identifies missing security headers (CSP, HSTS, X-Frame-Options)
2. Form & Parameter Testing
   a. Injects payloads into URL parameters and HTML forms
   b. Analyzes server responses for indicators of vulnerabilities
3. DVWA Mode
   a. Specialized scanning for Damn Vulnerable Web Application (DVWA), to mimic an organization's need for custom detection logic based on unique attack surface pertaining to their information environment. 
   b. Consistently identifies vulnerabilities.
4. AI-Powered Reporting (AI Integration)
   a. Generates structured security reports, including:
     1. Risk analysis
     2. Remediation strategies
     3. MITRE ATT&CK framework mappings
5. Professional Output Formatting
     a. Color-coded severity levels (High, Medium, Low)
     b. Table-based vulnerability display
     c. Summary Statistics
6. Dockerized Lab Environment
     a. Scanner runs in its own container
     b. The available targets include:
          1. Damn Vulnerable Web Application (DVWA)
          2. Vibe-Coded Vulnerable Web Application
     c. JSON Export
          1. Scan results can be saved for later analysis, or AI processing. 

## Instructions on How to Set Up and Run the Tool:

1. Prerequisites
     a. Remove Old Versions of Docker:
   
   `for pkg in docker.io docker-doc docker-compose podman-docker containerd runc; do sudo apt-get remove $pkg; done`

     b. Install Docker and Docker Compose (on Debian-based system)
   
   ```sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin ``` 

3. Project Setup

     a. Download this project's code.

     b. Navigate to the project directory:

   `cd ~/Downloads/robort`

     c. Ensure the folder structuer looks like this:

```robort/
|--- docker-compose.yml
|--- robort/
|--- vulnapp/```
