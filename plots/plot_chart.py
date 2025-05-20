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

        # Jumlah candle yang ditampilkan berdasarkan timeframe
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

        # Pastikan index adalah datetime dan diurutkan
        if not isinstance(display_df.index, pd.DatetimeIndex):
            display_df.index = pd.to_datetime(display_df.index)
        display_df = display_df.sort_index()

        # Fill NA values
        display_df = display_df.ffill().bfill()

        # Siapkan data OHLC tanpa konversi date_num
        ohlc = display_df[["open", "high", "low", "close"]].values
        dates = display_df.index

        # Lebar candle berdasarkan timeframe
        candle_width_map = {
            "M1": 0.0004,  # ~0.6/24/60
            "M5": 0.002,  # ~0.6/24/12
            "M15": 0.006,  # ~0.6/24/4
            "M30": 0.012,  # ~0.6/24/2
            "H1": 0.025,  # ~0.6/24
            "H4": 0.1,  # ~0.6/6
            "D1": 0.6,
        }
        width = candle_width_map.get(timeframe.upper(), 0.025)

        # Buat candlestick manual tanpa date_num
        for i, date in enumerate(dates):
            if not np.isnan(ohlc[i]).any():  # Pastikan tidak ada NaN
                color = (
                    "#26a69a" if ohlc[i, 3] >= ohlc[i, 0] else "#ef5350"
                )  # close >= open
                rect = plt.Rectangle(
                    (mdates.date2num(date) - width / 2, ohlc[i, 0]),
                    width,
                    ohlc[i, 3] - ohlc[i, 0],
                    facecolor=color,
                    edgecolor=color,
                )
                ax.add_patch(rect)
                # Garis vertikal (high-low)
                ax.plot(
                    [mdates.date2num(date), mdates.date2num(date)],
                    [ohlc[i, 1], ohlc[i, 2]],
                    color=color,
                    linewidth=1,
                )

        # Gambar moving average jika tersedia
        if "ema_21" in display_df.columns and "ema_50" in display_df.columns:
            ax.plot(
                dates,
                display_df["ema_21"],
                color="#2962FF",
                linewidth=1.2,
                alpha=0.7,
                label="EMA(21)",
            )
            ax.plot(
                dates,
                display_df["ema_50"],
                color="#FF6D00",
                linewidth=1.2,
                alpha=0.7,
                label="EMA(50)",
            )
            ax.legend(loc="upper left", facecolor="#131722", edgecolor="#2a2e39")

        # Style tradingview
        ax.set_title(
            f"{symbol.upper()} Timeframe {timeframe.upper()}",
            color="white",
            fontsize=14,
            fontweight="bold",
        )

        ax.set_facecolor("#131722")
        ax.grid(color="#2a2e39", linestyle="-", linewidth=0.5, alpha=0.5)

        # Format tanggal
        locator = mdates.AutoDateLocator()
        ax.xaxis.set_major_locator(locator)
        ax.xaxis.set_major_formatter(mdates.ConciseDateFormatter(locator))
        plt.xticks(rotation=30)

        # Atur batas sumbu
        if len(dates) > 0:
            valid_ohlc = ohlc[~np.isnan(ohlc).any(axis=1)]
            if len(valid_ohlc) > 0:
                low = np.min(valid_ohlc[:, 2])  # low
                high = np.max(valid_ohlc[:, 1])  # high
                padding = (high - low) * 0.08
                ax.set_ylim(low - padding, high + padding)
                ax.set_xlim(dates[0], dates[-1])

        # Hapus spines dan tambahkan watermark
        for spine in ["top", "right"]:
            ax.spines[spine].set_visible(False)
        for spine in ["left", "bottom"]:
            ax.spines[spine].set_color("#2a2e39")

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

        # Save the chart
        plot_path = PLOTS_DIR / f"{symbol}_{timeframe}_chart.png"
        plt.savefig(plot_path, dpi=150, bbox_inches="tight", pad_inches=0.2)
        plt.close()
        logger.info(f"Chart saved to {plot_path}")
        return plot_path
