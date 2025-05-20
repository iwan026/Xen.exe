import talib
import pandas as pd
from mt5.data import get_realtime_data
from logs.logger import setup_logging

logger = setup_logging()


class AnalisisSymbol:
    def add_exponential_moving_average(self, df: pd.DataFrame):
        df["ema_21"] = talib.EMA(df["close"], timeperiod=21)
        df["ema_50"] = talib.EMA(df["close"], timeperiod=50)

    def add_rsi(self, df: pd.DataFrame):
        df["rsi_14"] = talib.RSI(df["close"], timeperiod=14)

    def get_analisis(self, symbol: str, timeframe: str) -> pd.DataFrame:
        df = get_realtime_data(symbol, timeframe)
        self.add_exponential_moving_average(df)
        self.add_rsi(df)

        analisis = ""
        if df["close"] > df["ema_50"]:
            analisis += "📈 *Bullish*. Ditandai dengan harga saat ini di atas EMA 200"
        elif df["close"] < df["ema_50"]:
            analisis += "📉 *Bearish*. Ditandai dengan harga saat ini dibawah EMA 200"
        else:
            analisis += ""

        if df["rsi_14"] > 60 and df["rsi_14"] < 80:
            analisis += "RSI 14 sudah memasuki area *Overbought* menandakan bahwa ada kemungkinan terjadinya reversal"
        elif df["rsi_14"] > 20 and df["rsi_14"] < 40:
            analisis += "RSI 14 sudah memasuki area *Oversold*, ada kemungkinan akab terjadinya reversal"
        elif df["rsi_14"] < 20:
            analisis += (
                "RSI 14 sudah terlalu rendah, kemungkinan reversal sangat tinggi."
            )
        elif df["rsi_14"] > 80:
            analisis += (
                "RSI 14 sudah terlalu tinggi, kemungkinan reversal sangat tinggi."
            )
        else:
            analisis += ""

        return {"analisis": analisis}
