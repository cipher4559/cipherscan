# CipherScan

Automated security reconnaissance and vulnerability scanning tool with a Flask web dashboard and CLI interface.

---

## ⚠️ Legal Warning

Only scan targets you **own** or have **explicit written authorization** to test.
Unauthorized scanning is illegal in most jurisdictions.

---

## Features

- Subdomain enumeration (subfinder, assetfinder)
- Alive host probing (httpx)
- Port & service scanning (nmap)
- Vulnerability templates (nuclei)
- Directory brute-force (dirsearch)
- URL harvesting (gau, waybackurls)
- XSS detection (dalfox) — requires authorization flag
- SQL injection detection (sqlmap) — requires authorization flag
- PDF, JSON, and CSV reports
- Web dashboard with scan history and findings viewer
- CLI for headless/automated use
- Telegram alerts
- Concurrency-limited threading (max 5 parallel scans)
- Per-domain scan rate limiting (5 min cooldown)

---

## Setup

```bash
git clone <repo>
cd cipherscan
chmod +x setup.sh
./setup.sh
```

Edit `.env` with your Telegram credentials (optional):

```
TELEGRAM_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id
FLASK_SECRET_KEY=a_random_string
MAX_CONCURRENT_SCANS=5
```

---

## Usage

### Web dashboard

```bash
python app.py
# Open http://127.0.0.1:5000
```

### CLI

```bash
# Recon + scanning only (no exploitation)
python cli.py -d example.com --authorize --no-exploit

# Full scan including XSS and SQLi
python cli.py -d example.com --authorize
```

---

## Project structure

```
cipherscan/
├── app.py              # Flask web dashboard
├── cli.py              # Standalone CLI runner
├── cipherscan.py       # Main scan engine
├── config.py           # Loads settings from .env
├── db.py               # SQLite: scans + findings tables
├── requirements.txt
├── setup.sh
├── .env.example
│
├── modules/
│   ├── utils.py        # Domain validation, run_cmd, logging
│   ├── installer.py    # Tool availability checks (runs once)
│   ├── ratelimit.py    # Per-domain scan cooldown
│   ├── recon.py        # subfinder, assetfinder, httpx
│   ├── scanner.py      # nmap, nuclei, dirsearch
│   ├── urls.py         # gau, waybackurls, param extraction
│   ├── exploiter.py    # dalfox (XSS), sqlmap (SQLi) — auth-gated
│   ├── analyzer.py     # Parses tool output into findings list
│   ├── reporter.py     # PDF report generation
│   ├── exporter.py     # JSON + CSV export
│   └── notifier.py     # Telegram alerts
│
├── templates/
│   ├── index.html      # Dashboard + scan history
│   └── results.html    # Per-scan findings viewer
│
├── output/             # Per-domain scan output folders
└── logs/               # scan.log
```

---

## Report outputs

Each completed scan produces:

| File | Description |
|------|-------------|
| `output/<domain>/report.pdf` | PDF with severity summary and all findings |
| `output/<domain>/findings.json` | Machine-readable findings |
| `output/<domain>/findings.csv` | Spreadsheet-friendly findings |
| `output/<domain>/nmap.txt` | Raw nmap output |
| `output/<domain>/nuclei.txt` | Raw nuclei output |
| `output/<domain>/xss.txt` | Raw dalfox output |
| `output/<domain>/sqlmap/` | Raw sqlmap output directory |

---

## Dependencies

Python: `flask`, `requests`, `reportlab`, `python-dotenv`

External tools (installed via `setup.sh`): `subfinder`, `assetfinder`, `httpx`, `nuclei`, `nmap`, `dirsearch`, `gau`, `waybackurls`, `dalfox`, `sqlmap`
