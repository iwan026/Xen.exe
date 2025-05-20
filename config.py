import os
import MetaTrader5 as mt5
from pathlib import Path

# Konfigurasi Path Direktori
BASE_DIR = Path(os.path.dirname(os.path.abspath(__file__)))
PLOTS_DIR = BASE_DIR / "plots" / "visual"
LOGS_DIR = BASE_DIR / "logs"

# Konfigurasi Telegram
BOT_TOKEN = "7667262262:AAFYkfcdd8OZQskNYQPJ9KbVO8rGE3rvouI"
FOUNDER_IDS = [1198920849]

# Konfigurasi MT5
MT5_LOGIN = 204313635
MT5_PASSWORD = "123@Demo"
MT5_SERVER = "Exness-MT5Trial7"

SYMBOLS = ["EURUSD"]

TIMEFRAMES = {
    "M1": mt5.TIMEFRAME_M1,
    "M5": mt5.TIMEFRAME_M5,
    "M15": mt5.TIMEFRAME_M15,
    "M30": mt5.TIMEFRAME_M30,
    "H1": mt5.TIMEFRAME_H1,
    "H4": mt5.TIMEFRAME_H4,
    "D1": mt5.TIMEFRAME_D1,
}
