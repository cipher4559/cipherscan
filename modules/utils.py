import os
import re
import subprocess
from datetime import datetime


DOMAIN_RE = re.compile(
    r'^(?:[a-zA-Z0-9]'
    r'(?:[a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)'
    r'+[a-zA-Z]{2,}$'
)


def validate_domain(domain: str) -> bool:
    """Return True only if domain is a safe, well-formed hostname."""
    return bool(DOMAIN_RE.match(domain)) and len(domain) < 253


def create_workspace(domain: str):
    os.makedirs(f"output/{domain}", exist_ok=True)
    os.makedirs("logs", exist_ok=True)


def log(msg: str):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] {msg}"
    print(line)
    os.makedirs("logs", exist_ok=True)
    with open("logs/scan.log", "a") as f:
        f.write(line + "\n")


def run_cmd(args: list, timeout: int = 300) -> tuple[int, str, str]:
    """
    Run a command safely using subprocess (no shell=True).
    Returns (returncode, stdout, stderr).
    """
    try:
        result = subprocess.run(
            args,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        return result.returncode, result.stdout, result.stderr
    except FileNotFoundError:
        return 1, "", f"Tool not found: {args[0]}"
    except subprocess.TimeoutExpired:
        return 1, "", f"Timed out after {timeout}s: {' '.join(args)}"
    except Exception as e:
        return 1, "", str(e)


def file_has_content(path: str) -> bool:
    """Return True if file exists and is non-empty."""
    return os.path.isfile(path) and os.path.getsize(path) > 0
