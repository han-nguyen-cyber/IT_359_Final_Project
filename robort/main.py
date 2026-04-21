import argparse
from scanner import scan_site, banner, print_summary, save_json
from dvwa import scan_dvwa
from ai import generate_ai_report

def main():
    """
    Main entry point for the Robort :3 Scanner.
    Handles command-line arguments, orchestrates scan types, and manages output.
    """
    # Initialize the argument parser for CLI interaction
    parser = argparse.ArgumentParser(description="Robort :3 Scanner")

    # Define flags and parameters
    parser.add_argument("--target", help="Target URL to be scanned")
    parser.add_argument("--dvwa", action="store_true", help="Enable specialized DVWA authenticated mode")
    parser.add_argument("--no-ai", action="store_true", help="Disable the AI report generation feature")
    parser.add_argument("--json", action="store_true", help="Save the scan results to a JSON file")

    # Parse provided arguments from the terminal
    args = parser.parse_args()

    # Display the ASCII art header from the scanner module
    banner()

    # Determine target: Use the CLI flag if provided, otherwise prompt the user for input
    target = args.target if args.target else input("Target URL: ")

    # Branching logic to decide which scan module to execute
    if args.dvwa:
        # Executes scan using the authenticated session logic in dvwa.py
        findings = scan_dvwa(target)
    else:
        # Executes the general-purpose scan from scanner.py
        findings = scan_site(target)

    # Print a high-level count of vulnerabilities found (High/Medium/Low)
    print_summary(findings)

    # Optional output: Save raw data to a local file for further analysis
    if args.json:
        save_json(findings)

    # AI Integration: Sends findings to the LLM unless the user explicitly opted out
    if not args.no_ai:
        print("\n[+] Generating AI report...\n")
        try:
            # Pass the list of findings to the generate_ai_report function in ai.py
            print(generate_ai_report(findings))
        except Exception as e:
            # Fail gracefully to ensure the scanner finishes even if the AI is offline
            print(f"[!] AI failed: {e}")

# Standard Python idiom to ensure main() runs only if this file is executed directly
if __name__ == "__main__":
    main()