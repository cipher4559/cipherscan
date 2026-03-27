import os
from modules.utils import file_has_content, log


def _read_lines(path: str) -> list[str]:
    if not file_has_content(path):
        return []
    with open(path, "r", errors="replace") as f:
        return [l.strip() for l in f if l.strip()]


def analyze_results(domain: str) -> list[dict]:
    base = f"output/{domain}"
    findings = []

    # --- Nuclei ---
    nuclei_lines = _read_lines(f"{base}/nuclei.txt")
    for line in nuclei_lines:
        # nuclei output format: [severity] [template] [url] ...
        severity = "Medium"
        if line.startswith("[critical]"):
            severity = "Critical"
        elif line.startswith("[high]"):
            severity = "High"
        elif line.startswith("[low]"):
            severity = "Low"
        elif line.startswith("[info]"):
            severity = "Info"
        findings.append({"type": "Nuclei", "detail": line, "severity": severity})

    log(f"[✓] Nuclei: {len(nuclei_lines)} findings")

    # --- XSS (dalfox) ---
    xss_lines = _read_lines(f"{base}/xss.txt")
    for line in xss_lines:
        if "POC" in line or "xss" in line.lower():
            findings.append({"type": "XSS", "detail": line, "severity": "High"})

    log(f"[✓] XSS: {len(xss_lines)} potential findings")

    # --- SQLi (sqlmap) ---
    sqlmap_dir = f"{base}/sqlmap"
    sqli_count = 0
    if os.path.isdir(sqlmap_dir):
        for root, _, files in os.walk(sqlmap_dir):
            for fname in files:
                if fname.endswith(".txt"):
                    lines = _read_lines(os.path.join(root, fname))
                    for line in lines:
                        if "injectable" in line.lower() or "parameter" in line.lower():
                            findings.append({
                                "type": "SQLi",
                                "detail": line,
                                "severity": "Critical"
                            })
                            sqli_count += 1

    log(f"[✓] SQLi: {sqli_count} potential findings")

    # --- Nmap open ports ---
    nmap_lines = _read_lines(f"{base}/nmap.txt")
    for line in nmap_lines:
        if "/tcp" in line and "open" in line:
            findings.append({"type": "Open Port", "detail": line, "severity": "Info"})

    log(f"[✓] Analysis complete — total findings: {len(findings)}")
    return findings
