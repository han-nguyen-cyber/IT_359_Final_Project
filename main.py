import argparse
from scanner import scan_site, banner, print_summary, save_json
from dvwa import scan_dvwa
from ai import generate_ai_report

def main():
    parser = argparse.ArgumentParser(description="Robort :3 Scanner")

    parser.add_argument("--target", help="Target URL")
    parser.add_argument("--dvwa", action="store_true", help="DVWA mode")
    parser.add_argument("--no-ai", action="store_true", help="Disable AI")
    parser.add_argument("--json", action="store_true", help="Save JSON")

    args = parser.parse_args()

    banner()

    target = args.target if args.target else input("Target URL: ")

    # Scan
    if args.dvwa:
        findings = scan_dvwa(target)
    else:
        findings = scan_site(target)

    print_summary(findings)

    if args.json:
        save_json(findings)

    if not args.no_ai:
        print("\n[+] Generating AI report...\n")
        try:
            print(generate_ai_report(findings))
        except Exception as e:
            print(f"[!] AI failed: {e}")

if __name__ == "__main__":
    main()
