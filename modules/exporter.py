"""
Export scan findings to JSON or CSV for use in other tools.
"""

import csv
import json
import os
from modules.utils import log


def export_json(domain: str, findings: list[dict]) -> str:
    path = f"output/{domain}/findings.json"
    with open(path, "w") as f:
        json.dump({"domain": domain, "findings": findings}, f, indent=2)
    log(f"[✓] JSON export saved to {path}")
    return path


def export_csv(domain: str, findings: list[dict]) -> str:
    path = f"output/{domain}/findings.csv"
    fields = ["type", "severity", "detail"]
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(findings)
    log(f"[✓] CSV export saved to {path}")
    return path
