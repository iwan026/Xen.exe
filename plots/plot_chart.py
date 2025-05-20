import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from mplfinance.original_flavor import candlestick_ohlc
from config import PLOTS_DIR
from logs.logger import setup_logging
import numpy as np

logger = setup_logging()


class ChartVisualizer:
    def __init__(self):
        self.candle_counts = {
            "M1": 100,
            "M5": 100,
            "M15": 100,
            "M30": 100,
            "H1": 80,
            "H4": 60,
            "D1": 60,
        }
        self.candle_widths = {
            "M1": 0.6 / 24 / 60,
            "M5": 0.6 / 24 / 12,
            "M15": 0.6 / 24 / 4,
            "M30": 0.6 / 24 / 2,
            "H1": 0.6 / 24,
            "H4": 0.6 / 6,
            "D1": 0.6,
        }
        self.date_formats = {
            "M1": "%H:%M",
            "M5": "%H:%M",
            "M15": "%H:%M",
            "M30": "%H:%M",
            "H1": "%m-%d %H:%M",
            "H4": "%m-%d",
            "D1": "%Y-%m-%d",
        }
        self.major_locators = {
            "M1": mdates.MinuteLocator(interval=30),
            "M5": mdates.MinuteLocator(interval=30),
            "M15": mdates.HourLocator(interval=2),
            "M30": mdates.HourLocator(interval=2),
            "H1": mdates.DayLocator(interval=1),
            "H4": mdates.DayLocator(interval=3),
            "D1": mdates.WeekdayLocator(interval=14),
        }

    def _setup_axes(self, ax, symbol, timeframe):
        ax.set_title(
            f"{symbol.upper()} Timeframe {timeframe.upper()}",
            color="white",
            fontsize=14,
            fontweight="bold",
        )
        ax.set_facecolor("#131722")
        ax.grid(color="#2a2e39", linestyle="-", linewidth=0.5, alpha=0.5)

        for spine in ["top", "right"]:
            ax.spines[spine].set_visible(False)
        for spine in ["left", "bottom"]:
            ax.spines[spine].set_color("#2a2e39")

    def _configure_time_axis(self, ax, timeframe):
        timeframe = timeframe.upper()
        date_format = self.date_formats.get(timeframe, "%m-%d %H:%M")

        # Set major locator and formatter
        locator = self.major_locators.get(timeframe, mdates.HourLocator(interval=24))
        ax.xaxis.set_major_locator(locator)
        ax.xaxis.set_major_formatter(mdates.DateFormatter(date_format))

        # IMPORTANT: Completely disable minor ticks on x-axis
        ax.xaxis.set_minor_locator(plt.NullLocator())

    def _configure_price_axis(self, ax, display_df):
        ax.yaxis.set_minor_locator(plt.MultipleLocator(0.0005))
        ax.grid(which="minor", color="#1c202b", linestyle="-", linewidth=0.2, alpha=0.3)
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{x:.4f}"))

    def _set_axis_limits(self, ax, display_df):
        low = np.percentile(display_df["low"].values, 2)
        high = np.percentile(display_df["high"].values, 98)
        padding = (high - low) * 0.08
        ax.set_ylim(low - padding, high + padding)
        ax.set_xlim(display_df.index.min(), display_df.index.max())

    def generate_chart(self, df: pd.DataFrame, symbol: str, timeframe: str):
        plt.style.use("dark_background")
        fig, ax = plt.subplots(figsize=(16, 9), facecolor="#131722")

        # Get data to display
        timeframe = timeframe.upper()
        candle_count = self.candle_counts.get(timeframe, 100)
        display_df = df.tail(candle_count).copy().fillna(method="ffill")

        # Prepare OHLC data
        display_df["date_num"] = mdates.date2num(display_df.index.to_pydatetime())
        ohlc = display_df[["date_num", "open", "high", "low", "close"]].values

        # Draw candles
        candlestick_ohlc(
            ax,
            ohlc,
            width=self.candle_widths.get(timeframe, 0.6 / 24),
            colorup="#26a69a",
            colordown="#ef5350",
            alpha=1.0,
        )

        # Draw EMAs if available
        if all(col in display_df.columns for col in ["ema_21", "ema_50"]):
            for period, color in [(21, "#2962FF"), (50, "#FF6D00")]:
                ax.plot(
                    display_df.index,
                    display_df[f"ema_{period}"],
                    color=color,
                    linewidth=1.2,
                    alpha=0.7,
                    label=f"EMA({period})",
                )
            ax.legend(loc="upper left", facecolor="#131722", edgecolor="#2a2e39")

        # Configure chart
        self._setup_axes(ax, symbol, timeframe)
        self._configure_time_axis(ax, timeframe)
        self._configure_price_axis(ax, display_df)
        self._set_axis_limits(ax, display_df)

        # Add watermark
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

        # Final adjustments
        plt.xticks(rotation=0)
        plt.subplots_adjust(left=0.08, right=0.92, top=0.92, bottom=0.15)

        # Save chart
        plot_path = PLOTS_DIR / f"{symbol}_{timeframe}_chart.png"
        plt.savefig(plot_path, dpi=150, bbox_inches="tight", pad_inches=0.2)
        plt.close()
        logger.info(f"Chart saved to {plot_path}")
        return plot_path
