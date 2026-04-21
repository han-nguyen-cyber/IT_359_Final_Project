# IT\_359\_Final\_Project

# Robort :3 – Custom Web Vulnerability Scanner with AI Reporting
**Notes:**
- This was a custom web application vulnerability scanner, with an AI integration element of AI reporting, made as a project for IT 359.
- This readme outlines:
  1) The Project Overview
  2) The Tool's List of Features
  3) Instructions on How to Set Up and Run the Tool.
  
**Roles:** 
- **Technical Lead:** Han Nguyen
- **Presentation lead:** Carter Steiling
- **Documentation Lead:** Michael Mui

## i. Project Overview:
Robort is a custom-built web application vulnerability scanner with an AI integration, designed to identify common security issues in web applications, including SQL injection, cross-site scripting (XSS), and security misconfigurations. This tool is built to provide transparency on how automated scanners work, allowing users to understand detection logic, rather than relying on "black box" tools.

Robort combines automated scanning techniques with AI-powered reporting to generate detailed security assessments, which include risk analysis, remediation recommendations, and mapping to the MITRE ATT&CK framework.

This project also includes a containerized testing environment using Docker, allowing users to scan intentionally vulnerable targets such as Damn Vulnerable Web Application (DVWA), and a vulnerable vibe-coded web application.

## ii. List of Features:

1. **Automated Vulnerability Scanning**\
   a. Detects SQL Injection (SQLi)
   b. Detects Cross-Site Scripting (XSS)
   c. Identifies missing security headers (CSP, HSTS, X-Frame-Options)
   
3. **Form & Parameter Testing**\
   a. Injects payloads into URL parameters and HTML forms
   b. Analyzes server responses for indicators of vulnerabilities
   
5. **DVWA Mode**\
   a. Specialized scanning for Damn Vulnerable Web Application (DVWA), to mimic an organization's need for custom detection logic based on unique attack surface pertaining to their information environment. 
   b. Consistently identifies vulnerabilities.
   
7. **AI-Powered Reporting (AI Integration)**\
   a. Generates structured security reports, including:
     1. Risk analysis
     2. Remediation strategies
     3. MITRE ATT&CK framework mappings
        
8. **Professional Output Formatting**\
     a. Color-coded severity levels (High, Medium, Low)
     b. Table-based vulnerability display
     c. Summary Statistics
   
10. **Dockerized Lab Environment**\
     a. Scanner runs in its own container
     b. The available targets include:
          1. Damn Vulnerable Web Application (DVWA)
          2. Vibe-Coded Vulnerable Web Application
    
12. **JSON Export**\
          1. Scan results can be saved for later analysis or AI processing. 

## iii. Instructions on How to Set Up and Run the Tool:

1. **Prerequisites:**\
     a. **Remove Old Versions of Docker:**
   
   `for pkg in docker.io docker-doc docker-compose podman-docker containerd runc; do sudo apt-get remove $pkg; done`

     b. **Install Docker and Docker Compose (on Debian-based system)**
   
   ```
   sudo apt-get update
   sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin 
   ``` 

2. **Project Setup:**\

     a. **Download this project's code.**

     b. **Navigate to the project directory:**

   `cd ~/Downloads/robort`

     c. **Ensure the folder structure looks like this:**

```
robort/
|--- docker-compose.yml
|--- robort/
|--- vulnapp/
```

3. **Start the Environment:**\
     a. Build and launch all the services using the following command:
   
   ` docker-compose up --build `

   This command will start the Robort scanner container, DVWA on port 8081, and the vulnerable vibe-coded app on port 5000.

4. **Access Targets:**\
     a. If you want to access DVWA:\
        - Link: http://localhost:8081\
        - Username: admin\
        - Password: password\
        - The security level should be set to LOW.\
     b. If you want to access the Vibe-Coded vulnerable app:\
        - Link: http://localhost:5000\

5. **Run the Scanner:**\
     a. Open a new terminal, and access the scanner container:
   ` docker exec -it robort bash `

     b. Scan DVWA:
     ` python main.py --target http://dvwa/ --dvwa --json `

     c. Scan Vibe-Coded Web App:
   ` python main.py --target http://vulnapp:5000 --json `

     d. To generate an AI Report:
         - An API key must be configured by creating an .env file, and defining "MY_API_KEY=xxxxxxx", where you must provide your own API key for the http://sushi.it.ilstu.edu:8080/ server.
   
   ` python main.py --target http://dvwa/ --dvwa `

   With the above command, the tool will automatically generate a detailed AI-based vulnerability report. 
   
