import logging
from config import LOGS_DIR


def setup_logging():
    """Setup logging dan debugger"""
    log_file = LOGS_DIR / "app.log"
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    return logging.getLogger(__name__)
