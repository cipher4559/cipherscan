import requests
from config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID
from modules.utils import log


def send_alert(msg: str):
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        log("[!] Telegram not configured — skipping notification")
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    try:
        resp = requests.get(
            url,
            params={"chat_id": TELEGRAM_CHAT_ID, "text": msg},
            timeout=10
        )
        if resp.status_code == 200:
            log("[✓] Telegram alert sent")
        else:
            log(f"[!] Telegram error {resp.status_code}: {resp.text}")
    except requests.RequestException as e:
        log(f"[!] Telegram request failed: {e}")
