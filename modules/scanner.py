from modules.utils import run_cmd, log
from modules.installer import tool_available


def run_scan(domain: str, alive_file: str):
    base = f"output/{domain}"

    # --- Nmap ---
    if tool_available("nmap"):
        log("[*] Running nmap...")
        code, out, err = run_cmd(
            ["nmap", "-iL", alive_file, "-sS", "-sV",
             "--script=default,vuln", "-oN", f"{base}/nmap.txt"],
            timeout=600
        )
        if code != 0:
            log(f"[!] nmap error: {err.strip()}")
        else:
            log("[✓] nmap complete")
    else:
        log("[!] nmap not available, skipping port scan")

    # --- Nuclei ---
    if tool_available("nuclei"):
        log("[*] Running nuclei...")
        code, out, err = run_cmd(
            ["nuclei", "-l", alive_file, "-o", f"{base}/nuclei.txt"],
            timeout=600
        )
        if code != 0:
            log(f"[!] nuclei error: {err.strip()}")
        else:
            log("[✓] nuclei complete")
    else:
        log("[!] nuclei not available, skipping")

    # --- Dirsearch ---
    if tool_available("dirsearch"):
        log("[*] Running dirsearch...")
        code, out, err = run_cmd(
            ["dirsearch", "-l", alive_file, "-o", f"{base}/dirs.txt"],
            timeout=600
        )
        if code != 0:
            log(f"[!] dirsearch error: {err.strip()}")
        else:
            log("[✓] dirsearch complete")
    else:
        log("[!] dirsearch not available, skipping")
