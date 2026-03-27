import sqlite3
import json
from datetime import datetime

DB_PATH = "cipherscan.db"


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_conn()
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS scans (
        id        INTEGER PRIMARY KEY AUTOINCREMENT,
        domain    TEXT    NOT NULL,
        status    TEXT    NOT NULL DEFAULT 'Queued',
        started_at  TEXT,
        finished_at TEXT
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS findings (
        id        INTEGER PRIMARY KEY AUTOINCREMENT,
        scan_id   INTEGER NOT NULL REFERENCES scans(id),
        type      TEXT,
        detail    TEXT,
        severity  TEXT
    )
    """)

    conn.commit()
    conn.close()


def insert_scan(domain):
    conn = get_conn()
    c = conn.cursor()
    c.execute(
        "INSERT INTO scans (domain, status, started_at) VALUES (?, 'Running', ?)",
        (domain, datetime.now().isoformat())
    )
    scan_id = c.lastrowid
    conn.commit()
    conn.close()
    return scan_id


def update_scan_status(scan_id, status):
    conn = get_conn()
    c = conn.cursor()
    c.execute(
        "UPDATE scans SET status=?, finished_at=? WHERE id=?",
        (status, datetime.now().isoformat(), scan_id)
    )
    conn.commit()
    conn.close()


def insert_findings(scan_id, findings):
    if not findings:
        return
    conn = get_conn()
    c = conn.cursor()
    for f in findings:
        c.execute(
            "INSERT INTO findings (scan_id, type, detail, severity) VALUES (?, ?, ?, ?)",
            (scan_id, f.get("type"), f.get("detail"), f.get("severity"))
        )
    conn.commit()
    conn.close()


def get_all_scans():
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT * FROM scans ORDER BY id DESC")
    rows = [dict(r) for r in c.fetchall()]
    conn.close()
    return rows


def get_scan_with_findings(scan_id):
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT * FROM scans WHERE id=?", (scan_id,))
    scan = c.fetchone()
    if not scan:
        conn.close()
        return None, []
    c.execute("SELECT * FROM findings WHERE scan_id=?", (scan_id,))
    findings = [dict(r) for r in c.fetchall()]
    conn.close()
    return dict(scan), findings


def is_domain_running(domain):
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT id FROM scans WHERE domain=? AND status='Running'", (domain,))
    row = c.fetchone()
    conn.close()
    return row is not None
