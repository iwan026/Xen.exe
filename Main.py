from bots.telegram_bot import TelegramBot
from logs.logger import setup_logging

logger = setup_logging()


def main():
    """Ini entry point sistem"""
    try:
        logger.info("Started Xen.exe...")
        bot = TelegramBot()
        bot.run()
    except Exception as e:
        logger.error(f"Error: {e}")
        return None


if __name__ == "__main__":
    main()
