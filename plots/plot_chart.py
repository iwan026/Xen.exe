import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
from mplfinance.original_flavor import candlestick_ohlc
from config import PLOTS_DIR
from logs.logger import setup_logging

logger = setup_logging()


class ChartVisualizer:
    def generate_chart(self, df: pd.DataFrame, symbol: str, timeframe: str):
        # Styling
        plt.style.use("dark_background")
        fig, ax = plt.subplots(figsize=(14, 7), facecolor="#131722")

        display_df = df.tail(150).copy()
        display_df["date_num"] = mdates.date2num(display_df.index.to_pydatetime())
        ohlc = display_df[["date_num", "open", "high", "low", "close"]].values

        # Gambar Candle
        candlestick_ohlc(
            ax, ohlc, width=0.6 / 24, colorup="#26a69a", colordown="#ef5350", alpha=0.9
        )

        # Gambar exponential moving average
        if "ema_21" in display_df.columns and "ema_50" in display_df.columns:
            ax.plot(
                display_df.index,
                display_df["ema_21"],
                color="#2962FF",
                linewidth=1.2,
                alpha=0.7,
                label=f"EMA(21)",
            )
            ax.plot(
                display_df.index,
                display_df["ema_50"],
                color="#FF6D00",
                linewidth=1.2,
                alpha=0.7,
                label=f"EMA(50)",
            )

        # Style tradingview
        ax.set_title(
            f"{symbol.upper()} Timeframe {timeframe.upper()}",
            color="white",
            fontsize=14,
            fontweight="bold",
        )

        ax.set_facecolor("#131722")
        ax.grid(color="#2a2e39", linestyle="-", linewidth=0.5, alpha=0.7)

        ax.xaxis.set_major_formatter(mdates.DateFormatter("%m-%d %H:%M"))
        ax.xaxis.set_major_locator(mdates.HourLocator(interval=24))
        plt.xticks(rotation=45)

        # Adjust layout
        plt.tight_layout()

        # Save the chart
        plot_path = PLOTS_DIR / f"{self.symbol}_prediction.png"
        plt.savefig(plot_path, dpi=150, bbox_inches="tight")
        plt.close()
        return plot_path
