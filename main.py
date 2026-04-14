import argparse
from scanner import scan_site, banner, print_summary, save_json
from dvwa import scan_dvwa
from ai import generate_ai_report

def main():
    parser = argparse.ArgumentParser(description="Vulnix Web Vulnerability Scanner")

    parser.add_argument("--target", help="Target URL")
    parser.add_argument("--dvwa", action="store_true", help="Enable DVWA mode")
    parser.add_argument("--no-ai", action="store_true", help="Disable AI report")
    parser.add_argument("--json", action="store_true", help="Save results as JSON")

    args = parser.parse_args()

    banner()

    # Handle target
    target = args.target if args.target else input("Target URL: ")

    # Scan mode
    if args.dvwa:
        findings = scan_dvwa(target)
    else:
        findings = scan_site(target)

    print_summary(findings)

    # Save JSON
    if args.json:
        save_json(findings)

    # AI report
    if not args.no_ai:
        print("\n[+] Generating AI report...\n")
        print(generate_ai_report(findings))


if __name__ == "__main__":
    main()