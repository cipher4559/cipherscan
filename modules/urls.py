import os
from modules.utils import run_cmd, file_has_content, log
from modules.installer import tool_available


def collect_urls(domain: str) -> str | None:
    base = f"output/{domain}"
    gau_file = f"{base}/gau.txt"
    wb_file  = f"{base}/wayback.txt"
    all_file = f"{base}/all_urls.txt"

    if tool_available("gau"):
        log("[*] Running gau...")
        code, out, err = run_cmd(["gau", domain], timeout=180)
        if code == 0 and out:
            with open(gau_file, "w") as f:
                f.write(out)
        else:
            log(f"[!] gau error: {err.strip()}")
    else:
        log("[!] gau not available, skipping")

    if tool_available("waybackurls"):
        log("[*] Running waybackurls...")
        code, out, err = run_cmd(["waybackurls", domain], timeout=180)
        if code == 0 and out:
            with open(wb_file, "w") as f:
                f.write(out)
        else:
            log(f"[!] waybackurls error: {err.strip()}")
    else:
        log("[!] waybackurls not available, skipping")

    # Merge and deduplicate
    sources = [p for p in [gau_file, wb_file] if file_has_content(p)]
    if not sources:
        log("[!] No URLs collected.")
        return None

    code, _, err = run_cmd(["bash", "-c",
        f"cat {' '.join(sources)} | sort -u > {all_file}"])
    if not file_has_content(all_file):
        log("[!] URL dedup produced empty file.")
        return None

    log(f"[✓] URLs collected: {all_file}")
    return all_file


def extract_params(domain: str) -> str | None:
    base     = f"output/{domain}"
    all_file = f"{base}/all_urls.txt"
    params_file = f"{base}/params.txt"

    if not file_has_content(all_file):
        return None

    code, out, err = run_cmd(["grep", "=", all_file])
    if code != 0 or not out.strip():
        log("[!] No parameterised URLs found.")
        return None

    with open(params_file, "w") as f:
        f.write(out)

    log(f"[✓] Params extracted: {params_file}")
    return params_file
