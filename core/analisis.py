import pandas as pd
import pandas_ta as ta
from mt5.data import get_realtime_data
from logs.logger import setup_logging

logger = setup_logging()


class AnalisisSymbol:
    def __init__(self, csv_path):
        self.data = pd.read_csv(csv_path).sample(n=60, random_state=42)
        self.generate_technical_indicators()

    def generate_technical_indicators(self):
        self.add_exponential_moving_average()
        self.add_rsi()

    def add_exponential_moving_average(self):
        self.data["ema_21"] = ta.ema(self.data["close"], length=21)
        self.data["ema_50"] = ta.ema(self.data["close"], length=50)

    def add_rsi(self):
        self.data["rsi_14"] = ta.rsi(self.data["close"], length=14)

    def get_analisis(self, symbol: str):
        df = get_realtime_data(df)

        analisis = ""
        if df["close"] > df["ema_200"]:
            signal += "📈 *Bullish*. Ditandai dengan harga saat ini di atas EMA 200"
        elif df["close"] < df["ema_50"]:
            signal += "📉 *Bearish*. Ditandai dengan harga saat ini dibawah EMA 200"
        else:
            signal += ""

        if df["rsi_14"] in range(60, 80):
            signal += "RSI 14 sudah memasuki area *Overbought* menandakan bahwa ada kemungkinan terjadinya reversal"
        elif df["rsi_14"] in range(20, 40):
            signal += "RSI 14 sudah memasuki area *Oversold*, ada kemungkinan akab terjadinya reversal"
        elif df["rsi_14"] < 20:
            signal += "RSI 14 sudah terlalu rendah, kemungkinan reversal sangat tinggi."
        elif df["rsi_14"] > 80:
            signal += "RSI 14 sudah terlalu tinggi, kemungkinan reversal sangat tinggi."
        else:
            signal += ""

        return signal
