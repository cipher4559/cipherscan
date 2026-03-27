from modules.utils import run_cmd, file_has_content, log
from modules.installer import tool_available


def run_recon(domain: str) -> str | None:
    base = f"output/{domain}"

    # --- Subdomain enumeration ---
    subs_file = f"{base}/subs.txt"

    if tool_available("subfinder"):
        code, out, err = run_cmd(["subfinder", "-d", domain, "-o", subs_file], timeout=120)
        if code != 0:
            log(f"[!] subfinder error: {err.strip()}")
    else:
        log("[!] subfinder not available, skipping")

    if tool_available("assetfinder"):
        code, out, err = run_cmd(["assetfinder", "--subs-only", domain], timeout=60)
        if code == 0 and out:
            with open(subs_file, "a") as f:
                f.write(out)
        else:
            log(f"[!] assetfinder error: {err.strip()}")
    else:
        log("[!] assetfinder not available, skipping")

    # Deduplicate subs
    if file_has_content(subs_file):
        code, out, err = run_cmd(["sort", "-u", subs_file, "-o", subs_file])
    else:
        log("[!] No subdomains found. Aborting recon.")
        return None

    # --- Alive host probing ---
    alive_file = f"{base}/alive.txt"

    if not tool_available("httpx"):
        log("[!] httpx not available, cannot probe alive hosts")
        return None

    code, out, err = run_cmd(["httpx", "-l", subs_file, "-o", alive_file], timeout=180)
    if code != 0:
        log(f"[!] httpx error: {err.strip()}")

    if not file_has_content(alive_file):
        log("[!] No alive hosts found.")
        return None

    log(f"[✓] Recon complete. Alive hosts saved to {alive_file}")
    return alive_file
