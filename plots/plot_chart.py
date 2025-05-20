import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from mplfinance.original_flavor import candlestick_ohlc
from config import PLOTS_DIR
from logs.logger import setup_logging
import numpy as np

logger = setup_logging()


class ChartVisualizer:
    def generate_chart(self, df: pd.DataFrame, symbol: str, timeframe: str):
        # Setup dasar chart
        plt.style.use("dark_background")
        fig, ax = plt.subplots(figsize=(16, 9), facecolor="#131722")

        # Ambil data yang mau ditampilin
        candle_count = 100 if timeframe in ["M1", "M5", "M15", "M30"] else 60
        display_df = df.tail(candle_count).copy().fillna(method="ffill")

        # Buat candle chart
        display_df["date_num"] = mdates.date2num(display_df.index.to_pydatetime())
        ohlc = display_df[["date_num", "open", "high", "low", "close"]].values
        candlestick_ohlc(
            ax, ohlc, width=0.6 / 24, colorup="#26a69a", colordown="#ef5350"
        )

        # Kalau ada EMA, tambahkan
        if "ema_21" in display_df.columns:
            ax.plot(
                display_df.index, display_df["ema_21"], color="#2962FF", label="EMA 21"
            )
        if "ema_50" in display_df.columns:
            ax.plot(
                display_df.index, display_df["ema_50"], color="#FF6D00", label="EMA 50"
            )
        if "ema_21" in display_df.columns or "ema_50" in display_df.columns:
            ax.legend()

        # Setting tampilan
        ax.set_title(f"{symbol} {timeframe}", color="white")
        ax.set_facecolor("#131722")
        ax.grid(color="#2a2e39", alpha=0.5)

        # Format tanggal otomatis
        ax.xaxis.set_major_formatter(mdates.AutoDateFormatter(mdates.AutoDateLocator()))

        # Setting sumbu y
        low = display_df["low"].min()
        high = display_df["high"].max()
        padding = (high - low) * 0.1
        ax.set_ylim(low - padding, high + padding)

        # Simpan chart
        plot_path = PLOTS_DIR / f"{symbol}_{timeframe}_chart.png"
        plt.savefig(plot_path, dpi=150, bbox_inches="tight")
        plt.close()

        logger.info(f"Chart disimpan di {plot_path}")
        return plot_path
