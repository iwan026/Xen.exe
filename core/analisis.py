import pandas as pd
import pandas_ta as ta
from config import DATA_DIR
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
        self.data["ema_50"] = ta.ema(self.data["close"], length=50)
        self.data["ema_200"] = ta.ema(self.data["close"], length=200)

    def add_rsi(self):
        self.data["rsi_14"] = ta.rsi(self.data["close"], length=14)

    def get_analisis(self, symbol: str):
        filename = f"{symbol.upper()}.csv"
        csv_path = DATA_DIR / filename

        random_candle = self.data.sanple(n=1).iloc[0]

        analisis = ""
        if random_candle["close"] > random_candle["ema_200"]:
            signal += "📈 *Bullish*. Ditandai dengan harga saat ini di atas EMA 200"
        elif random_candle["close"] < random_candle["ema_50"]:
            signal += "📉 *Bearish*. Ditandai dengan harga saat ini dibawah EMA 200"
        else:
            signal += ""

        if random_candle["rsi_14"] in range(60, 80):
            signal += "RSI 14 sudah memasuki area *Overbought* menandakan bahwa ada kemungkinan terjadinya reversal"
        elif random_candle["rsi_14"] in range(20, 40):
            signal += "RSI 14 sudah memasuki area *Oversold*, ada kemungkinan akab terjadinya reversal"
        elif random_candle["rsi_14"] < 20:
            signal += "RSI 14 sudah terlalu rendah, kemungkinan reversal sangat tinggi."
        elif random_candle["rsi_14"] > 80:
            signal += "RSI 14 sudah terlalu tinggi, kemungkinan reversal sangat tinggi."
        else:
            signal += ""

        return signal
