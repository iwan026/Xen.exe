import os
from pathlib import Path

# Konfigurasi Path Direktori
BASE_DIR = Path(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = BASE_DIR / "data"
LOGS_DIR = BASE_DIR / "logs"

# Konfigurasi Telegram
BOT_TOKEN = "7667262262:AAFYkfcdd8OZQskNYQPJ9KbVO8rGE3rvouI"
FOUNDER_IDS = [1198920849]

SYMBOLS = ["EURUSD"]
