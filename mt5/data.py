import pandas as pd
import MetaTrader5 as mt5
from config import TIMEFRAMES, MT5_LOGIN, MT5_PASSWORD, MT5_SERVER
from logs.logger import setup_logging

logger = setup_logging()


def get_realtime_data(symbol: str, timeframe: str, num_candles: int = 150) pd.DataFrame:
    try:
        if not mt5.initialize(
            login=MT5_LOGIN, password=MT5_PASSWORD, server=MT5_SERVER
        ):
            logger.error(f"Tidak dapat terhubung ke MT5: {mt5.last_error()}")
            return None
        tf = TIMEFRAMES.get(timeframe)
        rates = mt5.copy_rates_from_pos(symbol, tf, 0, num_candles)

        df = pd.DataFrame(rates)
        df["time"] = pd.to_datetime(df["time"], unit="s")
        df = df.rename(columns={"tick_volume": "volume"})

        return df

    except Exception as e:
        logger.error(f"Gagal mengambil data realtime: {e}")
        return None
