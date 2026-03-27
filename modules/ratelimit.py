"""
Simple in-process rate limiter.
Prevents the same domain from being scanned more than once
per COOLDOWN_SECONDS window, even across rapid web requests.
"""

import time
import threading

COOLDOWN_SECONDS = 300  # 5 minutes between scans of the same domain

_lock   = threading.Lock()
_last   = {}   # domain -> last_scan_epoch


def is_rate_limited(domain: str) -> tuple[bool, int]:
    """
    Returns (limited, seconds_remaining).
    limited=True means the domain was scanned too recently.
    """
    now = time.time()
    with _lock:
        last = _last.get(domain, 0)
        elapsed = now - last
        if elapsed < COOLDOWN_SECONDS:
            remaining = int(COOLDOWN_SECONDS - elapsed)
            return True, remaining
        return False, 0


def record_scan(domain: str):
    """Call this when a scan is accepted to start the cooldown."""
    with _lock:
        _last[domain] = time.time()
