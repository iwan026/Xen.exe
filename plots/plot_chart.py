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
        plt.style.use("dark_background")
        fig, ax = plt.subplots(figsize=(16, 9), facecolor="#131722")

        candle_counts = {
            "M1": 100,
            "M5": 100,
            "M15": 100,
            "M30": 100,
            "H1": 80,
            "H4": 60,
            "D1": 60,
        }

        candle_count = candle_counts.get(timeframe.upper(), 100)
        display_df = df.tail(candle_count).copy()

        # Pastikan index datetime
        if not isinstance(display_df.index, pd.DatetimeIndex):
            display_df.index = pd.to_datetime(display_df.index)
        display_df = display_df.sort_index()

        # Isi nilai kosong
        display_df = display_df.ffill().bfill()

        # Siapkan data
        ohlc = display_df[["open", "high", "low", "close"]].values
        dates = range(len(display_df))

        # Lebar candle
        width = 0.6

        # Buat candlestick manual tanpa date_num
        for i, ohl in enumerate(ohlc):
            if not np.isnan(ohl).any():
                open_, high, low, close = ohl
                color = "#26a69a" if close >= open_ else "#ef5350"
                ax.add_patch(
                    plt.Rectangle(
                        (i - width / 2, open_), width, close - open_, color=color
                    )
                )
                ax.plot([i, i], [low, high], color=color, linewidth=1)

        # Moving average
        if "ema_21" in display_df.columns:
            ax.plot(
                dates,
                display_df["ema_21"],
                color="#2962FF",
                linewidth=1.2,
                label="EMA(21)",
            )
        if "ema_50" in display_df.columns:
            ax.plot(
                dates,
                display_df["ema_50"],
                color="#FF6D00",
                linewidth=1.2,
                label="EMA(50)",
            )
        ax.legend(loc="upper left", facecolor="#131722", edgecolor="#2a2e39")

        # Sumbu X
        ax.set_xticks(dates[:: max(len(dates) // 10, 1)])
        ax.set_xticklabels(
            display_df.index.strftime("%Y-%m-%d %H:%M")[:: max(len(dates) // 10, 1)],
            rotation=30,
            fontsize=9,
        )

        ax.set_title(
            f"{symbol.upper()} Timeframe {timeframe.upper()}",
            color="white",
            fontsize=14,
            fontweight="bold",
        )
        ax.set_facecolor("#131722")
        ax.grid(color="#2a2e39", linestyle="-", linewidth=0.5, alpha=0.5)

        # Sumbu Y otomatis
        ax.set_xlim(-1, len(display_df))
        valid_ohlc = ohlc[~np.isnan(ohlc).any(axis=1)]
        if len(valid_ohlc) > 0:
            low = np.min(valid_ohlc[:, 2])
            high = np.max(valid_ohlc[:, 1])
            padding = (high - low) * 0.08
            ax.set_ylim(low - padding, high + padding)

        # Watermark
        ax.text(
            0.99,
            0.01,
            f"{symbol.upper()} {timeframe.upper()}",
            fontsize=10,
            color="white",
            alpha=0.2,
            ha="right",
            va="bottom",
            transform=ax.transAxes,
        )

        # Simpan chart
        plot_path = PLOTS_DIR / f"{symbol}_{timeframe}_chart.png"
        plt.savefig(plot_path, dpi=150, bbox_inches="tight", pad_inches=0.2)
        plt.close()
        logger.info(f"Chart saved to {plot_path}")
        return plot_path
