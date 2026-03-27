from modules.recon import run_recon
from modules.scanner import run_scan
from modules.urls import collect_urls, extract_params
from modules.exploiter import run_xss, run_sqli
from modules.analyzer import analyze_results
from modules.reporter import generate_report
from modules.exporter import export_json, export_csv
from modules.installer import install_tools
from modules.utils import create_workspace, validate_domain, log
from modules.notifier import send_alert
from db import update_scan_status, insert_findings


def main(domain: str, scan_id: int, authorized: bool = False):
    # Validate domain before doing anything
    if not validate_domain(domain):
        log(f"[✗] Invalid domain rejected: {domain!r}")
        update_scan_status(scan_id, "Failed")
        return

    log(f"[*] Starting scan for {domain} (scan_id={scan_id}, authorized={authorized})")

    try:
        create_workspace(domain)
        install_tools()

        # Recon
        alive_file = run_recon(domain)
        if not alive_file:
            log("[!] No alive hosts found. Ending scan.")
            update_scan_status(scan_id, "Failed")
            return

        # Port + vuln scanning
        run_scan(domain, alive_file)

        # URL collection
        urls = collect_urls(domain)
        if not urls:
            log("[!] No URLs found — skipping param extraction and exploitation.")
        else:
            params = extract_params(domain)
            if params:
                # Exploitation only runs when user confirmed authorization
                run_xss(params, domain, authorized=authorized)
                run_sqli(params, domain, authorized=authorized)
            else:
                log("[!] No parameterised URLs — skipping exploitation phase.")

        # Analyze and report
        findings = analyze_results(domain)
        insert_findings(scan_id, findings)
        generate_report(domain, findings)
        export_json(domain, findings)
        export_csv(domain, findings)

        update_scan_status(scan_id, "Completed")
        send_alert(f"✅ CipherScan completed for {domain} — {len(findings)} findings")
        log("[✓] Scan completed successfully.")

    except Exception as e:
        log(f"[✗] Unhandled error during scan for {domain}: {e}")
        update_scan_status(scan_id, "Failed")
        send_alert(f"❌ CipherScan failed for {domain}: {e}")
