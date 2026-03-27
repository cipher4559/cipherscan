#!/bin/bash
# CipherScan Setup Script
# Run once: chmod +x setup.sh && ./setup.sh

set -e

echo ""
echo "╔══════════════════════════════════════╗"
echo "║        CipherScan Setup              ║"
echo "╚══════════════════════════════════════╝"
echo ""

# ── Python deps ──────────────────────────────────────────────────────────────
echo "[*] Installing Python dependencies..."
pip install -r requirements.txt --quiet
echo "[✓] Python deps installed"

# ── .env ─────────────────────────────────────────────────────────────────────
if [ ! -f .env ]; then
    cp .env.example .env
    echo "[✓] .env created from template — edit it to add your Telegram credentials"
else
    echo "[✓] .env already exists, skipping"
fi

# ── Go tools ─────────────────────────────────────────────────────────────────
if command -v go &>/dev/null; then
    echo "[*] Installing Go-based tools..."
    go install github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
    go install github.com/tomnomnom/assetfinder@latest
    go install github.com/projectdiscovery/httpx/cmd/httpx@latest
    go install github.com/projectdiscovery/nuclei/v2/cmd/nuclei@latest
    go install github.com/lc/gau/v2/cmd/gau@latest
    go install github.com/tomnomnom/waybackurls@latest
    go install github.com/hahwul/dalfox/v2@latest
    echo "[✓] Go tools installed"
else
    echo "[!] Go not found — skipping Go tools (subfinder, httpx, nuclei, etc.)"
    echo "    Install Go from https://go.dev/dl/ then re-run this script"
fi

# ── apt tools ─────────────────────────────────────────────────────────────────
if command -v apt &>/dev/null; then
    echo "[*] Installing apt tools..."
    sudo apt install -y nmap sqlmap --quiet
    echo "[✓] nmap + sqlmap installed"
else
    echo "[!] apt not found — install nmap and sqlmap manually"
fi

# ── pip tools ─────────────────────────────────────────────────────────────────
echo "[*] Installing dirsearch..."
pip install dirsearch --quiet
echo "[✓] dirsearch installed"

# ── Workspace dirs ────────────────────────────────────────────────────────────
mkdir -p output logs static
echo "[✓] Directories created"

# ── Done ──────────────────────────────────────────────────────────────────────
echo ""
echo "╔══════════════════════════════════════╗"
echo "║  Setup complete! Run:                ║"
echo "║    python app.py                     ║"
echo "╚══════════════════════════════════════╝"
echo ""
