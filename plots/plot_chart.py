import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from mplfinance.original_flavor import candlestick_ohlc
from config import PLOTS_DIR
from logs.logger import setup_logging
import numpy as np
from datetime import timedelta

logger = setup_logging()


class ChartVisualizer:
    def generate_chart(self, df: pd.DataFrame, symbol: str, timeframe: str):
        # Styling
        plt.style.use("dark_background")
        fig, ax = plt.subplots(figsize=(14, 7), facecolor="#131722")

        candle_counts = {
            "M1": 150,
            "M5": 150,
            "M15": 150,
            "M30": 150,
            "H1": 120,
            "H4": 100,
            "D1": 90,
        }

        candle_count = candle_counts.get(timeframe.upper(), 150)

        display_df = df.tail(candle_count).copy()
        display_df["date_num"] = mdates.date2num(display_df.index.to_pydatetime())
        ohlc = display_df[["date_num", "open", "high", "low", "close"]].values

        # Gambar Candle dengan width yang sesuai berdasarkan timeframe
        candle_width = {
            "M1": 0.6 / 24 / 60,
            "M5": 0.6 / 24 / 12,
            "M15": 0.6 / 24 / 60,
            "M30": 0.6 / 24 / 2,
            "H1": 0.6 / 24,
            "H4": 0.6 / 6,
            "D1": 0.6,
        }

        width = candle_width.get(timeframe.upper(), 0.6 / 24)

        candlestick_ohlc(
            ax, ohlc, width=width, colorup="#26a69a", colordown="#ef5350", alpha=0.9
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

            # Tambahkan legend
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

        # Sesuaikan format date dan interval berdasarkan timeframe
        date_formats = {
            "M1": "%H:%M",
            "M5": "%H:%M",
            "M15": "%H:%M",
            "M30": "%m-%d %H:%M",
            "H1": "%m-%d %H:%M",
            "H4": "%m-%d",
            "D1": "%Y-%m-%d",
        }

        # Default format jika timeframe tidak dikenal
        date_format = date_formats.get(timeframe.upper(), "%m-%d %H:%M")

        # Interval label waktu yang disesuaikan dengan timeframe
        if timeframe.lower() in ["M1", "M5"]:
            ax.xaxis.set_major_locator(mdates.MinuteLocator(interval=15))
        elif timeframe.lower() in ["M15", "M30"]:
            ax.xaxis.set_major_locator(mdates.HourLocator(interval=1))
        elif timeframe.lower() == "H1":
            ax.xaxis.set_major_locator(mdates.DayLocator(interval=1))
        elif timeframe.lower() == "H4":
            ax.xaxis.set_major_locator(mdates.DayLocator(interval=3))
        elif timeframe.lower() == "D1":
            ax.xaxis.set_major_locator(mdates.WeekdayLocator(interval=1))
        else:
            ax.xaxis.set_major_locator(mdates.HourLocator(interval=24))

        ax.xaxis.set_major_formatter(mdates.DateFormatter(date_format))

        # Minor ticks untuk grid yang lebih halus
        ax.xaxis.set_minor_locator(mdates.AutoDateLocator())
        ax.yaxis.set_minor_locator(plt.MultipleLocator(0.0005))
        ax.grid(which="minor", color="#1c202b", linestyle="-", linewidth=0.2, alpha=0.3)

        # Memperbaiki tampilan y-axis dengan format 4 digit
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{x:.4f}"))

        # Memperbaiki rotasi label dan spacing
        plt.xticks(rotation=45)

        # Tambahkan padding
        plt.subplots_adjust(left=0.08, right=0.92, top=0.92, bottom=0.15)

        # Dynamically set y-axis limits with a bit of padding
        y_range = display_df["high"].max() - display_df["low"].min()
        y_padding = y_range * 0.05  # 5% padding

        ax.set_ylim(
            display_df["low"].min() - y_padding, display_df["high"].max() + y_padding
        )

        # Hapus spines yang tidak perlu
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_color("#2a2e39")
        ax.spines["bottom"].set_color("#2a2e39")

        # Tambahkan watermark dengan opacity rendah
        fig.text(
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
