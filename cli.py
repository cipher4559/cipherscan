#!/usr/bin/env python3
"""
CipherScan CLI
Usage:
    python cli.py -d example.com [--authorize] [--no-exploit]
"""

import argparse
import sys
from db import init_db, insert_scan
from cipherscan import main
from modules.utils import validate_domain, log


def parse_args():
    parser = argparse.ArgumentParser(
        prog="cipherscan",
        description="CipherScan — Automated Security Reconnaissance & Scanning"
    )
    parser.add_argument(
        "-d", "--domain",
        required=True,
        help="Target domain (e.g. example.com)"
    )
    parser.add_argument(
        "--authorize",
        action="store_true",
        help="Confirm you have explicit authorization to test this target"
    )
    parser.add_argument(
        "--no-exploit",
        action="store_true",
        help="Skip XSS and SQLi exploitation phases"
    )
    return parser.parse_args()


def main_cli():
    args = parse_args()
    domain = args.domain.strip().lower()

    if not validate_domain(domain):
        print(f"[✗] Invalid domain: {domain!r}")
        sys.exit(1)

    if not args.authorize:
        print("\n[!] You must pass --authorize to confirm you have permission")
        print("    to perform security testing on this target.")
        print("    Unauthorized scanning may be illegal in your jurisdiction.\n")
        sys.exit(1)

    authorized = not args.no_exploit

    print(f"\n[*] Starting CipherScan for: {domain}")
    print(f"    Exploitation phases: {'enabled' if authorized else 'disabled'}\n")

    init_db()
    scan_id = insert_scan(domain)

    main(domain, scan_id, authorized=authorized)

    print(f"\n[✓] Done. Report saved to output/{domain}/report.pdf")


if __name__ == "__main__":
    main_cli()
