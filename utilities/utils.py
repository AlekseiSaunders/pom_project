# utils.py

import logging
import os
from datetime import datetime
from .config import LOG_DIR


# Set up logging
def setup_logging():
    # Ensure the log directory exists
    os.makedirs(LOG_DIR, exist_ok=True)

    # Create a timestamp for the log file name
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    log_file = os.path.join(LOG_DIR, f'log_{timestamp}.log')

    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()  # This will keep console logging as well
        ]
    )

    # Create a logger
    logger = logging.getLogger(__name__)

    logger.info(f"Logging initialized. Log file: {log_file}")

    return logger


# Create a global logger instance
logger = setup_logging()
