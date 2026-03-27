import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN   = os.getenv("TELEGRAM_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")
FLASK_SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "dev-secret-change-me")
MAX_CONCURRENT_SCANS = int(os.getenv("MAX_CONCURRENT_SCANS", "5"))
