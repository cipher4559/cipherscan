import shutil
import subprocess
from modules.utils import log

TOOLS = {
    "subfinder":    ("go", "go install github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest"),
    "assetfinder":  ("go", "go install github.com/tomnomnom/assetfinder@latest"),
    "httpx":        ("go", "go install github.com/projectdiscovery/httpx/cmd/httpx@latest"),
    "nuclei":       ("go", "go install github.com/projectdiscovery/nuclei/v2/cmd/nuclei@latest"),
    "nmap":         ("apt", "sudo apt install nmap -y"),
    "dirsearch":    ("pip", "pip install dirsearch"),
    "gau":          ("go", "go install github.com/lc/gau/v2/cmd/gau@latest"),
    "waybackurls":  ("go", "go install github.com/tomnomnom/waybackurls@latest"),
    "dalfox":       ("go", "go install github.com/hahwul/dalfox/v2@latest"),
    "sqlmap":       ("apt", "sudo apt install sqlmap -y"),
}

_checked = False
_missing = []


def is_installed(tool: str) -> bool:
    return shutil.which(tool) is not None


def install_tools():
    """Check and install missing tools. Only runs once per process."""
    global _checked, _missing
    if _checked:
        if _missing:
            log(f"[!] Previously missing tools still absent: {', '.join(_missing)}")
        return

    _missing = []
    for tool, (method, cmd) in TOOLS.items():
        if is_installed(tool):
            log(f"[✓] {tool} already installed")
            continue

        log(f"[!] Installing {tool} via {method}...")
        try:
            subprocess.run(cmd, shell=True, check=True, timeout=120)
            if is_installed(tool):
                log(f"[✓] {tool} installed successfully")
            else:
                log(f"[✗] {tool} install command ran but binary not found")
                _missing.append(tool)
        except subprocess.CalledProcessError as e:
            log(f"[✗] Failed to install {tool}: {e}")
            _missing.append(tool)
        except subprocess.TimeoutExpired:
            log(f"[✗] Install timed out for {tool}")
            _missing.append(tool)

    _checked = True

    if _missing:
        log(f"[!] Warning — these tools are missing and will be skipped: {', '.join(_missing)}")


def tool_available(tool: str) -> bool:
    return is_installed(tool)
